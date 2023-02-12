from unittest import TestCase
from unittest.mock import Mock, patch

from src.ml_modules.bert_classifier import BertClassifier
from src.ml_modules.rule_based_clustering import RuleBasedClassifier


class TestClassifiers(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.classifiers = [BertClassifier(), RuleBasedClassifier()]

    def test_classify_empty_case(self):
        with patch('src.ml_modules.bert_classifier.requests.post') as mock_post:
            mock_post.return_value = Mock()
            mock_post.return_value.json.return_value = [
                [
                    {
                        "label": "foo",
                        "score": 0.0,
                    },
                    {
                        "label": "bar",
                        "score": 0.0,
                    },
                ]
            ]
            mock_post.return_value.status_code = 200

            for classifier in self.classifiers:
                result = classifier.classify("")
                assert isinstance(result, list)
                assert len(result) == 0

    def test_classify_base(self):
        with patch('src.ml_modules.bert_classifier.requests.post') as mock_post:
            mock_post.return_value = Mock()
            mock_post.return_value.json.return_value = [
                [
                    {
                        "label": "foo",
                        "score": 0.7,
                    },
                    {
                        "label": "bar",
                        "score": 0.4,
                    },
                ]
            ]
            mock_post.return_value.status_code = 200

            for classifier in self.classifiers:
                result = classifier.classify(
                    "Enkaz altındayım lütfen yardım edin")
                assert isinstance(result, list)
                assert len(result) > 0
                for el in result:
                    assert isinstance(el, str)
