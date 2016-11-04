import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, ENGLISH_STOP_WORDS
from sklearn.decomposition import TruncatedSVD, NMF
from numpy.random import rand, RandomState
from numpy import array, matrix, linalg
import cPickle as pickle
import csv


def reconst_mse(target, left, right):
    return (array(target - left.dot(right))**2).mean()

def describe_nmf_results(document_term_mat, W, H, n_top_words = 15):
    print("Reconstruction error: %f") %(reconst_mse(document_term_mat, W, H))
    for topic_num, topic in enumerate(H):
        print("Topic %d:" % topic_num)
        print(" ".join([feature_words[i] \
                for i in topic.argsort()[:-n_top_words - 1:-1]]))
    return

def build_stop_words():
    with open('stop_words.csv', 'rb') as f:
        reader = csv.reader(f)
        my_stop_words = list(reader)[0]
    my_stop_words.extend(ENGLISH_STOP_WORDS)
    return my_stop_words

if __name__ == "__main__":
    n_features = 1000
    n_topics = 15

    # Use imported function to read transcripts and build df
    # from read_transcripts import read_transcripts_into_df
    # df = read_transcripts_into_df()

    # Instead, open pickeled model to save time:
    with open('transcripts_df.pkl') as f:
        df = pickle.load(f)

    docs = df[(df['speaker'] != 'MODERATOR') & (df['len'] > 75)]['content']
    my_stop_words = build_stop_words()

    vectorizer = TfidfVectorizer(max_df = .7, stop_words=my_stop_words, analyzer = 'word',ngram_range = (1,2))
    document_term_mat = vectorizer.fit_transform(docs)
    feature_words = vectorizer.get_feature_names()

    print("\n Decomposition: \n")
    nmf = NMF(n_components=n_topics)
    W = nmf.fit_transform(document_term_mat)
    H = nmf.components_
    describe_nmf_results(document_term_mat, W, H)
