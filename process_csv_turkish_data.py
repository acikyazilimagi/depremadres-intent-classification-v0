import re
import pandas as pd
# from unicodedata import normalize
from unidecode import unidecode

def get_data(file_name):
    df = pd.read_csv(file_name, header=None)
    return df

# write pd dataframe to csv
def write_to_csv(df, file_name):
    df.to_csv(file_name, index=False)

def check_regex(full_text):
    full_text = re.sub(r'[^a-z\s]+', '', full_text, flags=re.IGNORECASE)
    return full_text

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

if __name__ == "__main__":
    df = get_data("deprem_convert_csv/v10.csv")
    # df.drop(index=df.index[1], inplace=True) # drop first row
    print(df.head())
    for i in df.columns:
        df[i] = df[i].apply(lambda x: unidecode(x) if type(x) == str else x)
    print(df.head())
    write_to_csv(df, "deprem_converted_csv/v10.csv")
