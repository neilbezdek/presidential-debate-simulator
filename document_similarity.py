# Web app uses these functions to retrieve candidate responses based on user input

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords
import numpy as np
import numpy.linalg as LA
from lemmatizer import lemmatizer
from topic_modeling import build_stop_words
import cPickle as pickle

def find_questions_and_answers(df, candidate, question):
    '''
    Input: DF with all transcript contents, name of candidate (str), question from user (str)
    Output: Function returns the location of the most similar question  that candidate has answered
    '''
    #lemmatize and remove stop words from question
    question = lemmatizer(question)
    df_new = df[df['speaker'] == candidate][['question','simple_question','content']]
    df_new.reset_index(drop=True, inplace = True)

    corpus = [question] + df_new['simple_question'].values.tolist()

    tfidf = TfidfVectorizer(stop_words=build_stop_words()).fit_transform(corpus)
    cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
    most_similar_question_idx = cosine_similarities.argsort()[-2]
    return df_new.ix[most_similar_question_idx,'content']

def answer_questions(question):
    with open('transcripts_df.pkl') as f:
        df = pickle.load(f)
    responses = {}
    candidates = ['KENNEDY','REAGAN','B. CLINTON', 'OBAMA', 'H. R. CLINTON','TRUMP']
    for c in candidates:
        responses[c] = find_questions_and_answers(df, c, question)
    return responses

def find_closest_answers(df, candidate, question):
    '''
    Input: DF with all transcript contents, name of candidate (str), question from user (str)
    Output: Function returns the location of the most similar answer that a candidate has given
    '''
    #lemmatize and remove stop words from question
    question = lemmatizer(question)
    df_new = df[(df['speaker'] == candidate) & (df['len'] > 20)][['simple_content','content']]
    df_new.reset_index(drop=True, inplace = True)

    corpus = [question] + df_new['simple_content'].values.tolist()

    tfidf = TfidfVectorizer(stop_words=build_stop_words()).fit_transform(corpus)
    cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
    most_similar_question_idx = cosine_similarities.argsort()[-2]
    return df_new.ix[most_similar_question_idx,'content']

def give_closest_answers(question):
    with open('transcripts_df.pkl') as f:
        df = pickle.load(f)
    responses = {}
    candidates = ['KENNEDY','REAGAN','B. CLINTON', 'OBAMA', 'H. R. CLINTON','TRUMP']
    for c in candidates:
        responses[c] = find_closest_answers(df, c, question)
    return responses

if __name__ == '__main__':
    pass
