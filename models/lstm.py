import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../output/total_phrases_labelled_train.csv')
df.isnull().sum()
#drop french phrases and extra data
df = df.dropna()
df.isnull().sum()


from collections import Counter

#count unique words
def counter_word(text):
    count = Counter()
    for i in text.values:
        for word in i.split():
            count[word] += 1
    return count

text = df['Phrase']
counter = counter_word(text)
print(len(counter))
num_words = len(counter)

#max number of words in a sequence
#replace with length of longest string
max_length = 30

def split_train_test(features, target, size):
    #size is the size of the training set
    train_size = int(features.shape[0]* size) #check me
    X_train = features[:train_size]
    y_train = target[:train_size]

    X_test = features[train_size:]
    y_test = target[train_size:]
    return X_train, y_train, X_test, y_test


train = df[['Phrase','Target']]
features = train['Phrase']
target = train['Target']
X_train, y_train, X_test, y_test = split_train_test(features, target, 0.8)

from keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(X_train)
word_index = tokenizer.word_index


train_sequences = tokenizer.texts_to_sequences(X_train)

from keras.preprocessing.sequence import pad_sequences
train_padded = pad_sequences(
    train_sequences, maxlen=max_length, padding="post", truncating="post"
)

test_sequences = tokenizer.texts_to_sequences(X_test)
test_padded = pad_sequences(
    test_sequences, maxlen=max_length, padding="post", truncating="post"
)


from tqdm import tqdm
from keras.layers import Dense,SpatialDropout1D
from nltk.tokenize import word_tokenize

tokenizer_obj=Tokenizer()
"""Creates corpus from feature column, which is a pandas series"""
def create_corpus(df):
    corpus=[]
    for phrase in tqdm(df['Phrase']):
        words=[word.lower() for word in word_tokenize(phrase) if(word.isalpha()==1)]
        corpus.append(words)
    return corpus


"""Creates an embedding dictionary using GloVe"""
embedding_dict={}
with open('/Users/vankhaido/glove.6B.100d.txt','r') as f:
    for line in f:
        values=line.split()
        word=values[0]
        vectors=np.asarray(values[1:],'float32')
        embedding_dict[word]=vectors
f.close()

"""Create padded sequences of equal lenght as input to LSTM"""
def create_padded_inputs(corpus):
    MAX_LEN=30
    tokenizer_obj.fit_on_texts(corpus)
    sequences=tokenizer_obj.texts_to_sequences(corpus)

    phrase_pad=pad_sequences(sequences,maxlen=MAX_LEN,truncating='post',padding='post')
    return phrase_pad