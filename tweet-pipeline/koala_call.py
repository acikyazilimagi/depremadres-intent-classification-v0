import requests
import json


def get_label_and_adres(tweet_text):
    """
    This function is used to call the Koala API and get the output as label and adres.
    Koala API is COMPLETELY FREE TO USE AND DOES NOT REQUIRE ANY AUTHENTICATION.
    THE RESPONSE TIME IS AROUND 4-6 SECONDS.
    :param tweet_text: The tweet text that is going to be used as input for the Koala API.
    :return: 
        label -> list : The label that is predicted by the Koala API. 
        adres -> str : The address that is predicted by the Koala API. 
    """

    prompt = """
        Generate keyword content and adress. You are highly intelligent and accurate sentimental analyst. From
        plain text input and especially from emergency text that carries address and/or demand information, your inputs can be text
        of arbitrary size written in Turkish considering the tweets from Turkey, the label has to be one of the following:
        ['YEMEK', 'SU', 'ELEKTRONIK', 'GIYSI', 'BARINMA', 'LOJISTIK', 'KURTARMA', 'SAGLIK', 'YAGMALAMA', 'TUVALET', 'ALAKASIZ'].
        'ALAKASIZ' means the tweet is not related any of the other labels. ONLY AND ONLY give the output as one of the labels from the 
        given list without providing any further information and say only '' (empty string) if you're not able to extract the information. Note that the
        labels are not mutually exclusive, a tweet can have multiple labels. Lastly, parse the tweet to extract the address information and
        save it as a dictionary with the key 'address' and the value as the address as 'adres': 'address information'. If the address is not
        found in the tweet, then the value should be an empty string.
        Example:
            Input: #depremadres #deprem  Göçükten ses gelmediği için vinçler geri gitmis arkadaşlarımız enkaz altında lütfen artık çıkarılsınlar lütfen  ZENGİNLER MAHALLESİ KIRK ASIRLIK TÜRK YURDU CADDESİ (2.YILDIZ APARTMANI) BİNA NO :26 KAPI NO:8 KAT:4 ANTAKYA/ HATAY https://t.co/81JbSYUMEw
            Output: {'label': ['KURTARMA'], 'adres': 'Zenginler Mahallesi Kırk Asırlık Tğrk Yurdu Caddesı (2. Yıldız Apartmanı) Bina No:26 Kapı No:8 Kat:4 Antakya/Hatay'}
        Question:
            Input: 
        """ + tweet_text + "\n Output: "

    data = {"input": prompt}
    data = json.dumps(data)

    headers = {"Content-Type": "application/json"}

    response = requests.post('https://koala.sh/api/gpt/', headers=headers, data=data)
    response = json.loads(response.text)

    output = response['output']
    output = output.replace("'", '"')
    output = json.loads(output)

    label = output['label']
    label = list(label)
    adres = output['adres']

    return label, adres


# Sample use case
# tweet = 'İletişim: Alperen Kurt - 5375590370 Adres: Gaziantep sevindi köyü Mesaj: köy evinde kalıyoruz elektrikli soba ihtiyacımız var 20-25 kişiyiz https://t.co/v6ZteOPatj @afadbaskanlik @akut_dernegi @ahbap @haluklevent #depremAdres'
# label, adres = get_tweet(tweet)
# return:
#     label:  ['ELEKTRONIK', 'YEMEK', 'BARINMA'] -> <class 'list'>
#     adres:  Gaziantep Sevindi Köyü -> <class 'str'>

# Uncomment the following lines to test the function
# tweet = 'İletişim: Alperen Kurt - 5375590370 Adres: Gaziantep sevindi köyü Mesaj: köy evinde kalıyoruz elektrikli soba ihtiyacımız var 20-25 kişiyiz https://t.co/v6ZteOPatj @afadbaskanlik @akut_dernegi @ahbap @haluklevent #depremAdres'
# print(get_label_and_adres(tweet))
