# Hafız AI

Hafız AI, hafızların Kur'an'ı ezberden doğru ve akıcı okumalarına yardımcı olmak
üzere tasarlanmış bir yapay zekâ koçudur. Bu depo; gerçek zamanlı web arayüzü,
ses tanıma entegrasyonu için tarayıcı tarafı hazırlıkları ve metin tabanlı
analiz motorunu içerir. Sistem, öğrencinin okumasını referans metin ile
karşılaştırıp doğruluk oranını hesaplar, eksik veya fazla kelimeleri tespit eder
ve telaffuz skorları sağlanırsa hedefli geri bildirim üretir.

## Başlıca Özellikler

- **Modern web arayüzü:** Tarayıcıda mikrofon izni verildiğinde Web Speech API
  üzerinden canlı transkript alır, eş zamanlı geri bildirim panosu sunar.
- **Hazır referans pasajlar:** Fâtiha ve İhlâs sureleri, Arapça metin,
  transliterasyon ve Türkçe meal ile birlikte gelir.
- **Metin normalizasyonu:** Arapça harfler korunurken hareke ve noktalama gibi
  okumayı etkilemeyen işaretler kaldırılır.
- **Kelime tabanlı karşılaştırma:** Eksik, fazla ve yanlış sıralanan kelimeler
  ayrıştırılır.
- **Telaffuz geri bildirimi:** İsteğe bağlı olarak sağlanan kelime başına skor
  değerlerini analiz ederek hedefli öneriler üretir.
- **CLI deneyimi:** Terminal üzerinden hızlı denemeler yapmak için hazır arayüz.

## Kurulum

Bir sanal ortam oluşturup gerekli bağımlılıkları yükleyin:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows için `.venv\Scripts\activate`
```

Projede yalnızca Python standart kütüphanesi kullanıldığı için ek bağımlılık
yüklemenize gerek yoktur. Ardından depo klasöründe çalışmaya
başlayabilirsiniz.

## Web uygulamasını başlatma

Geliştirme sunucusunu başlatmak için aşağıdaki komutu kullanın:

```bash
python -m hafiz_ai.web.app
```

Komut sunucuyu varsayılan olarak `http://127.0.0.1:8000` adresinde açar. Açılan
sayfada aşağıdaki deneyim sağlanır:

1. Çalışmak istediğiniz pasajı seçersiniz.
2. **Kaydı Başlat** düğmesi ile tarayıcınıza mikrofon izni verirsiniz.
3. Web Speech API okumanızı canlı olarak metne çevirir, Hafız AI ise sonucu
   referans ile karşılaştırır.
4. Geri bildirim panelinde doğruluk oranı, eksik/fazla kelimeler ve öneriler
   gerçek zamanlı olarak güncellenir.

> Not: Web Speech API tarayıcıya özeldir. Eğer desteklenmiyorsa, arayüzdeki
> metin alanına kendi transkriptinizi yapıştırarak yine analiz alabilirsiniz.

Diğer cihazlardan erişmek isterseniz sunucuyu `0.0.0.0` adresiyle
başlatabilirsiniz:

```bash
python -m hafiz_ai.web.app --host 0.0.0.0 --port 8000
```

## Komut satırı aracı

`hafiz.py` betiği CLI arayüzünü çalıştırır. Beklenen metin ve öğrencinin
okumasını doğrudan argüman olarak verebilir veya metinleri dosyadan
okuyabilirsiniz.

```bash
python hafiz.py \
  --expected "بسم الله الرحمن الرحيم" \
  --transcript "بسم الله الرحيم" \
  --pronunciation-score "الرحيم=0.80"
```

Alternatif olarak dosya tabanlı kullanım:

```bash
python hafiz.py --expected-file data/expected.txt --transcript-file data/student.txt
```

Çıktıda doğruluk skoru, eşleşen/eksik/fazla kelimeler ve otomatik öneriler
listelenir.

## Testler

Birim testleri `pytest` ile çalıştırabilirsiniz.

```bash
pip install pytest
pytest
```

## Yol Haritası

- Tarayıcıdan gelen ses akışını sunucu tarafında işleyip kelime bazlı telaffuz
  skorları üretmek
- Kullanıcı bazlı oturumlar ve ilerleme raporları
- Mobil uygulamalar için ortak değerlendirme API'leri
