import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from typing import Dict, Tuple, Set, Optional, List, Union

# set:
#  key: geo_loc
#  value: cluster_label: {enkaz: tweet_sayisi, tweet_id, created_at}, (yemek, tweet_sayisi, tweet_id, created_at), (barinma, tweet_sayisi, tweet_id, created_at), (ses, tweet_sayisi, tweet_id, created_at)
cluster_dict_label = {"KURTARMA": [{}], "YEMEK-SU": [{}], "GIYSI": [{}]}
kurtarma_keywords = ["enkaz", "enkaz altinda ses", "yardim", "altinda", "enkaz", "gocuk", "bina", "YARDIM", "acil", 
                    "kat", "ACIL", "altindalar", "enkazaltindayim", "yardim", "alinamiyor", "Enkaz", "yardimci", "ENKAZ", 
                    "saatlerdir", "destek", "altinda", "enkazda", "kurtarma", "kurtarma calismasi", "kurtarma talebi", "ulasilamayan kisiler", 
                     "ses", "vinc", "eskavator", "projektor", "sesler", "kurtarilmayi", "yaşında", "blok", "altında",
                     "apartmanı", "Sitesi", "ailesi", "göçük", "acilvinc", "sesi", "altındalar", "Doktor"]
yemek_su_keywords = ["gida talebi", "gida", "yemek", "su", "corba", "yiyecek", "icecek", "acliktan", "erzak"]
giysi_keywords = ["giysi talebi", "giysi", "battaniye", "yagmurluk", "kazak", "corap", "soguk", "bot", "isitici", "cadir", "hava", 
                    "camasir", "pijama", "soguktan", "yatak", "sisme", "bez", "bezi", "bebek bezi", "soba", 
                    "hijyen", "temizlik", "temizlik malzemesi", "basortu", "hijyen paketi", "kar", "hipotermi", "donmak", "yorgan"]

keywords = kurtarma_keywords + yemek_su_keywords + giysi_keywords
labels = ["KURTARMA", "YEMEK-SU", "GIYSI"]
# labels = [{"KURTARMA": kurtarma_keywords}, {"YEMEK-SU", yemek_su_keywords}, {"SES": ses_keywords}, {"GIYSI": giysi_keywords}]
# pattern = f"(^|\W){keywords}($|\W)"
# plot_data = {"key": labels, "count": [0 for i in range(len(labels))]}

def get_data(file_name):
    df = pd.read_csv(file_name)
    return df

def check_regex_return_keyword(full_text: str)-> Set[str]:
    """
    Check if the given text contains any of the keywords. To assign a label to the tweet.
    Args:
        full_text: The text to check.

    Returns:
        The labels of the tweet. If the tweet does not contain any of the keywords, return an empty set.
    """
    label_list = []
    for keyword in keywords:
        pattern = f"(^|\W){keyword}($|\W)"
        full_text = re.sub(r'[^a-z\s]+', '', full_text, flags=re.IGNORECASE)
        if re.search(pattern, full_text, re.IGNORECASE):
            if keyword in kurtarma_keywords:
                label_list.append("KURTARMA")
            elif keyword in yemek_su_keywords:
                label_list.append("YEMEK-SU")
            elif keyword in giysi_keywords:
                label_list.append("GIYSI")

    return set(label_list)

def remove_diacritics(text: str) -> str:
    """
    Remove diacritics from the given text.
    Args:
        text: The text to remove diacritics from.

    Returns:
        The text without diacritics.
    """
    # define the mapping from diacritic characters to non-diacritic characters
    mapping = {
        '\u00c7': 'C', '\u00e7': 'c',
        '\u011e': 'G', '\u011f': 'g',
        '\u0130': 'I', '\u0131': 'i',
        '\u015e': 'S', '\u015f': 's',
        '\u00d6': 'O', '\u00f6': 'o',
        '\u00dc': 'U', '\u00fc': 'u',
        '\u0152': 'OE', '\u0153': 'oe',
        '\u0049': 'I', '\u0131': 'i',
    }
 
    # replace each diacritic character with its non-diacritic counterpart
    text = ''.join(mapping.get(c, c) for c in text)
 
    return text

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
    tweet_normalized = remove_diacritics(tweet[1]) # tweet[1] -> full_text

    # check if tweet contains any of the keywords
    labels = check_regex_return_keyword(tweet_normalized)
    if not labels:
        return None, plot_data

    plot_data = update_plot_data(plot_data, labels)
    # TODO check: db format'a uygun mu? Halihazirda gelen bir dataya sadece label eklenecek ise guncellenmesi lazim.
    # db_format = {"label": labels, "geo_loc": tweet["geo_loc"], "tweet_id": tweet['tweet_id'], "created_at": tweet['created_at'], "full_text": tweet['full_text']}
    return labels, plot_data


def process_tweet_stream(df):
    db_ready_data_list = []
    for _, row in df.iterrows():
        db_ready_data_list.append(process_tweet(row))
    return db_ready_data_list

def update_plot_data(plot_data: Dict, labels: Union[Set[str],List[str]]) -> Dict:
    """
    Update the plot data with the given labels.
    Args:
        plot_data: The plot data to update.
        labels: The labels to update the plot data with.

    Returns:
        The updated plot data.
    """
    for label in labels:
        label_index = plot_data["key"].index(label)
        plot_data["count"][label_index] += 1
    return plot_data

def draw_plot(plot_data: Dict):
    """ Draw the plot with the given plot data.
       It draws label count of the tweets.

    Args:
        plot_data: The plot data to draw the plot with.

    Returns:
        None
    """
    plt.bar(plot_data["key"], plot_data["count"])
    plt.xlabel("Cluster Label")
    plt.ylabel("Tweet Count")
    plt.title("Tweet Count per Cluster Label")
    plt.show()

# data = get_data('data_new.csv')
# processed_data = process_tweet_stream(data)
# draw_plot(plot_data)
