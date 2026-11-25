---
description: "Teslimden önce testleri, belgeleri ve Git kayıtlarını denetle."
argument-hint: ""
---

Proje kökünde, dosyaları düzenlemeden aşağıdaki kontrolleri yap:

1. `CLAUDE.md` veya README'deki proje test komutunu çalıştır. Çıkış durumunu ve özeti kaydet.
2. README'yi oku ve amaç, kurulum, çalıştırma, test, ekip, lisans ve kaynak bilgilerini kontrol et. `rg -l 'TODO|FIXME' --glob '!.git/**' --glob '!.github/**' --glob '!.env*' .` ile açık iş içeren dosyaları bul ve teslimi etkileyen maddeleri incele. `rg` yoksa proje dosyalarını başka bir mevcut araçla tara.
3. Git varsa `git status --short`, `git ls-files` ve `git log --all --full-history --name-only --format= --` ile indeksi ve erişilebilen geçmişteki dosya adlarını incele. `.env` ve `.env.*` dosyası ara. Sahte değerli `.env.example` dosyalarını ayrıca değerlendir. `git grep -I -i -l -E --cached` ve `git log --all -i -G ... --name-only --format=` ile özel anahtar başlıkları ve açık metin anahtar, parola veya belirteç atamalarını ara. Dosya adlarını raporla ve gizli değerleri görüntüleme. Git yoksa veya henüz commit oluşmadıysa geçmişin durumunu belirt. Basit desen taramasının sınırını söyle.
4. Lisans kararını, dış kaynaklara verilen atıfları ve varsa dersin yapay zekâ kullanımı açıklamasını denetle.

Türkçe olarak her kontrolün sonucunu, çalıştırdığın komutları ve gerekiyorsa dosya yollarını ver. Çalıştırılamayan kontrolleri ve nedenlerini belirt.
