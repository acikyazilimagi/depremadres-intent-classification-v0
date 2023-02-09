import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from typing import Dict, Tuple, Set, Optional, List, Union
from unidecode import unidecode
import os

# Directory of this file.
CUR_DIR = os.path.dirname(os.path.realpath(__file__))

# Directory that has <intent>.txt config files.
INTENT_CONFIG_DIR = os.path.join(CUR_DIR, "intent_config")


class RuleBasedClassifier(object):
    """
    Rule based classifier that uses regex patterns to classify tweets.

    It will read all the .txt files in the intent_config directory and use the
    file name as the intent name and the file contents as the keywords.

    The keywords are used to compile regex patterns that are used to classify
    the tweets.

    Example usage:
    >>> classifier = RuleBasedClassifier()
    >>> classifier.classify("Yardim edin")
    {"KURTARMA"}
    """

    def __init__(self, intent_config_dir=INTENT_CONFIG_DIR):
        self.intent_to_keywords = {}  # Will be loaded below.
        self.intent_to_patterns = {}  # Will be loaded below.
        self.__load_intent_configs(intent_config_dir)
        self.__compile_keywords_to_patterns()

    def __load_intent_configs(self, intent_config_dir):
        configs = [f for f in os.listdir(
            intent_config_dir) if f.endswith(".txt")]
        self.intent_to_config = {os.path.splitext(c)[0]: c for c in configs}
        for intent, config in self.intent_to_config.items():
            with open(os.path.join(intent_config_dir, config), "r") as f:
                self.intent_to_keywords[intent] = f.read().splitlines()

    def __compile_keywords_to_patterns(self):
        for intent, keywords in self.intent_to_keywords.items():
            self.intent_to_patterns[intent] = [re.compile(
                f"(^|\W){k}($|\W)", re.IGNORECASE) for k in keywords]

    def all_intents(self):
        """Returns list of all possible intents this classifier can classify."""
        return self.intent_to_patterns.keys()

    def classify(self, text: str) -> Set[str]:
        """
        Check if the given text contains any of the keywords of any intent.
        Args:
            text: The text to check.

        Returns:
            Set of labels of the tweet, if any.
        """
        intents = []
        for intent, patterns in self.intent_to_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    intents.append(intent)
                    break  # No need to check other patterns for this intent.
        return set(intents)


# Signleton instance of the classifier that holds precompiled regex patterns for all intents.
classifier = RuleBasedClassifier()


def get_data(file_name):
    df = pd.read_csv(file_name)
    return df


def preprocess_tweet(text: str) -> str:
    """
    Preprocess the given text before inference.

    Right now only converts diacritics to ascii versions (turkish letters).
    Args:
        text: The text to normalize.

    Returns:
        Normalized text.
    """
    return unidecode(text)


def process_tweet(tweet: Tuple, plot_data: Dict) -> Tuple[Optional[Set[str]], Dict]:
    """
    Process the given tweet.
    Check if the tweet contains any of the keywords using rules.
    If it does, update the plot data and assign labels to the tweet

    Args:
        tweet: The tweet to process. tweet[1] -> full_text
        plot_data: The plot data to update.

    Returns:
        The labels of the tweet. If the tweet does not contain any of the keywords, return None.
    """

    # normalize text to english characters
    tweet_normalized = preprocess_tweet(tweet[1])  # tweet[1] -> full_text

    # check if tweet contains any of the keywords
    labels = classifier.classify(tweet_normalized)
    if not labels:
        return None, plot_data

    plot_data = update_plot_data(plot_data, labels)
    return labels, plot_data


def process_tweet_stream(df):
    plot_data = {}
    db_ready_data_list = []
    for _, row in df.iterrows():
        db_ready_data_list.append(process_tweet(row, plot_data))
    return db_ready_data_list, plot_data


def update_plot_data(plot_data: Dict, labels: Union[Set[str], List[str]]) -> Dict:
    """
    Increment the count of the given labels in the plot data.
    Args:
        plot_data: The dictionary that holds INTENT - COUNT pairs. 
        labels: The labels to increment the count of.

    Returns:
        The updated plot data.
    """
    for label in labels:
        if label in plot_data:
            plot_data[label] += 1
        else:
            plot_data[label] = 1
    return plot_data


def draw_plot(plot_data: Dict):
    """ Draw the plot with the given plot data.
       It draws label count of the tweets.

    Args:
        plot_data: The plot data to draw the plot with.

    Returns:
        None
    """
    plt.bar(plot_data.keys(), plot_data.values())
    plt.xlabel("Cluster Label")
    plt.ylabel("Tweet Count")
    plt.title("Tweet Count per Cluster Label")
    plt.show()


if __name__ == '__main__':
    data = get_data('sample_data.csv')
    processed_data, plot_data = process_tweet_stream(data)
    draw_plot(plot_data)
