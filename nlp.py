# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup
from spacy.lang.es.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

from itertools import combinations

from gensim.models import KeyedVectors


#word_vectors = KeyedVectors.load_word2vec_format(r'cc.es.300.vec.gz', limit=20000)

#word_vectors.save(r'medium_cc.es.300.kv')

word_vectors = KeyedVectors.load("medium_cc.es.300.kv", mmap='r')

#word_vectors = KeyedVectors.load("small_cc.es.300.kv", mmap='r')

# print(word_vectors.index_to_key[0:10])
# print(type(word_vectors.index_to_key))

stop = list(set(list(STOP_WORDS) + word_vectors.index_to_key[0:100]))

top_1000_words = word_vectors.index_to_key[:2000]
top_1000_vectors = [word_vectors[word] for word in top_1000_words]


def get_most_similar_words(top_words, ngrupos = 6, n_words_target = 6):
    similar_words = top_words[:2]
    similar_words_values = []
    # Generar combinaciones de 4 palabras de las 5 originales
    # print(type(top_words))
    # print('top_words')
    # print(top_words)
    for combo in combinations(top_words, ngrupos):
        # Calcular el vector promedio para la combinación actual
        count = 0
        suma= 0
        # print('combo')
        # print(combo)
        for i, word in enumerate(combo):
            try:
                suma+= word_vectors[word]
                count+=1
            except KeyError:
                # print('no')
                pass
            try:
                avg_vector = suma/count
            except ZeroDivisionError:
                avg_vector = word_vectors['general']
                # print('combo')
                # print(combo)
        # Encontrar la palabra más similar a ese vector promedio
        try:
            most_similar = word_vectors.most_similar(positive = [avg_vector], negative = similar_words[-1:], topn=15)
        except:
            most_similar = word_vectors.most_similar(positive = [avg_vector], topn=15)
        for similar_word in most_similar:
            if similar_word[0].lower().strip() not in similar_words:
                # print('similar_word')
                # print(similar_word)
                # Tomar solo la palabra del resultado
                if similar_word[0].lower().strip() in word_vectors.index_to_key:
                    similar_words.append(similar_word[0].lower().strip())
                    similar_words_values.append(similar_word[1])
                    # print('ya llevamos')
                    # print(similar_words)
                    break
            
        if len(similar_words)==n_words_target:
                return similar_words
            
       # df = pd.DataFrame({'words':similar_words, 'values':similar_words_values})
       # similar_words_list = df.sort_values(['values'], ascending = False).head(5)['words'].to_list()
    return similar_words

# Supongamos que estas son las palabras obtenidas con TF-IDF
tfidf_words = ['abril', 'mayo', 'martes', 'luna', 'caballo', 'estrella', 'nube', 'esotérico', 'pasta', 'sensual']
similar_result = get_most_similar_words(tfidf_words)
print(similar_result)

print(similar_result[3]==similar_result[5])





def find_internal_links(domain, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    internal_links = [link for link in links if domain in link]
    return list(set(internal_links))

def extract_content_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = ' '.join([p.text for p in soup.find_all('p')])
    return text

def compute_tfidf_for_urls(urls, language='spanish'):
    documents = [extract_content_from_url(url) for url in urls]
    vectorizer = TfidfVectorizer(stop_words=list(STOP_WORDS))
    print(documents)
    print(len(documents))
    if len(documents) > 20:
        documents = documents[0:20]
    X = vectorizer.fit_transform(documents)
    feature_array = vectorizer.get_feature_names_out()
    tfidf_sorting = [sorted(zip(X[i].toarray().flatten(), feature_array), reverse=True) for i in range(X.shape[0])]
    return tfidf_sorting

def get_top_n_words(tfidf_sorting, n=10):
    top_n_words = []
    for sorting in tfidf_sorting:
        top_n_words.append([word[1] for word in sorting[:n]])
    return top_n_words