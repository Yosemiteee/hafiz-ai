# Hafız AI

Hafız AI, hafızların Kur'an'ı ezberden doğru ve akıcı okumalarına yardımcı olmak
üzere tasarlanmış bir yapay zekâ projesidir. Bu depoda, metin tabanlı ilk
prototip yer alıyor. Sistem, öğrencinin okumasını referans metin ile
karşılaştırıp doğruluk oranını hesaplar, eksik veya fazla kelimeleri tespit eder
ve telaffuz skorları sağlanırsa hedefli geri bildirim üretir.

## Özellikler

- **Metin normalizasyonu:** Arapça harfler korunurken hareke ve noktalama gibi
  okumayı etkilemeyen işaretler kaldırılır.
- **Kelime tabanlı karşılaştırma:** Eksik, fazla ve yanlış sıralanan kelimeler
  ayrıştırılır.
- **Telaffuz geri bildirimi:** İsteğe bağlı olarak sağlanan kelime başına skor
  değerlerini analiz ederek hedefli öneriler üretir.
- **CLI deneyimi:** Terminal üzerinden hızlı denemeler yapmak için hazır arayüz.

## Kurulum

Proje yalnızca Python standart kütüphanesini kullanır. Geliştirmeye başlamak
için bir sanal ortam oluşturmanız önerilir.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows için `.venv\\Scripts\\activate`
```

Ardından depo klasöründe çalışmaya başlayabilirsiniz.

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

- Ses işleme ve otomatik konuşma tanıma entegrasyonu
- Gerçek zamanlı geri bildirim ve görsel arayüz
- Ezber takibi için ilerleme raporları
