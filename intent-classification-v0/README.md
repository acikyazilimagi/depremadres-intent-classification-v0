# deprem-intent-classification-v0

Twitterdan #depremadres hashtagine paylasilan tweetlerin intent analizi amaciyla gelistirilmis basit bir kural tabanli kodbase.

[AcikKaynak](https://github.com/acikkaynak) organizasyonun'un Discord kanalinda toplanmis bir ekiple gelistiriyoruz.

Projenin calismasi icin gereken paketler:

psycopg2, dotenv, pandas, matplotlib

Projeyi calistirmak icin:

Postgres tablosuna erisim icin credentiallar gerekli.
Projenin yonetimiyle alakasi olan birileriyle iletisime gecip Postgres erisim credentiallariyla baglanti saglanmasi gerekiyor.

```
pip install -r requirements.txt
python main.py
```


# Quality performance
Current performance on `RuleBasedClassifier` is as follows (but take the stats with a grain of salt because eval set is not perfect & doesn't have multilabels)

```
Intent: KURTARMA
==================================
KURTARMA Precision: 0.73
KURTARMA Recall: 0.87
KURTARMA F1: 0.79

Intent: YEMEK-SU
==================================
YEMEK-SU Precision: 0.44
YEMEK-SU Recall: 0.80
YEMEK-SU F1: 0.57

Intent: GIYSI
==================================
GIYSI Precision: 0.32
GIYSI Recall: 0.78
GIYSI F1: 0.45
```