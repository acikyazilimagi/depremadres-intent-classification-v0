"""
Command line verison of the intent classification app.

Usage:
    python app_main.py --run_rule_based_classifier --run_bert_classifier -text='Yardim'
"""
import argparse

# ML modules
from ml_modules.rule_based_clustering import RuleBasedClassifier
from ml_modules.bert_classifier import BertClassifier

# Define command line arguments to control which classifiers to run.
parser = argparse.ArgumentParser()
parser.add_argument('--text', type=str)
parser.add_argument('--run_rule_based_classifier',
                    action=argparse.BooleanOptionalAction, default=True)
parser.add_argument('--run_bert_classifier',
                    action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()

# Initialize classifiers
rule_based_classifier = None
if args.run_rule_based_classifier:
    rule_based_classifier = RuleBasedClassifier()

bert_classifier = None
if args.run_bert_classifier:
    bert_classifier = BertClassifier()


def run_classifiers(text):
    intents = []

    if args.run_rule_based_classifier:
        assert rule_based_classifier
        intents.extend(rule_based_classifier.classify(text))

    if args.run_bert_classifier:
        assert bert_classifier
        intents.extend(bert_classifier.classify(text))

    # Remove duplicates.
    intents = list(set(intents))
    return intents

if __name__ == '__main__':
    intents = run_classifiers(args.text)
    print(intents)