import pandas as pd

# Load the dataset

def read_csv(file):
    df = pd.read_csv(file)
    return df

def display_informatiion(df):
    print(' \n head {}'.format(df.head()))
    print(' \n info {}'.format(df.info()))

def to_text(df, columns):
    df = df[columns]
    return df