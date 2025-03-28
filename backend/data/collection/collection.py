# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# import clean_text from textcleaning.py
from textcleaning import clean_text
# import functions from editdataset.py
from editdataset import read_csv, display_informatiion, to_text

politics_data = "./input/Political_tweets.csv"
columns = 'text'

def import_dataframe(data):
    df = read_csv(data)
    return df

def drop_columns(df):

    columns = ['user_name', 'user_location', 'user_description',
               'user_created', 'user_followers', 'user_friends',
               'user_favourites', 'user_verified', 'date',
               'hashtags', 'source', 'is_retweet']

    for c in columns:
        df.drop(c, axis=1, inplace=True)

    return df

def main():
    # import dataframe and call it as df
    df = import_dataframe(politics_data)
    display_informatiion(df)
    df_text = drop_columns(df)
    display_informatiion(df_text)
    #print("Before Cleaning:", text)
    #print("\nAfter Cleaning:", clean_text(text))

if __name__ == "__main__":
    main()