import kivy
kivy.require('1.9.0')
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooser, FileChooserListLayout, FileChooserIconLayout
from Predictor import Demo
import Predictor
from threading import Thread

class MainScreen(Screen):

    def predict(self, user_input, prediction):
        updated_rating, updated_sentiment = Demo().get_text(str(user_input.text))
        if updated_sentiment == 0:
            updated_sentiment = 'Negative'
        elif updated_sentiment == 1:
            updated_sentiment = 'Neutral'
        else:
            updated_sentiment = 'Positive'

        rate_text = '* '*updated_rating
        prediction.text = rate_text+' ('+str(updated_rating)+".0)\n"+updated_sentiment
    def btn_touch_up(self):
        from subprocess import Popen, PIPE
        secondApp = Popen('python FileExplorer.py', shell=True)

class LandingScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file('SentimentAnalyser.kv')

class FinalApp(App):
    def build(self):
        return presentation

if __name__ == '__main__':
    Demo().load_model()
    FinalApp().run()
