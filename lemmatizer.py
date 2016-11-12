import pattern.en as en
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import csv
import string

def build_stop_words():
    with open('stop_words.csv', 'rb') as f:
        reader = csv.reader(f)
        my_stop_words = list(reader)[0]
    my_stop_words.extend(ENGLISH_STOP_WORDS)
    return my_stop_words

def lemmatizer(line):
    '''
    For each line of text (str), lemmatize words before vectorization.
    '''
    stopwords = build_stop_words()
    exclude = set(string.punctuation)
    line = ''.join(ch for ch in line if ch not in exclude)
    line = ' '.join([en.lemma(w) for w in line.split() if w not in stopwords])
    return line

if __name__ == '__main__':
    pass
