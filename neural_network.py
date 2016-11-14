# Functions in this file train a text-generation neural network for each candidate or use the stored neural to generate a response based on a given seed. Running the if __name__ == '__main__' block trains and the neural net. Model is based on one of the examples provided by Keras.

from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import cPickle as pickle
from document_similarity import find_questions_and_answers
sys.setrecursionlimit(1500)

def train_neural_net(candidate, df):
    '''
    Train a neural net based for each candidate based on entire content of respnonses.
    '''
    text = ''.join(df[df['speaker']==candidate]['content'].values)
    text = text.split(' ')
    words = sorted(list(set(text)))
    word_indices = dict((w, i) for i, w in enumerate(words))
    indices_word = dict((i, w) for i, w in enumerate(words))

    maxlen = 10
    step = 3
    sentences = []
    next_words = []
    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_words.append(text[i + maxlen])

    print('Vectorization...')
    X = np.zeros((len(sentences), maxlen, len(words)), dtype=np.bool)
    y = np.zeros((len(sentences), len(words)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, word in enumerate(sentence):
            X[i, t, word_indices[word]] = 1
        y[i, word_indices[next_words[i]]] = 1

    print('Build model...')
    model = Sequential()
    model.add(LSTM(128, input_shape=(maxlen, len(words))))
    model.add(Dense(len(words)))
    model.add(Activation('softmax'))
    optimizer = RMSprop(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    model.fit(X, y, batch_size=128, nb_epoch=20)

    #pickle_model
    filename = 'neural_networks/{}_neural_network.pkl'.format(candidate)
    with open(filename, 'w') as f:
        pickle.dump(model, f)

    return None

def sample(preds, temperature=1.0):
    '''
    Helper function to sample an index from a probability array
    '''
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def generate_one_response(seed,candidate,df):
    '''
    INPUTS:
        seed: User question (str)
        candidate: Candidate name (str)
        df: dataframe of all debate transcripts (pandas dataframe)
    OUTPUT:
        answer: Hypothetical answer to seed question (str) for display in web app
    '''
    text = ''.join(df[df['speaker']==candidate]['content'].values)
    text = text.split(' ')
    words = sorted(list(set(text)))
    word_indices = dict((w, i) for i, w in enumerate(words))
    indices_word = dict((i, w) for i, w in enumerate(words))

    maxlen = 10
    step = 3
    sentences = []
    next_words = []
    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_words.append(text[i + maxlen])

    X = np.zeros((len(sentences), maxlen, len(words)), dtype=np.bool)
    y = np.zeros((len(sentences), len(words)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, word in enumerate(sentence):
            try:
                X[i, t, word_indices[word]] = 1
            except:
                pass
        y[i, word_indices[next_words[i]]] = 1

    filename = 'neural_networks/{}_neural_network.pkl'.format(candidate)
    with open(filename) as f:
        model = pickle.load(f)

    sentence = find_questions_and_answers(df, candidate, seed)
    # sentence = sentence.strip("...")
    sentence = sentence.split(' ')
    sentence = sentence[:5] if len(sentence) >= 5 else sentence
    # generated = []
    # generated.extend(sentence)
    # # print('{} says: '.format(candidate))
    # # print('----- Generating with seed: "' + ' '.join(generated) + '"')
    # # sys.stdout.write(' '.join(generated))
    # # sys.stdout.write(' ')

    for i in range(40):
        x = np.zeros((1, maxlen, len(words)))
        for t, word in enumerate(sentence):
            try:
                x[0, t, word_indices[word]] = 1.
            except:
                pass
        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, 10.)
        next_word = indices_word[next_index]

        # generated.append(next_word)
        sentence.append(next_word)
        sentence = sentence[1:]
        # sys.stdout.write(next_word)
        # sys.stdout.write(' ')
        # sys.stdout.flush()
        seed += ' '
        seed += next_word
    return seed

def generate_responses(question):
    with open('transcripts_df.pkl') as f:
        df = pickle.load(f)
    responses = {}
    candidates = ['KENNEDY','REAGAN','B. CLINTON', 'OBAMA', 'H. R. CLINTON','TRUMP']
    for c in candidates:
        print(c)
        responses[c] = generate_one_response(question, c, df)
        print(responses[c])
    return responses


if __name__ == '__main__':

    with open('transcripts_df.pkl') as f:
        df = pickle.load(f)

    candidates = [
        'KENNEDY',
        'REAGAN',
        'B. CLINTON',
        'OBAMA',
        'H. R. CLINTON',
        'TRUMP']

    # for c in candidates:
    #     train_neural_net(c, df)
    #     generate_one_response("What is your plan for immigration?",c,df)
