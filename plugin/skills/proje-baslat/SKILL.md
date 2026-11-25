---
name: "proje-baslat"
description: "Yeni ders veya takım projesi başlatmak için kullan. Tetikleyiciler: proje başlat, ders projesi oluştur, start a project, scaffold a student project."
---

# Proje başlat

Öğrencinin verdiği bilgileri kullan. Eksik olanları tek mesajda kısa sorularla öğren:

1. Projenin adı ne? ASCII harf, rakam, tire ve alt çizgi kullanılabilir.
2. Hangi dil kullanılacak? Python, JavaScript, Java veya C.
3. Proje bireysel mi, takım projesi mi?
4. Dersin kodu ve adı nedir? Bu bilgi isteğe bağlıdır.

Komutla çağrıldıysan ve `$ARGUMENTS` içinde bir ad verildiyse onu kullan. Varsayılan hedef çalışma dizinindeki proje adıyla aynı adlı alt dizindir. Öğrenci bir hedef veya Git tercihi belirtirse ona göre ilgili bayrağı geçir.

```sh
python3 "${CLAUDE_PLUGIN_ROOT}/skills/proje-baslat/scripts/baslat.py" \
  --ad=veri-yapilari --dil python --tur takim --ders="BLM203 Veri Yapıları"
```

Örnekteki değerleri öğrencinin yanıtlarıyla değiştir. Değerleri ayrı kabuk argümanları olarak güvenli biçimde alıntıla. Ders bilgisi yoksa `--ders` bayrağını atla. Betik hedefi reddederse hatayı açıkla ve farklı bir hedef iste.

Üretim başarılıysa proje dizininde `CLAUDE.md` içindeki test komutunu çalıştır. Eksik araç veya bağımlılık varsa testin çalışmadığını ve hangi gereksinimin eksik olduğunu belirt. Türkçe olarak hedef dizini, test sonucunu, Git durumunu ve ilk adımı özetle. İlk adımda README'deki TODO alanlarını, takım projesinde görev dağılımını da hatırlat.
