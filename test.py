import pandas as pd
import matplotlib.pyplot as plt

class PlotBarGraph():
    def __init__(self):
        df = pd.read_csv('output.csv')
        print(df.head(5))
        color_bar = ['g', 'r', 'y']
        plt.bar(df['Sentiment'], height=0, width=.1, color=color_bar)
        plt.xlabel('Sentiments')
        plt.ylabel('Frequency')
        plt.xticks(rotation=0)
        plt.show()
        plt.savefig('Sentiment_Graph.png')


