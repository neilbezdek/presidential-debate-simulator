import pattern.en as en
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, ENGLISH_STOP_WORDS
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
    INPUT: article (str) - raw text from the article (where text has been lowered and punctuation removed already)
    OUTPUT: lemmatized_article - article text with all stopwords removed and the remaining text lemmatized
    '''
    # Load in stopwords from load_data
    stopwords = build_stop_words()
    # Load Dictionary to fix commonly mislemmatized words
    # correct_lemma = fix_lemmatized_words()
    # Lemmatize article by running each word through the pattern.en lemmatizer and only including it in the resulting text if the word doesn't appear in the set of stopwords

    exclude = set(string.punctuation)
    line = ''.join(ch for ch in line if ch not in exclude)
    line = ' '.join([en.lemma(w) for w in line.split() if w not in stopwords])
    # Return the article text after fixing common mislemmatized words
    return line
