from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys

from read_transcripts import read_transcripts_into_df
# path = get_file('nietzsche.txt', origin="https://s3.amazonaws.com/text-datasets/nietzsche.txt")
# text = open(path).read().lower()

df = read_transcripts_into_df()
text = ''.join(df[df['speaker']=='OBAMA']['content'].values)
text = text.split(' ')
print('corpus length:', len(text))

words = sorted(list(set(text)))
print('total words:', len(words))
word_indices = dict((w, i) for i, w in enumerate(words))
indices_word = dict((i, w) for i, w in enumerate(words))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 10
step = 3
sentences = []
next_words = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_words.append(text[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
X = np.zeros((len(sentences), maxlen, len(words)), dtype=np.bool)
y = np.zeros((len(sentences), len(words)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, word in enumerate(sentence):
        X[i, t, word_indices[word]] = 1
    y[i, word_indices[next_words[i]]] = 1


# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(words))))
model.add(Dense(len(words)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# train the model, output generated text after each iteration
for iteration in range(1, 2):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(X, y, batch_size=128, nb_epoch=20)

    start_index = random.randint(0, len(text) - maxlen - 1)

    for diversity in [0.2, 0.5, 1.0, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0]:
        print()
        print('----- diversity:', diversity)

        generated = []
        sentence = text[start_index: start_index + maxlen]
        generated.extend(sentence)
        print('----- Generating with seed: "' + ' '.join(generated) + '"')
        sys.stdout.write(' '.join(generated))
        sys.stdout.write(' ')

        for i in range(40):
            x = np.zeros((1, maxlen, len(words)))
            for t, word in enumerate(sentence):
                x[0, t, word_indices[word]] = 1.

            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_word = indices_word[next_index]

            generated.append(next_word)
            sentence.append(next_word)
            sentence = sentence[1:]
            sys.stdout.write(next_word)
            sys.stdout.write(' ')
            sys.stdout.flush()
        print()
