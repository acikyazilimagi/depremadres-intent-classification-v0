import json
import requests
import os 
from dotenv import load_dotenv

load_dotenv(".env")

API_TOKEN = os.getenv("HF_HUB_TOKEN")
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/emrecan/convbert-base-turkish-mc4-cased-allnli_tr"
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


def batch_query(data, candidate_labels):
    """
    List ya da text'leri iceren herhangi bir iterable alir.

    Parameter
    ---------
    data : Iterable
        Text'leri iceren iterable.
    candidate_labels : List
        Siniflandirilmak istenen topic'ler.

    Returns
    -------
    outputs
        JSON output listesi: JSON'un key'ler sequence (asil input), labels (tahmin edilen siniflar)
        ve scores (siniflarin kac olasilikla tahmin edildigi)
    # TODO: olasiliklara gore fallback mekanizmasi yazilacak.
    """
    outputs = []
    if not candidate_labels:
        candidate_labels = ["battaniye", "yemek", "göçük"]
    for tweet in data:
        outputs.append(query(
            {
                "inputs": tweet,
                "parameters": {"candidate_labels": candidate_labels},
            }))
    return outputs
