"""Ders projesi şablonlarını yeni veya boş bir dizine üretir."""

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess

TEMPLATES = Path(__file__).resolve().parents[1] / "templates"
PLACEHOLDER = re.compile(r"\{\{([a-z_]+)\}\}")
COMMANDS = {
    "python": {
        "kurulum": "python3 -m venv .venv\n. .venv/bin/activate\npython3 -m pip install ruff",
        "calistir": "python3 -m src.{{paket}}",
        "test": "python3 -m unittest",
        "lint": "ruff check .",
        "format": "ruff format .",
    },
    "javascript": {
        "kurulum": "npm install",
        "calistir": "npm start",
        "test": "npm test",
        "lint": "npm run lint",
        "format": "npm run format",
    },
    "java": {
        "kurulum": "mvn -q package",
        "calistir": "java -cp target/classes edu.{{paket}}.App",
        "test": "mvn test",
        "lint": "mvn spotless:check",
        "format": "mvn spotless:apply",
    },
    "c": {
        "kurulum": "make",
        "calistir": "./build/proje",
        "test": "make test",
        "lint": "make lint",
        "format": "make format",
    },
}
PREREQUISITES = {
    "python": "Python 3.10+",
    "javascript": "Node.js 22.13+ (22.x) veya 24+ ve npm",
    "java": "JDK 17 ve Maven",
    "c": "C derleyicisi, make ve biçim denetimi için clang-format",
}


def render(template, values):
    return PLACEHOLDER.sub(lambda match: values[match[1]], template)


def plan_files(args):
    package = "ogr_" + args.ad.lower().replace("-", "_")
    values = {
        "ad": args.ad,
        "paket": package,
        "ders": args.ders or "TODO",
        "tur": {"bireysel": "Bireysel", "takim": "Takım"}[args.tur],
        "gereksinimler": PREREQUISITES[args.dil],
        "ekip": (
            "TODO: Üyeleri yazın ve [görev dağılımını](docs/gorev-dagilimi.md) doldurun."
            if args.tur == "takim"
            else "TODO: Adınızı ve proje sorumluluğunuzu yazın."
        ),
    }
    values.update({key: render(value, values) for key, value in COMMANDS[args.dil].items()})

    roots = [TEMPLATES / "ortak", TEMPLATES / args.dil]
    if args.tur == "takim":
        roots.extend([TEMPLATES / "takim", TEMPLATES / "ci" / args.dil])
    files = {}
    for root in roots:
        for source in sorted(root.rglob("*")):
            if not source.is_file():
                continue
            if not source.resolve().is_relative_to(TEMPLATES):
                raise ValueError(f"Şablon yolu geçersiz: {source}")
            destination = Path(render(source.relative_to(root).as_posix(), values))
            if destination.is_absolute() or ".." in destination.parts or destination in files:
                raise ValueError(f"Çıktı yolu geçersiz veya yineleniyor: {destination}")
            files[destination] = render(source.read_text(encoding="utf-8"), values)
    return files


def initialize_git(target, files):
    git = shutil.which("git")
    if git is None:
        print("Git bulunamadı. Proje dosyaları hazır.")
        return

    try:
        # Üst deponun çalışma ağacı, indeksi veya nesne dizini kullanılmasın.
        local_vars = subprocess.check_output([git, "rev-parse", "--local-env-vars"], text=True)
        env = os.environ.copy()
        for key in local_vars.splitlines():
            env.pop(key, None)

        def run(*args, quiet=False):
            return subprocess.run(
                [git, "-c", f"core.hooksPath={os.devnull}", *args],
                cwd=target, env=env, check=False, capture_output=quiet,
            ).returncode == 0

        if not run("init", "-q", "--template="):
            print("Git deposu başlatılamadı. Proje dosyaları hazır.")
        elif not all(
            run("var", identity, quiet=True)
            for identity in ("GIT_AUTHOR_IDENT", "GIT_COMMITTER_IDENT")
        ):
            print("Git kimliği eksik. Depo başlatıldı, ilk commit bekliyor.")
        elif run("add", "-f", "--", *sorted(files)) and run(
            "commit", "-qm", "chore: proje iskeletini oluştur"
        ):
            print("Git deposu ve ilk commit hazır.")
        else:
            print("İlk commit oluşturulamadı. Proje dosyaları hazır.")
    except (OSError, subprocess.SubprocessError) as error:
        print(f"Git işlemi tamamlanamadı: {error}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ad", required=True)
    parser.add_argument("--dil", choices=COMMANDS, required=True)
    parser.add_argument("--tur", choices=("bireysel", "takim"), required=True)
    parser.add_argument("--ders")
    parser.add_argument("--hedef", type=Path)
    parser.add_argument("--git", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--kuru", action="store_true")
    args = parser.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.ad):
        parser.error("Proje adı yalnızca ASCII harf, rakam, tire ve alt çizgi içerebilir.")
    if args.ders and args.ders.splitlines() != [args.ders]:
        parser.error("Ders adı tek satır olmalıdır.")

    target = args.hedef if args.hedef is not None else Path(args.ad)
    try:
        if target.is_symlink() or (target.exists() and (
            not target.is_dir() or any(target.iterdir())
        )):
            parser.error(f"Hedef yeni veya boş bir dizin olmalıdır: {target}")
        target = target.resolve()
        files = plan_files(args)
        if args.kuru:
            print(f"Hedef: {target}")
            for path in sorted(files):
                print(path.as_posix())
            return

        target.mkdir(parents=True, exist_ok=True)
        if any(target.iterdir()):
            parser.error(f"Hedef artık boş değil: {target}")
        for path, content in files.items():
            output = target / path
            if not output.resolve().is_relative_to(target):
                raise ValueError(f"Çıktı hedefin dışında: {path}")
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(content)
        print(f"{len(files)} dosya oluşturuldu: {target}", flush=True)
        if args.git:
            initialize_git(target, files)
    except (ValueError, OSError, KeyError, RuntimeError) as error:
        parser.exit(1, f"Hata: {error}\n")


if __name__ == "__main__":
    main()
