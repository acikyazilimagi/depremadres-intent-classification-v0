# Yeni classifier eklenmesi

1. `ml_modules` altında BaseClassifier'ı extend eden yeni sınıf yarat.
2. Eğer gerekliyse `requirements.txt`'yi ve `requirements-dev.txt`'yi güncelle.
3. `tests/ml/classifiers/test_models.py` dosyasında yeni classifier'ı importlayıp `setupClass`'ı güncelle.
4. `make test-docker` komutu ile testlerin geçtiğinden emin ol.
5. Yeni branch'ı pushla ve PR aç.

# Deprem Verisi ile Intent Classificiation

**Proje amaci**: Twitter’dan toplanan deprem alakali verilerin labellanmasi ve analizi. Su ana kadar kelime tabanli ve zero-shot classification modeli kullanilarak intent classification yapildi. Onumuzdeki amacimiz veri takimlarinin yardimiyla verisetleri olusturup tweetleri ilgili yardim birimlerine ulastirmak amacli kumelemek. Ornegin: yemek ihtiyaci oldugunu belirten bir tweetin enkaz icin degil de gida transferi saglayacak ekiplerle paylasilmasi icin duzenlenmesi.

#depremadres data Trello'da mevcut: 130k tweet data

**Yapilmasi gerekenler**

1. Depremle ilgili elimizde olan verilerin analiz edilmesi.

   1. #depremadres hashtaginden 2232 tweet var elimizde.
   2. deprem alakali 130k tweet var elimizde.
   3. yapilabilecek preprocessing gelistirmeleri.
   4. veriyi en iyi represent edecek label listesinin olusturulmasi.
   5. data exploration

2. yeni toplanabilecek verilerin planlanmasi.
3. veri takimiyla iletisime gecilip toplanmis verilerin annotation isleminin yapilmasi.
4. supervised classification probleminin tasarlanmasi.

   1. elimizdeki tweet yardim isteyen tweet vs ornegin siyasi tweet mi.
   2. yardim tweetlerinin hangi contextte yardim istedigi: enkaz yardim, gida yardim, ilac yardim, gibi.
   3. daha fazla model mumkun, veri analizleri dogrultusunda neler gelistirilebilirse deneyebilirsiniz.

5. problemin etrafinda gelistirilebilecek modellerin belirlenmesi.
6. modellerin training ve testing gelistirmelerinin yapilmasi.
7. sonuclarin analizinin yapilmasi.
8. pm ekibiyle iletisime gecilip modellerin ne yonde ise yarayabileceginin ve entegrasyonunun planlanmasi.
