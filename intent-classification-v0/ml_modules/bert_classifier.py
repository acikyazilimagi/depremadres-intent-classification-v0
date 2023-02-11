import logging
import os
from typing import List

import requests
from dotenv import load_dotenv
from ml_modules.base_classifier import BaseClassifier

load_dotenv(".env")

# Add logging.
logging.basicConfig(level=logging.INFO)


class BertClassifier(BaseClassifier):
    """
    BERT based classifier to uses huggingface inference API to classify tweets.

    Example usage:
    >>> classifier = BertClassifier()
    >>> classifier.classify("Kırıkkale'de deprem oldu.")
    ["KURTARMA"]
    """

    def __init__(self, classification_threshold=0.5):
        # The score threshold to deem a label as positive.
        self.classification_threshold = classification_threshold

        API_TOKEN = os.getenv("HF_HUB_TOKEN")
        self.headers = {"Authorization": f"Bearer {API_TOKEN}"}

        model_name = "deprem-ml/multilabel_earthquake_tweet_intent_bert_base_turkish_cased"
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"

    def __query(self, text):
        response = requests.post(
            self.api_url, headers=self.headers, json={"inputs": text})

        # raise HTTPException if status code != 200
        response.raise_for_status()
        return response.json()

    def all_intents(self):
        """
        Returns list of all possible intents this classifier can classify.
        """
        return ["ALAKASIZ", "KURTARMA", "BARINMA", "SAGLIK", "LOJISTIK", "SU",
                "YAGMA", "YEMEK", "GIYSI", "ELEKTRONIK"]

    @property
    def none_label(self):
        return "ALAKASIZ"

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
            labels = [l_and_s["label"].upper()
                      for l_and_s in labels_and_scores
                      if l_and_s["score"] > self.classification_threshold
                      ]

        # if ALAKASIZ and other category survive after threshold filter,
        # remove ALAKASIZ
        if self.none_label in labels and len(labels) > 1:
            labels.pop(self.none_label)

        # Don't return set, as it will lose ordering.
        return labels


# If name main
if __name__ == "__main__":
    text = "Kırıkkale'de deprem oldu."
    labels = BertClassifier().classify(text)
    print(labels)
