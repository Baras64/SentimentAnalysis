import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import h5py
import joblib
import re
import unicodedata
import matplotlib
path1 = ""

class Demo:
    model = None
    tokenizer = None

    def load_model(self):
        global model
        global tokenizer
        tokenizer = joblib.load('tokenizer.pickle')
        model = tf.keras.models.load_model("Conv1LSTM1.h5")

    def convert(self, sentence):
        sentence = self.preprocess(sentence)
        print(sentence)
        tokenized_sent = tf.keras.preprocessing.text.text_to_word_sequence(sentence)
        tokenized_sent = tokenizer.texts_to_sequences([sentence])
        tokenized_sent = tf.keras.preprocessing.sequence.pad_sequences(tokenized_sent, maxlen=75, padding='post', truncating='pre')
        return tokenized_sent

    def get_text(self, msg):
        y_pred = model.predict(self.convert(msg))
        return np.argmax(y_pred[0])+1, np.argmax(y_pred[1])

    def get_text_array(self, msg_array):
        y_pred = model.predict(msg_array, verbose=1)
        return y_pred

    def unicode_to_ascii(self, s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    def preprocess(self, w):
        w = self.unicode_to_ascii(w.lower().strip())
        w = re.sub(r"([?.!,¿])", r" \1 ", w)
        w = re.sub(r'[" "]+', " ", w)
        w = re.sub(r"newlinechar", "", w)
        w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)
        w = w.rstrip().strip()
        return w

    def get_path(self, dataset, selected_col, path1):
        self.load_model()
        df = pd.DataFrame(dataset)
        sent = tokenizer.texts_to_sequences(df[selected_col].apply(self.preprocess))
        sent = tf.keras.preprocessing.sequence.pad_sequences(sent, padding='post', maxlen=75, truncating='pre')
        result = self.get_text_array(sent)
        sentiment = []
        rating = []
        sentiment_confidence = []
        for i in range(len(result[0])):
            y_pred = result[0]
            y_pred1 = result[1]
            rating.append(np.argmax(y_pred[i]) + 1)
            sentiment_hat = np.argmax(y_pred1[i])
            sentiment_confidence.append(max(np.array(y_pred1)[i]))
            if sentiment_hat == 0:
                sentiment.append('Negative')
            elif sentiment_hat == 1:
                sentiment.append('Neutral')
            else:
                sentiment.append('Positive')

        df['Ratings'] = rating
        df['Sentiment'] = sentiment
        df.to_csv('output.csv', index=False)

        print('h')
        print(df['Sentiment'])
        # ax = df['Sentiment'].value_counts().plot(kind='bar', figsize=(8, 5))
        # ax.set_xlabel('Sentiment')
        # ax.set_ylabel('Frequency')
        pd.value_counts(df['Sentiment'].values).plot.bar()

        return rating, sentiment, sentiment_confidence