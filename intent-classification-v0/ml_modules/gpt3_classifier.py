from typing import List

from ml_modules.base_classifier import BaseClassifier


class GPT3Classifier(BaseClassifier):

    def classify(self, text: str) -> List[str]:
        raise NotImplementedError
