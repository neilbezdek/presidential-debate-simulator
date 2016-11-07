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
    Output: Function returns the location of the most similar question that that candidate has answered
    '''
    #lemmatize and remove stop words from question
    question = lemmatizer(question)
    df_new = df[df['speaker'] == candidate][['question','simple_question','content']]
    df_new.reset_index(drop=True, inplace = True)

    corpus = [question] + df_new['simple_question'].values.tolist()

    tfidf = TfidfVectorizer(stop_words=build_stop_words()).fit_transform(corpus)
    cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
    most_similar_question_idx = cosine_similarities.argsort()[-2]

    # Print statements for assessing model
    # print '\nSimlilar question index:'
    # print most_similar_question_idx, '\n'
    # print 'Original question:'
    # print question, '\n'
    # print 'Most similar question:'
    # print df_new.ix[most_similar_question_idx,'question'], '\n'
    # print 'Candidate answer:'
    # print df_new.ix[most_similar_question_idx,'content'], '\n'
    return df_new.ix[most_similar_question_idx,'content']

def answer_questions(question, candidates = ['KENNEDY','REAGAN','B. CLINTON', 'OBAMA', 'H. R. CLINTON','TRUMP']):
    with open('transcripts_df.pkl') as f:
        df = pickle.load(f)
    for c in candidates:
        print c
        print find_questions_and_answers(df, c, question),'\n'
    return None

if __name__ == '__main__':

    pass
