import json
import requests
import os
import time
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv(".env")

API_TOKEN = os.getenv("HF_HUB_TOKEN")

headers = {"Authorization": f"Bearer {API_TOKEN}"}

API_URL = "https://api-inference.huggingface.co/models/emrecan/convbert-base-turkish-mc4-cased-allnli_tr"

def query(payload: Dict) -> Optional[Dict]:
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)

    # Check status code
    if response.status_code != 200:
        print(f"Query: {payload} failed to run by returning code of {response.status_code}. Response: {response.text} ")
        print("Trying again in 10 seconds...")
        # Wait 10 seconds and try again
        time.sleep(10)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        if response.status_code != 200:
            return None

    return response.json()


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
