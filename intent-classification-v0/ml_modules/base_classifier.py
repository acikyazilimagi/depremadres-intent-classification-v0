from abc import ABC, abstractmethod
from typing import List


class BaseClassifier(ABC):

    @abstractmethod
    def classify(self, text: str) -> List[str]:
        raise NotImplementedError
