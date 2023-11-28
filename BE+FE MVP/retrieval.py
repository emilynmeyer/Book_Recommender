## Importing necessary modules

import nltk

import string
import pickle
import pandas as pd
import numpy as np
from rank_bm25 import BM25Okapi
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
nltk.download('wordnet')
nltk.download('stopwords')


## Function to preprocess sentence
def preprocess_sentence(sentence):
    lemmatizer = WordNetLemmatizer()
    porter = PorterStemmer()
    
    sentence = sentence.split(' ')
    
    for i, word in enumerate(sentence):
        word = word.lower()
        word = "".join([char for char in word if char not in string.punctuation])
        word = lemmatizer.lemmatize(word)
        word = porter.stem(word)
        sentence[i] = word
    
    sentence = [word for word in sentence if word not in stopwords.words('english')]
    sentence = " ".join(sentence)
    
    return sentence

def get_top_five(query_string):
    ## Importing book information (Title, ISBN, Description, etc.) extracted from Google BooksAPI
    with open('book_list.pkl', 'rb') as input_file:
        book_list = pickle.load(input_file)
        
    ## Preprocessing description
    desc_isbn = {}

    for k, v in book_list.items():
        desc = preprocess_sentence(v['description'])
        desc_isbn[desc] = k


    # https://pypi.org/project/rank-bm25/

    corpus = list(desc_isbn.keys())

    tokenized_corpus = [doc.split(" ") for doc in corpus]

    bm25 = BM25Okapi(tokenized_corpus)

    query = preprocess_sentence(query_string)
    tokenized_query = query.split(" ")

    doc_scores = bm25.get_scores(tokenized_query)
    max_index = np.argmax(doc_scores)
    top_n = bm25.get_top_n(tokenized_query, corpus, n=5)

    isbns = []
    
    for i, idx in enumerate(top_n):
        print('Rank', i + 1, ":", book_list[desc_isbn[idx]].get('title'), '-', book_list[desc_isbn[idx]].get('author'))
        isbns.append(desc_isbn[idx])
    
    return isbns

        
#print(get_top_five("Harry Potter has never been the star of a Quidditch team, scoring points while riding a broom far above the ground. He knows no spells, has never helped to hatch a dragon, and has never worn a cloak of invisibility. All he knows is a miserable life with the Dursleys, his horrible aunt and uncle, and their abominable son, Dudley"))
