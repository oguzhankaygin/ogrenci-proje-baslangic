import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugin"
SCRIPT = PLUGIN / "skills/proje-baslat/scripts/baslat.py"
KONU_SKILL = PLUGIN / "skills/konu-sayfasi"
KONU_EXAMPLE = KONU_SKILL / "ornek/konu-ikili-arama.html"
PACKAGE = "ogr_3_veri"
COMMON = {".editorconfig", ".gitignore", "CLAUDE.md", "README.md"}
TEAM = {
    "CONTRIBUTING.md",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/gorev.md",
    "docs/gorev-dagilimi.md",
    ".github/workflows/test.yml",
}
LANGUAGES = {
    "python": {
        "pyproject.toml",
        f"src/{PACKAGE}/__init__.py",
        f"src/{PACKAGE}/__main__.py",
        "tests/__init__.py",
        "tests/test_topla.py",
    },
    "javascript": {"package.json", "eslint.config.js", "src/index.js", "src/topla.js",
                   "test/topla.test.js"},
    "java": {"pom.xml", f"src/main/java/edu/{PACKAGE}/App.java",
             f"src/test/java/edu/{PACKAGE}/AppTest.java"},
    "c": {".clang-format", "Makefile", "src/main.c", "src/topla.c", "src/topla.h",
          "tests/test_topla.c"},
}


def read_frontmatter(path):
    """Depoda kullanılan JSON tırnaklı YAML dizgesi alt kümesini ayrıştırır."""
    opening, content, body = path.read_text(encoding="utf-8").split("---\n", 2)
    if opening or not body.strip():
        raise ValueError(f"Frontmatter veya belge gövdesi eksik: {path}")
    fields = {}
    for line in content.splitlines():
        key, value = line.split(": ", 1)
        if not key or key in fields:
            raise ValueError(f"Geçersiz frontmatter anahtarı: {key}")
        value = json.loads(value)
        if not isinstance(value, str):
            raise ValueError(f"Frontmatter değeri dizge olmalı: {key}")
        fields[key] = value
    return fields


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(directory.cleanup)
        self.cwd = Path(directory.name)

    def generate(self, language="python", mode="bireysel", name="3-Veri", extra=(), env=None):
        return self.run_command(
            [sys.executable, str(SCRIPT), f"--ad={name}", "--dil", language, "--tur", mode,
             "--no-git", *extra],
            self.cwd, env,
        )

    def run_command(self, command, cwd, env=None):
        return subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=45)

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_each_language_and_mode(self):
        ci_commands = {
            "python": "python3 -m unittest",
            "javascript": "npm test",
            "java": "mvn -B test",
            "c": "make test",
        }
        for language, expected in LANGUAGES.items():
            for mode in ("bireysel", "takim"):
                with self.subTest(language=language, mode=mode):
                    target = self.cwd / f"{language}-{mode}"
                    self.assert_success(self.generate(
                        language, mode, extra=("--hedef", str(target), "--ders", "BLM203 Veri Yapıları"),
                    ))
                    actual = {path.relative_to(target).as_posix() for path in target.rglob("*")
                              if path.is_file()}
                    self.assertEqual(actual, COMMON | expected | (TEAM if mode == "takim" else set()))
                    for relative in actual:
                        self.assertNotIn("{{", relative)
                        self.assertNotIn("{{", (target / relative).read_text(encoding="utf-8"), relative)
                    readme = (target / "README.md").read_text(encoding="utf-8")
                    self.assertIn("BLM203 Veri Yapıları", readme)
                    for heading in ("Amaç", "Kurulum", "Çalıştırma", "Test", "Ekip", "Lisans"):
                        self.assertIn(f"## {heading}\n", readme)
                    self.assertIn("## Öğrenme modu", (target / "CLAUDE.md").read_text(encoding="utf-8"))
                    if mode == "takim":
                        workflow = (target / ".github/workflows/test.yml").read_text(encoding="utf-8")
                        self.assertIn("- run: " + ci_commands[language], workflow)
                    if language == "javascript":
                        manifest = json.loads((target / "package.json").read_text(encoding="utf-8"))
                        self.assertEqual(manifest["scripts"]["test"], "node --test")
                    if language == "java":
                        self.assertTrue(ElementTree.parse(target / "pom.xml").getroot().tag.endswith("}project"))

    def test_existing_empty_target_is_accepted(self):
        target = self.cwd / "3-Veri"
        target.mkdir()
        self.assert_success(self.generate())
        self.assertTrue((target / "README.md").is_file())

    def test_nonempty_target_is_rejected(self):
        target = self.cwd / "3-Veri"
        target.mkdir()
        sentinel = target / ".sakla"
        sentinel.write_text("koru", encoding="utf-8")
        result = self.generate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("boş", result.stderr)
        self.assertEqual(list(target.iterdir()), [sentinel])
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "koru")

    def test_symlink_target_is_rejected(self):
        target = self.cwd / "gercek"
        target.mkdir()
        (self.cwd / "3-Veri").symlink_to(target, target_is_directory=True)
        self.assertNotEqual(self.generate().returncode, 0)
        self.assertEqual(list(target.iterdir()), [])

    def test_invalid_names_are_rejected(self):
        for name in ("", "../kac", "iki kelime", "ad/alt", "ad;komut"):
            with self.subTest(name=name):
                self.assertNotEqual(self.generate(name=name).returncode, 0)
        self.assertEqual(list(self.cwd.iterdir()), [])

    def test_dry_run_lists_files_without_writing(self):
        result = self.generate(mode="takim", extra=("--hedef", "yeni/proje", "--git", "--kuru"))
        self.assert_success(result)
        files = result.stdout.splitlines()[1:]
        self.assertEqual(files, sorted(COMMON | TEAM | LANGUAGES["python"]))
        self.assertEqual(list(self.cwd.iterdir()), [])

    def test_python_generated_tests(self):
        self.assert_success(self.generate("python"))
        result = self.run_command([sys.executable, "-m", "unittest"], self.cwd / "3-Veri")
        self.assert_success(result)
        self.assertIn("Ran 1 test", result.stderr)

    @unittest.skipUnless(shutil.which("node"), "Node.js bulunamadı")
    def test_javascript_generated_tests(self):
        self.assert_success(self.generate("javascript"))
        result = self.run_command(["node", "--test", "--test-reporter=tap"], self.cwd / "3-Veri")
        self.assert_success(result)
        self.assertIn("# pass 1", result.stdout)

    @unittest.skipUnless(shutil.which("make") and shutil.which("gcc"), "make veya gcc bulunamadı")
    def test_c_generated_tests(self):
        self.assert_success(self.generate("c"))
        self.assert_success(self.run_command(["make", "test", "CC=gcc"], self.cwd / "3-Veri"))

    def test_missing_git_is_reported(self):
        result = self.generate(extra=("--git",), env={**os.environ, "PATH": ""})
        self.assert_success(result)
        self.assertIn("Git bulunamadı", result.stdout)
        self.assertTrue((self.cwd / "3-Veri" / "README.md").exists())

    @unittest.skipUnless(shutil.which("git"), "Git bulunamadı")
    def test_missing_git_identity_leaves_initialized_repository(self):
        config = self.cwd / "gitconfig"
        config.write_text("[user]\n    useConfigOnly = true\n", encoding="utf-8")
        env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=str(config))
        result = self.generate(extra=("--git",), env=env)
        self.assert_success(result)
        self.assertIn("Git kimliği eksik", result.stdout)
        target = self.cwd / "3-Veri"
        self.assertTrue((target / ".git").is_dir())
        self.assertNotEqual(self.run_command(["git", "rev-parse", "--verify", "HEAD"], target, env).returncode, 0)


class PluginTests(unittest.TestCase):
    def test_json_manifests(self):
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        entry, = marketplace["plugins"]
        self.assertEqual(marketplace["name"], "ogrenci-proje-baslangic")
        self.assertEqual(entry["name"], manifest["name"])
        self.assertEqual(entry["version"], manifest["version"])
        self.assertEqual((ROOT / entry["source"]).resolve(), PLUGIN)
        self.assertEqual(marketplace["owner"], manifest["author"])

    def test_skill_frontmatter(self):
        skills = sorted((PLUGIN / "skills").glob("*/SKILL.md"))
        self.assertEqual({path.parent.name for path in skills}, {"proje-baslat", "ogrenme-modu", "konu-sayfasi"})
        for path in skills:
            with self.subTest(path=path):
                metadata = read_frontmatter(path)
                self.assertEqual(set(metadata), {"name", "description"})
                self.assertEqual(metadata["name"], path.parent.name)
                self.assertIn("Tetikleyiciler:", metadata["description"])

    def test_command_frontmatter(self):
        commands = sorted((PLUGIN / "commands").glob("*.md"))
        self.assertEqual({path.stem for path in commands}, {"proje-baslat", "ipucu", "teslim-kontrol", "konu-sayfasi"})
        for path in commands:
            with self.subTest(path=path):
                metadata = read_frontmatter(path)
                self.assertEqual(set(metadata), {"description", "argument-hint"})
                self.assertTrue(metadata["description"])

    def test_konu_sayfasi_command_references_skill(self):
        command = PLUGIN / "commands/konu-sayfasi.md"
        self.assertEqual(read_frontmatter(command)["argument-hint"], "[konu]")
        self.assertIn("`ogrenci-proje:konu-sayfasi`", command.read_text(encoding="utf-8"))

    def test_konu_sayfasi_skill_requirements(self):
        skill = (KONU_SKILL / "SKILL.md").read_text(encoding="utf-8")
        for text in ("Önce tahmin et", "Nereden doğrulamalı", "CDN"):
            with self.subTest(text=text):
                self.assertIn(text, skill)

    def test_konu_sayfasi_example_is_offline_and_accessible(self):
        html = KONU_EXAMPLE.read_text(encoding="utf-8")
        self.assertNotRegex(html, r"""(?i)\s(?:src|href)\s*=\s*["']?\s*https?://""")
        self.assertNotRegex(html, r"(?i)<script\b[^>]*\ssrc\s*=")
        self.assertNotIn("innerHTML", html)
        for text in ('lang="tr"', "prefers-color-scheme", "prefers-reduced-motion"):
            with self.subTest(text=text):
                self.assertIn(text, html)
        self.assertRegex(html, r'aria-live\s*=|role\s*=\s*"status"')

    def test_konu_sayfasi_example_script_syntax(self):
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node bulunamadı")
        html = KONU_EXAMPLE.read_text(encoding="utf-8")
        scripts = re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.IGNORECASE | re.DOTALL)
        self.assertTrue(scripts)
        for script in scripts:
            result = subprocess.run(
                [node, "--check", "-"], input=script, capture_output=True, text=True, encoding="utf-8"
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
