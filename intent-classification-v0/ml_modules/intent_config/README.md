# Intent config

Burada classify edilecek intentlerin konfigurasyonunu tutuyoruz.

Bunu `rule_based_clustering.py` deki `RuleBasedClassifier` okuyup dinamik olarak intent - keyword eslesmesini olusturuyor.

Detayli kullanim icin `RuleBasedClassifier` pydoc a bakin.

Konfigurasyon dosyalari soyle:

   - **dosya ismi**: <INTENT>.txt
   - **dosya icerigi**: o intente ait keywordlerin line separated listesi

### Ornek
Dosya adi:

```
YEMEK-SU.txt
```

icerik:

``` 
gida talebi
gida
yemek
su
corba
...
```
