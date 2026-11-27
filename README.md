# Öğrenci Proje Başlangıç Paketi

Bu Claude Code eklentisi, üniversite ders projeleri için Python, JavaScript, Java ve C iskeleti oluşturur. Her projede Türkçe README, örnek kod ve test, lint veya biçim ayarları, `.gitignore`, `.editorconfig` ve `CLAUDE.md` bulunur. Takım projelerine ayrıca katkı rehberi, GitHub şablonları, görev tablosu ve test iş akışı eklenir.

## Tanıtım sayfası

[Kurulum adımları, Claude Code olmadan kullanım ve ücretsiz Claude hesabıyla öğrenme modu](https://oguzhankaygin.github.io/ogrenci-proje-baslangic/).

## Kurulum

Claude Code oturumunda:

```text
/plugin marketplace add oguzhankaygin/ogrenci-proje-baslangic
/plugin install ogrenci-proje@ogrenci-proje-baslangic
```

Depoyu yerelden denemek için proje kökünde `claude --plugin-dir ./plugin` çalıştırın. Eklentinin komutları Claude Code'da eklenti adıyla çağrılır. [Claude Code eklenti belgeleri](https://code.claude.com/docs/en/plugins)

| Komut | İşlev |
| --- | --- |
| `/ogrenci-proje:proje-baslat [ad]` | Ders projesi iskeleti oluşturur ve testi çalıştırır. |
| `/ogrenci-proje:ipucu [konu]` | Öğrenme modunda sıradaki tek ipucunu verir. |
| `/ogrenci-proje:teslim-kontrol` | Testleri, belgeleri, TODO'ları ve Git kayıtlarını denetler. |

## Örnek oturum

```text
Öğrenci: /ogrenci-proje:proje-baslat veri-yapilari
Claude: Hangi dil? Bireysel mi, takım projesi mi? Dersin kodu ve adı nedir?
Öğrenci: Python, takım, BLM203 Veri Yapıları.
Claude: veri-yapilari/ oluşturuldu. Örnek unittest testi geçti.
       README'deki amacı yazın ve docs/gorev-dagilimi.md tablosunu doldurun.
```

## Claude olmadan kullanım

Üretici Python 3.10+ ve standart kütüphaneyle çalışır. Git isteğe bağlıdır.

```sh
python3 plugin/skills/proje-baslat/scripts/baslat.py \
  --ad veri-yapilari --dil python --tur takim --ders "BLM203 Veri Yapıları"
```

`--dil` için `python`, `javascript`, `java` veya `c`, `--tur` için `bireysel` veya `takim` seçin. Varsayılan hedef proje adıyla aynı adlı alt dizindir. `--hedef DIZIN` ile yeni ya da boş bir dizin seçin. Proje adında ASCII harf, rakam, tire ve alt çizgi kullanılabilir.

`--kuru` dosya listesini gösterir. Git varsa varsayılan olarak depo başlatılır ve Git kimliği uygunsa ilk commit oluşturulur. Git adımlarını atlamak için `--no-git` kullanın. Üretimden sonra proje README'sindeki kurulum, çalıştırma ve test adımlarını izleyin.

## Öğrenme modu

Claude, öğrencinin denemesinden hareket eder. Kavramdan başlayıp yaklaşım, sözde kod ve kısmi kodla ilerler. Her adımda öğrenciden gerekçeyi veya bir örnekte beklenen sonucu açıklamasını ister. Doğrudan çözüm için öğrencinin açık isteği ve dersin yapay zekâ politikasının izni gerekir. Projeye özgü öğrenme kurallarını kapatmak için üretilen `CLAUDE.md` dosyasındaki **Öğrenme modu** bölümünü kaldırabilirsiniz.

## Etkileşimli konu sayfası

Claude Code'da `/ogrenci-proje:konu-sayfasi Bayes teoremi` komutunu çalıştırın. Claude, tarayıcıda çevrimdışı açabileceğiniz tek bir HTML dosyası oluşturur.

Ücretsiz claude.ai hesabınızda aşağıdaki istemi kopyalayın. Başka bir konu için Bayes örneğini uyarlayabilirsiniz.

```text
Bayes teoremini öğrenmek için çevrimdışı çalışan tek bir HTML artifact oluştur. Önce tek mesajda dersimi ve seviyemi, işlemek istediğim alt konuyu, zaten bildiklerimi ve varsa paylaşabileceğim ders notunu veya kitap bölümünü sor. Yanıt gelmezse varsayımlarını yaz ve devam et. Not veya kitap metni verirsem yalnızca o metne dayan, eksik bilgiyi belirt.

Sayfada 3–5 öğrenme hedefi, yanıtı gizli bir “Önce tahmin et” sorusu, adım adım anlatım, olasılıkları değiştirince sonucu güncelleyen bir etkileşim, çözümlü örnek, her seçeneği açıklayan beş test sorusu, sık yapılan hatalar ve “Nereden doğrulamalı” bölümü olsun. Kaynak uydurma. Bir ödev sorusu verirsem farklı sayılarla benzer bir örnek kullan ve dersin yapay zekâ politikasını hatırlat.

Dosyayı konu-bayes-teoremi.html olarak adlandır. CSS ve JavaScript dosyanın içinde olsun. Harici kütüphane, CDN, font ve görsel kullanma. Öğrenci girdisini DOM'a textContent ile ekle. Formülleri düz metin, Unicode veya sub/sup ile yaz. Mobil uyum, açık/koyu tema, azaltılmış hareket, klavye erişimi, görünür odak, form etiketleri, canlı geri bildirim ve WCAG AA kontrastı sağla. Teslimden önce örnek hesabı, test yanıtlarını ve çevrimdışı çalışmayı kontrol et.
```

## Katkı

Dil şablonları `plugin/skills/proje-baslat/templates/` altında yer alır. Şablon değişikliklerinin ardından üretici testlerini çalıştırın ve PR'da hangi dilde hangi davranışı doğruladığınızı belirtin.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Paket MIT lisanslıdır. Ayrıntılar için [LICENSE](LICENSE) dosyasına bakın.
