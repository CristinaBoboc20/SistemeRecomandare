import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity
import os
print(os.getcwd())

df = pd.read_csv("Lab4\startups.csv")
df = df.head(1000)  
print("Dataset loaded. Number of items:", len(df))

stopwords_set = text.ENGLISH_STOP_WORDS

def text_clean(text):
    text = str(text).lower() 
    text = re.sub(r'[^a-z\s]', ' ', text)  
    text = " ".join([w for w in text.split() if w not in stopwords_set]) 
    return text

df["description"] = df["description"].fillna("")

texts_cleaned = df["description"].apply(text_clean)

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(texts_cleaned)

similarity_matrix = cosine_similarity(tfidf_matrix)
np.fill_diagonal(similarity_matrix, 0)

max_idx = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)
startup1 = df.iloc[max_idx[0]]["name"]
startup2 = df.iloc[max_idx[1]]["name"]
score = similarity_matrix[max_idx]

desc1 = df.iloc[max_idx[0]]["description"]
desc2 = df.iloc[max_idx[1]]["description"]

print("Most Similar Startups:")
print(f"1. {startup1}")
print(f"2. {startup2}")
print(f"Cosine Similarity Score: {score:.4f}\n")

print("Descriptions:")
print(f"{startup1}: {desc1}\n")
print(f"{startup2}: {desc2}\n")

with open("Lab4\README.txt", "w", encoding="utf-8") as f:
    f.write("Most similar startups:\n")
    f.write(f"1. {startup1}\n")
    f.write(f"2. {startup2}\n")
    f.write(f"Cosine Similarity Score: {score:.4f}\n\n")
    f.write("Descriptions:\n")
    f.write(f"{startup1}: {desc1}\n\n")
    f.write(f"{startup2}: {desc2}\n")
