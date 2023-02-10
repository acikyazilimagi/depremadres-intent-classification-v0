from dotenv import load_dotenv
from typing import Dict, Tuple, Set, Optional, List, Union
import logging
import os
import requests

load_dotenv(".env")

# Add logging.
logging.basicConfig(level=logging.INFO)

API_URL = "https://api-inference.huggingface.co/models/deprem-ml/multilabel_earthquake_tweet_intent_bert_base_turkish_cased"
API_TOKEN = os.getenv("HF_HUB_TOKEN")

headers = {"Authorization": f"Bearer {API_TOKEN}"}

# The score threshold to deem a label as positive.
CLASSIFICATION_THRESHOLD = 0.5


class BertClassifier(object):
    """
    BERT based classifier to uses huggingface inference API to classify tweets.

    Example usage:
    >>> classifier = BertClassifier()
    >>> classifier.classify("Kırıkkale'de deprem oldu.")
    ["KURTARMA"]
    """

    def __init__(self, classification_threshold=CLASSIFICATION_THRESHOLD):
        self.classification_threshold = classification_threshold

    def __query(self, text):

        response = requests.post(
            API_URL, headers=headers, json={"inputs": text})
        return response.json()

    def all_intents(self):
        """Returns list of all possible intents this classifier can classify."""
        return ["ALAKASIZ", "KURTARMA", "BARINMA", "SAGLIK", "LOJISTIK", "SU", "YAGMA", "YEMEK", "GIYSI", "ELEKTRONIK"]


    def classify(self, text: str) -> List[str]:
        """
        Check if the given text contains any of the keywords of any intent.
        Args:
            text: The text to check.

        Returns:
            List of labels of the tweet, if any, ordered by score.
        """
        response = self.__query(text)
        logging.info(f"Response: {response}")
        labels = []

        if response:
            # Labels are returned as a list of lists.
            labels_and_scores = response[0]
            labels = [l_and_s["label"].upper() for l_and_s in labels_and_scores if l_and_s["score"] > self.classification_threshold]

        # Don't return set, as it will lose ordering.
        return labels


# If name main
if __name__ == "__main__":
    text = "Kırıkkale'de deprem oldu."
    labels = BertClassifier().classify(text)
    print(labels)
