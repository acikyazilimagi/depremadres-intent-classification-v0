from unittest import TestCase

from ml_modules.bert_classifier import BertClassifier


class TestBERClassifier(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.classifier = BertClassifier()

    def test_classify_base_case(self):
        result = self.classifier.classify("")
        assert isinstance(result, (set, list))
        assert len(result) == 0

    def test_classify_base(self):
        result = self.classifier.classify(
            "Enkaz altındayım lütfen yardım edin")
        assert isinstance(result, (set, list))
        assert len(result) > 0
        for el in result:
            assert isinstance(el, str)
