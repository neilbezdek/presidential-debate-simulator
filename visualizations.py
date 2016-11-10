import numpy as np
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import cPickle as pickle
from lemmatizer import lemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
plt.style.use('ggplot')

def make_average_words_plot(df):
    fig = plt.figure(figsize = (12,9))
    fig.add_subplot(1,1,1)
    rep_len = df[df['party']=='Republican'].groupby(['year'])['len'].mean().values
    dem_len = df[df['party']=='Democrat'].groupby(['year'])['len'].mean().values
    x = df[df['party']=='Democrat'].groupby(['year'])['len'].mean().index
    plt.plot(x, rep_len, 'ro-', label = 'Republican')
    plt.plot(x, dem_len, 'b^-', label = 'Democrat')
    plt.title('Mean Length of Continuous Speech')
    plt.xlabel('Debate Year')
    plt.ylabel('Mean Number of Words Per Response Before Stopping or Interruption')
    plt.legend()
    plt.savefig('images/average_words_per_response.png', dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches=None, pad_inches=0.3, frameon=None)
    return None

def make_vocabulary_size_plot(df):

    years = sorted(list(set(df['year'].values)))
    rep_vocab = []
    for year in years:
        corpus = ' '.join(df[(df['party']=='Republican') & (df['year'] == year)]['simple_content'].values).split(' ')[:2500]
        vocab_size = CountVectorizer().fit_transform(corpus).shape[1]
        rep_vocab.append(vocab_size)

    dem_vocab = []
    for year in years:
        corpus = ' '.join(df[(df['party']=='Democrat') & (df['year'] == year)]['simple_content'].values).split(' ')[:2500]
        vocab_size = CountVectorizer().fit_transform(corpus).shape[1]
        dem_vocab.append(vocab_size)

    fig = plt.figure(figsize = (12,9))
    fig.add_subplot(1,1,1)
    plt.plot(years, rep_vocab, 'ro-', label = 'Republican')
    plt.plot(years, dem_vocab, 'b^-', label = 'Democrat')
    plt.title('Vocabulary Size Per Candidate Per Election')
    plt.xlabel('Debate Year')
    plt.ylabel('Unique Words Per First 2500 Words')
    plt.ylim(600,1000)
    plt.legend()
    plt.savefig('images/vocab_size_per_election.png', dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches=None, pad_inches=0.3, frameon=None)
    return None

if __name__ == '__main__':

    with open('transcripts_df.pkl') as f:
        df = pickle.load(f)
