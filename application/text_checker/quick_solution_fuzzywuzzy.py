import pandas as pd
from fuzzywuzzy import fuzz, process

# %%


def checker(input_text):
    absolute_path = "C:/personal projects/fakenews/data/first_dataset.xlsx"
    relative_path = "data/first_dataset.xlsx"
    df = pd.read_excel(relative_path)

    our_data = df["text"].values
    return process.extractOne(input_text, our_data, scorer=fuzz.token_sort_ratio)


if __name__ == "__main__":
    print(checker("India has not outlawed social media"))