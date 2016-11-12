from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
import csv
from wordcloud import WordCloud
from lemmatizer import build_stop_words

def make_masked_cloud(df, party):

    d = path.dirname(__file__)

    text = df[df['party']==party]['simple_content'].values.tolist()
    text = ' '.join(text)

    party = party.replace('. ','')
    party = party.lower()

    stencil_filename = 'images/{}_stencil.png'.format(party)
    mask = np.array(Image.open(path.join(d, stencil_filename)))

    stopwords = set(build_stop_words())

    wc = WordCloud(background_color="black", max_words=2000, mask=mask,
                   stopwords=stopwords)
    # generate word cloud
    wc.generate(text)

    # store to file
    cloud_filename = 'images/{}_masked_cloud.png'.format(party)
    wc.to_file(path.join(d, cloud_filename))

    # show
    plt.imshow(wc)
    plt.axis("off")
    plt.figure()
    plt.imshow(mask, cmap=plt.cm.gray)
    plt.axis("off")
    plt.show()

if __name__ == '__main__':

    with open('transcripts_df.pkl') as f:
        df = pickle.load(f)

    party = ['Republican','Democrat']

    for p in party:
        make_masked_cloud(df, p)

    #image sources: http://www.freestencilgallery.com/ , https://openclipart.org, http://www.spraypaintstencils.com/
