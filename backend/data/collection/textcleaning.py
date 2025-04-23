# Mar 11, 2025

import re
import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')


def clean_text(text):
    # convert text to lowercase
    text = text.lower()

    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # remove numbers
    text = re.sub(r'\d+', '', text)

    # remove unnecessary white spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # remove stopwords from text
    #stop_words = set(stopwords.words('english'))
    tokens = text.split()
    tokens = [word for word in tokens]
    #tokens = [word for word in tokens if word not in stop_words]

    # join cleaned tokens
    cleaned_text = ' '.join(tokens)
    return cleaned_text