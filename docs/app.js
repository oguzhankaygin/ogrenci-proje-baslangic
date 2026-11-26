"use strict";

const ISTEM = `Bir üniversite ders projesinde öğrenme modunda yardımcı ol.
Kurallar:
- Doğrudan tam çözüm verme. Önce kavramı, sonra yaklaşımı, sonra sözde kodu, en son kısmi kodu öner.
- Her adımda benden bir deneme ya da gerekçe iste; denememden hareket et.
- Önce proje iskeletini (klasör yapısı, README başlıkları, bir örnek test) öner.
- Tam çözümü yalnızca açıkça istersem ve dersin yapay zekâ politikası izin veriyorsa ver.
Projem: `;

function bildir(metin) {
  document.getElementById("durum").textContent = metin;
}

async function kopyala(metin) {
  try {
    await navigator.clipboard.writeText(metin);
    return true;
  } catch {
    return false;
  }
}

for (const dugme of document.querySelectorAll("[data-kopyala]")) {
  dugme.addEventListener("click", async () => {
    const tamam = await kopyala(document.getElementById(dugme.dataset.kopyala).textContent);
    dugme.textContent = tamam ? "Kopyalandı" : "Kopyalanamadı, elle seçin";
    setTimeout(() => { dugme.textContent = "Kopyala"; }, 2000);
  });
}

document.getElementById("claude-ac").addEventListener("click", async () => {
  const konu = document.getElementById("konu").value.trim() || "[konuyu ve dili yaz]";
  const tamam = await kopyala(ISTEM + konu);
  window.open("https://claude.ai/new", "_blank", "noopener");
  bildir(tamam ? "İstem kopyalandı. Claude'da yapıştırıp gönderin." : "Kopyalanamadı; tarayıcı izni verin.");
});
