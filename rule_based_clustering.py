import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

# set:
#  key: geo_loc
#  value: cluster_label: {enkaz: tweet_sayisi, tweet_id, created_at}, (yemek, tweet_sayisi, tweet_id, created_at), (barinma, tweet_sayisi, tweet_id, created_at), (ses, tweet_sayisi, tweet_id, created_at)
cluster_dict_label = {"KURTARMA": [{}], "YEMEK-SU": [{}], "GIYSI": [{}]}
kurtarma_keywords = ["enkaz", "enkaz altinda ses", "yardim", "altinda", "enkaz", "gocuk", "bina", "YARDIM", "acil", 
                    "kat", "ACIL", "altindalar", "enkazaltindayim", "yardim", "alinamiyor", "Enkaz", "yardimci", "ENKAZ", 
                    "saatlerdir", "destek", "altinda", "enkazda", "kurtarma", "kurtarma calismasi", "kurtarma talebi", "ulasilamayan kisiler", "ses"]
yemek_su_keywords = ["gida talebi", "gida", "yemek", "su", "corba", "yiyecek", "icecek"]
giysi_keywords = ["giysi talebi", "giysi", "battaniye", "yagmurluk", "kazak", "corap", "soguk", "isitici", "cadir"]
keywords = kurtarma_keywords + yemek_su_keywords + giysi_keywords
labels = ["KURTARMA", "YEMEK-SU", "GIYSI"]
# labels = [{"KURTARMA": kurtarma_keywords}, {"YEMEK-SU", yemek_su_keywords}, {"SES": ses_keywords}, {"GIYSI": giysi_keywords}]
# pattern = f"(^|\W){keywords}($|\W)"
# plot_data = {"key": labels, "count": [0 for i in range(len(labels))]}

def get_data(file_name):
    df = pd.read_csv(file_name)
    return df

def check_regex_return_keyword(full_text):
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
    if len(label_list) > 0:
        return set(label_list), True
    else:
        return None, False

def remove_diacritics(text):
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

def process_tweet(tweet, plot_data):
    # normalize text to english characters
    tweet_normalized = remove_diacritics(tweet[1]) # tweet[1] -> full_text
    # check if tweet contains any of the keywords
    labels, is_match = check_regex_return_keyword(tweet_normalized)
    if is_match:
        plot_data = update_plot_data(plot_data, labels)
        # TODO check: db format'a uygun mu? Halihazirda gelen bir dataya sadece label eklenecek ise guncellenmesi lazim.
        # db_format = {"label": labels, "geo_loc": tweet["geo_loc"], "tweet_id": tweet['tweet_id'], "created_at": tweet['created_at'], "full_text": tweet['full_text']}
        return labels, plot_data
    else:
        return None, plot_data

def process_tweet_stream(df):
    db_ready_data_list = []
    for _, row in df.iterrows():
        db_ready_data_list.append(process_tweet(row))
    return db_ready_data_list

def update_plot_data(plot_data, labels):
    for label in labels:
        label_idx = [i for i, x in enumerate(plot_data["key"]) if x == label][0]
        plot_data["count"][label_idx] += 1
    return plot_data

def draw_plot(plot_data):
        plt.bar(plot_data["key"], plot_data["count"])
        plt.xlabel("Cluster Label")
        plt.ylabel("Tweet Count")
        plt.title("Tweet Count per Cluster Label")
        plt.show()

# data = get_data('data_new.csv')
# processed_data = process_tweet_stream(data)
# draw_plot(plot_data)