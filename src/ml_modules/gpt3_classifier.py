from typing import List

from src.ml_modules.base_classifier import BaseClassifier


class GPT3Classifier(BaseClassifier):

    def classify(self, text: str) -> List[str]:
        raise NotImplementedError
