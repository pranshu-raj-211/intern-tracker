import pandas as pd
import nltk
import time
import string
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

with open('data/queries.json', 'r') as f:
    queries = json.load(f)
query_words = [word for sublist in queries for word in sublist]


count =0

def preprocess_text(text):
    if pd.isnull(text):
        return ''
    
    text = text.lower()
    print('initiating punct removal')
    text = text.translate(str.maketrans('', '', string.punctuation))
    # ! punct not removed from inside word, example - let's

    print(text)
    time.sleep(5)
    # todo : add step to remove non alphabetical stuff
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords.words('english')]
    text = ' '.join(words)
    print('lemmatized text\n')
    print(text)
    time.sleep(10)
    return text

df = pd.read_csv('data/desc/2024_03_17desc_in.csv')
df['description'] = df['description'].apply(preprocess_text)

# How to store the vectors, would a json file with the doc index be good?
# Doc index can be made of timestamp (int) - as I scrape things with delays
vectorizer = TfidfVectorizer()

df['description'] = list(vectorizer.fit_transform(df['description']).toarray())
# df.to_csv('processed_data.csv', index=False)