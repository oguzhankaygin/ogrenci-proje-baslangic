---
name: "konu-sayfasi"
description: "Bir ders konusunu çevrimdışı çalışan etkileşimli bir HTML sayfasıyla öğret. Tetikleyiciler: konu anlat, bu konuyu etkileşimli öğret, konu sayfası, interactive explainer, explain this topic."
---

# Etkileşimli konu sayfası

Önce tek mesajda dersi ve seviyeyi, konuyu, öğrencinin zaten bildiklerini ve varsa paylaşabileceği ders notunu veya kitap bölümünü sor. Öğrencinin verdiği bilgileri yeniden sorma. Yanıt gelmezse makul varsayımlarını yaz ve devam et. Öğrenci not veya kitap metni yapıştırırsa anlatımı yalnızca bu metne dayandır. Eksik bilgiyi belirt ve kaynak uydurma.

## Sayfa sırası

1. 3–5 maddelik öğrenme hedefleri.
2. **Önce tahmin et** sorusu. Öğrenci açana kadar yanıtı ve gerekçesini gizle.
3. Kısa, adım adım kavram açıklaması.
4. En az bir etkileşim. Parametreyi değiştiren bir kaydırıcı veya girdiyle canlı hesap ya da basit SVG/canvas görselleştirmesi sun veya bir algoritmayı adım adım izlet.
5. Gerekçeleriyle çözümlü bir örnek.
6. **Kendini sına** bölümünde beş çoktan seçmeli veya kısa yanıtlı soru. Her seçenek için neden doğru veya yanlış olduğunu açıkla. Kısa yanıtta beklenen yanıtı ve öğrenme açısından gerekli düzeltmeyi göster.
7. Sık yapılan hatalar ve bu hataları önleme yolları.
8. **Nereden doğrulamalı** bölümünde ilgili ders kitabı veya not bölümünü belirt. Kaynak adı veya bölüm numarası uydurma ve emin olmadığın bilgiyi açıkça belirt.

## Teknik kurallar ve teslim

- Tek bir `konu-<kisa-ad>.html` dosyası üret. CSS ve JS dosyanın içinde olsun. Harici kütüphane, CDN, yazı tipi ve görsel kullanma.
- Öğrenci girdisini DOM'a `textContent` ile ekle. `innerHTML` yalnızca kendi yazdığın sabit metni içerebilir. Formülleri düz metin, Unicode veya basit HTML (`sub`, `sup`) ile yaz ve MathJax kullanma.
- Mobil uyumlu tasarla. `prefers-color-scheme` ile açık ve koyu temaları, `prefers-reduced-motion` ile hareket azaltma tercihini destekle. Her kontrol klavyeyle kullanılabilsin ve odak görünür olsun. Form alanlarına `label`, dinamik geri bildirime `role="status"` veya `aria-live` ekle. Her iki temada WCAG AA kontrastını sağla.
- Claude Code'da dosyayı çalışma dizinine yaz. Linux'ta `xdg-open`, macOS'ta `open` komutuna dosya adını vererek veya dosyaya çift tıklayarak tarayıcıda nasıl açılacağını göster. claude.ai'de HTML'yi artifact olarak ver.

Kavramı öğretmek için `ogrenme-modu` becerisini uygula. Öğrenci bir ödev sorusunu sayfaya çevirmek isterse aynı yapıda, farklı sayılar içeren benzer bir örnek kullan ve dersin yapay zekâ politikasını hatırlat.

## Son kontrol

- Örnek bir girdiyle hesapları ve etkileşim adımlarını sına.
- Beş sorunun doğru yanıtını ve geri bildirimini anlatımla karşılaştır.
- Dosyanın internetsiz açıldığını ve etkileşimin çalıştığını doğrula.

[İkili arama örneği](ornek/konu-ikili-arama.html)
