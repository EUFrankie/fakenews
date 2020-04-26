import pandas as pd
from fuzzywuzzy import fuzz, process
import json


# %%


def basic_checker(input_text, path="rel"):
    absolute_path = "C:/personal projects/fakenews/data/first_dataset.xlsx"
    relative_path = "data/first_dataset.xlsx"
    if path == "rel":
        df = pd.read_excel(relative_path)
    elif path == "abs":
        df = pd.read_excel(absolute_path)

    our_data = df["text"].values
    return process.extractOne(input_text, our_data, scorer=fuzz.token_sort_ratio)


def checker(input_text, path="rel"):
    absolute_path = "C:/personal projects/fakenews/data/data_poynter_COMPLETE_without_cleaning_2020-04-25.csv"
    relative_path = "data/data_poynter_COMPLETE_without_cleaning_2020-04-25.csv"

    if path == "rel":
        df = pd.read_csv(relative_path)
    elif path == "abs":
        df = pd.read_csv(absolute_path)

    def filter_titles(title):
        number_title_words = len(title.split())
        if number_title_words >= 4:
            return True
        else:
            return False

    df = df[df.title.apply(filter_titles)]

    our_titles = df["title"].values

    text, score = process.extractOne(input_text, our_titles, scorer=fuzz.token_set_ratio)

    relevant_row = df[df["title"] == text]

<<<<<<< HEAD
    json_format = {
        "fact_checker": relevant_row["fact_checker"].iloc[0],
        "date": relevant_row["date"].iloc[0],
        "location": relevant_row["location"].iloc[0],
        "label": relevant_row["label"].iloc[0],
        "title": relevant_row["title"].iloc[0],
        "explanation": relevant_row["explanation"].iloc[0],
        "score": score
    }
=======
    if relevant_row.shape[0] > 0:
        json_format = {
            "fact_checker": relevant_row["fact_checker"].iloc[0],
            "date": relevant_row["date"].iloc[0],
            "location": relevant_row["location"].iloc[0],
            "label": relevant_row["label"].iloc[0],
            "title": relevant_row["title"].iloc[0],
            "explanation": relevant_row["explanation"].iloc[0],
            "score":  score
        }
    else:
        json_format = {
            "fact_checker": " ",
            "date": " ",
            "location": " ",
            "label": " ",
            "title": " ",
            "explanation": " ",
            "score":  0
        }
>>>>>>> 2faebd426248d693f882603cf6cce00c66da3246

    return json_format


def checker_options(input_text, path="rel"):
    absolute_path = "C:/personal projects/fakenews/data/data_poynter_COMPLETE_2020-04-24.csv"
    relative_path = "data/data_poynter_COMPLETE_2020-04-24.csv"

    if path == "rel":
        df = pd.read_csv(relative_path)
    elif path == "abs":
        df = pd.read_csv(absolute_path)

    our_titles = df["title"].values

    output = process.extract(input_text, our_titles, scorer=fuzz.token_set_ratio, limit=3)

    output_list = []
    for item in output:
        relevant_row = df[df["title"] == item[0]]
        output_list.append({
            "fact_checker": relevant_row["fact_checker"].iloc[0],
            "date": relevant_row["date"].iloc[0],
            "location": relevant_row["location"].iloc[0],
            "label": relevant_row["label"].iloc[0],
            "title": relevant_row["title"].iloc[0],
            "explanation": relevant_row["explanation"].iloc[0],
            "url_checker": relevant_row["url_checker"].iloc[0],
            "score": item[1]
        })
    return output_list


def checker_test(input_text, path="rel"):
    absolute_path = "C:/personal projects/fakenews/data/data_poynter_COMPLETE_without_cleaning_2020-04-25.csv"
    relative_path = "data/data_poynter_COMPLETE_without_cleaning_2020-04-25.csv"

    if path == "rel":
        df = pd.read_csv(relative_path)
    elif path == "abs":
        df = pd.read_csv(absolute_path)

    our_titles = df["title"]

    result = process.extract(input_text, our_titles, scorer=fuzz.token_set_ratio, limit=None)

    return df, result


if __name__ == "__main__":
    # print(basic_checker("India has not outlawed social media", "abs"))
    print(checker("5G causes flu", "abs"))
    df, result = checker_test("5G causes flu", "abs")
    test_result = fuzz.token_set_ratio("5G causes flu",
                                       "The 5G network causes flu symptoms and it caused the covid-19 pandemic")
    testing = checker_options("5G causes flu", "abs")
    print(checker_options("5G causes flu", "abs"))
