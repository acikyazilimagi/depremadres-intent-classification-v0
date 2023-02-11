from unittest import TestCase

from ml_modules.rule_based_clustering import RuleBasedClassifier


class TestRuleBased(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.classifier = RuleBasedClassifier()

    def test_classify_base_case(self):
        result = self.classifier.classify("")
        assert isinstance(result, list)
        assert len(result) == 0

    def test_classify_base(self):
        result = self.classifier.classify(
            "Enkaz altındayım lütfen yardım edin")
        assert isinstance(result, list)
        assert len(result) > 0
        for el in result:
            assert isinstance(el, str)
