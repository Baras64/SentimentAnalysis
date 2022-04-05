from kivy.app import App
from kivy.uix.screenmanager import Builder, ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import pandas as pd
from Predictor import Demo
import matplotlib.pyplot as plt
import os
import CsvFileException

class MainScreen(Screen):
    df = ''
    path1 = ''
    def load(self, path, selection):
        global df
        global path1
        path1 = selection[0]
        try:
            if os.path.basename(path1).split('.')[1] == 'csv':
                df = pd.read_csv(selection[0])
                self.clear_widgets()
                gd = GridLayout()
                gd.cols = df.shape[1]
                self.add_widget(gd)

                for i in range(0, gd.cols):
                    test = 'Select=>'+str(df.columns[i])
                    btn = Button(text=test)
                    btn.font_size = 12
                    gd.add_widget(btn)
                    btn.bind(on_press = self.callback)
                for i in range(0, 10):
                    X = df.iloc[i].values
                    for j in range(0, gd.cols):
                        test = str(X[j])
                        gd.add_widget(Label(text=test))
            else:
                raise(Exception)
        except Exception as e:
            print('Please Select a CSV file')
            pass

    def callback(self, event):
        selected_col = event.text.split('=>')
        MainScreen.clear_widgets(self)
        ratings, sentiments, s_conf = Demo().get_path(df, selected_col[1], path1)
        gd = GridLayout(cols=4)
        self.add_widget(gd)
        gd.add_widget(Label(text='Review Text'))
        gd.add_widget(Label(text='Ratings'))
        gd.add_widget(Label(text='Sentiment'))
        gd.add_widget(Label(text='Sentiment Confidence'))
        for i in range(0, 15):
            review_text = df[selected_col[1]][i][:20]
            pred_rate = str(ratings[i])
            pred_sent = str(sentiments[i])
            pred_s = str(round(float(s_conf[i])*100, 2))
            clr = []
            clr_rate = []
            if pred_sent == 'Positive':
                clr = [0, 1, 0, 1]
            elif pred_sent == 'Negative':
                clr = [1, 0, 0, 1]
            else:
                clr = [0, 0, 1, 1]

            if pred_rate == '4' or pred_rate == '5':
                clr_rate = [0, 1, 0, 1]
            elif pred_rate == '1' or y_pred == '2':
                clr_rate = [1, 0, 0, 1]
            else:
                clr_rate = [0, 0, 1, 1]
            gd.add_widget(Label(text=review_text))
            gd.add_widget(Label(text=pred_rate, color=clr_rate))
            gd.add_widget(Label(text=pred_sent, color=clr))
            gd.add_widget(Label(text=pred_s))

        from test import PlotBarGraph
        PlotBarGraph()


presentation = Builder.load_file('FileExplorer.kv')


class FileExplorerApp(App):
    def build(self):
        return presentation

if __name__ == '__main__':
    FileExplorerApp().run()