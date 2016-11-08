from os import path
from wordcloud import WordCloud
import cPickle as pickle

d = path.dirname(__file__)

with open('transcripts_df.pkl') as f:
    df = pickle.load(f)

text = df[df['speaker']=='B. CLINTON']['simple_content'].values.tolist()
text = ' '.join(text)

# Generate a word cloud image
wordcloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud)
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

# The pil way (if you don't have matplotlib)
#image = wordcloud.to_image()
#image.show()
