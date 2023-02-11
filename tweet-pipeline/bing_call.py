import requests
import re

url = "https://gpt.song.work/chat"

tweet = 'İletişim: Alperen Kurt - 5375590370 Adres: Gaziantep sevindi köyü Mesaj: köy evinde kalıyoruz elektrikli soba ihtiyacımız var 20-25 kişiyiz https://t.co/v6ZteOPatj @afadbaskanlik @akut_dernegi @ahbap @haluklevent #depremAdres'
tweet2 = '"İletişim: Fatma - 5454948636 Adres: Şanlıurfa 2.organize sanayi bölgesi fabrikaların olduğu bölge karaköprü  merkez Mesaj: Şanlıurfada camide kalıyoruz hijyen paketleri kadınlar için,çocuk bezi mama ihtiyaç https://t.co/v6ZteOPatj @afadbaskanlik @ahbap @haluklevent #depremAdres"'
tweet3 = '"İletişim: Özgür sezen - 5055986960 Adres: Hatay Defne Çekmece mahallesi 41/2  Mesaj: bebek bezi mama su hasta bezi yorgan battaniye fener ve kalın kıyafetler https://t.co/tV5WR3R5Wn @afadbaskanlik @akut_dernegi @ahbap @haluklevent #depremAdres"'
tweet4 = '"İletişim: Muhammet çobanpınar - 05456375898 Adres: Kahramanmaraş Avşin avşin yeşilyurt mahalesi kemalertekin caddesi hastane üstü mobese karşısı Mesaj: Gıda ve battaniye ihtiyaçları var. @afadbaskanlik @akut_dernegi @ahbap @haluklevent #depremAdres"'
tweet5 = '"@Darkwebhaber #depremadres adres: Atatürk Caddesi 1 Nolu Sağlık Ocağının 100 m doğusu Gencebay Kasap- Fırının arkası, Samandağ/Hatay telefonla az önce konuşuldu yaşam belirtisi mevcut gelen giden henüz olmamış sesler gelmekte  0537 773 6787 0537 329 6809 https://t.co/4T74jCkKCk"'

tweet_list = [tweet, tweet2, tweet3, tweet4, tweet5]

for tweet in tweet_list:
        prompt = """
                Generate keyword content. You are highly intelligent and accurate intent classifier from
                plain text input and especially from emergency text that carries address and/or demand information, your inputs can be text
                of arbitrary size written in Turkish considering the tweets from Turkey, the label has to be one of the following:
                ['YEMEK', 'SU', 'ELEKTRONIK', 'GIYSI', 'BARINMA', 'LOJISTIK', 'KURTARMA', 'SAGLIK', 'YAGMALAMA', 'TUVALET', 'ALAKASIZ'].
                'ALAKASIZ' means the tweet is not related any of the other labels. ONLY AND ONLY give the output as one of the labels from the 
                given list without providing any further information and say only 'None' if you're not able to extract the information. Note that the
                labels are not mutually exclusive, a tweet can have multiple labels. Lastly, parse the tweet to extract the address information and
                save it as a dictionary with the key 'address' and the value as the address as {'adres': 'address information'}. If the address is not
                found in the tweet, then the value should be None.
                Example:
                        Input: #depremadres #deprem  Göçükten ses gelmediği için vinçler geri gitmis arkadaşlarımız enkaz altında lütfen artık çıkarılsınlar lütfen  ZENGİNLER MAHALLESİ KIRK ASIRLIK TÜRK YURDU CADDESİ (2.YILDIZ APARTMANI) BİNA NO :26 KAPI NO:8 KAT:4 ANTAKYA/ HATAY https://t.co/81JbSYUMEw
                        Bing: ['KURTARMA'], {'adres': 'Zenginler Mahallesi Kırk Asırlık Tğrk Yurdu Caddesı (2. Yıldız Apartmanı) Bina No:26 Kapı No:8 Kat:4 Antakya/Hatay'}
                Question:
                        Input: 
                """ + tweet + " Output: "

        data = {"prompt": prompt}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, json=data, headers=headers)
        label = response.text.split("{")[0]
        adres = response.text.split("{")[1].split("}")[0]
        # adres = response.text.split("{")[1].split("}")[0]
        # print(label)
        print(label, adres)