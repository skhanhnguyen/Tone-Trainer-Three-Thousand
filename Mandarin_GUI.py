# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.properties import OptionProperty
from kivy.core.text import LabelBase
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.popup import Popup
from pymatbridge import Matlab
import pyaudio
import audio_test
import wave
import random
import numpy as np
import pickle
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


from kivy.core.audio import SoundLoader

mlab = Matlab()
mlab.start()

sound = SoundLoader.load('oriental_bgm.wav')
sound.volume = 0.3
if sound:
    print("Sound found at %s" % sound.source)
    print("Sound is %.3f seconds" % sound.length)
    
def check_sound(dt=None):
    sound.play()

sound.play()
Clock.schedule_interval(check_sound,22 )


fileObject = open('pinyin_to_character_dict','rb')
pinyin_to_character_dict = pickle.load(fileObject)

fileObject2 = open('okmodel2.sav','rb')
okmodel = pickle.load(fileObject2)

KIVY_FONTS = [
    {
        "name": "chinese_font",
        "fn_regular": "chinese_font.ttf",
    }
]

history = []



for font in KIVY_FONTS:
    LabelBase.register(**font)
    



class MainScreen(Screen):
    pass

class HistoryScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

class MainScreenLayout(BoxLayout):
    pass

class HistoryScreenLayout(BoxLayout):
    pass
    
class DisplayScreen(BoxLayout):

    def __init__(self,**kwargs):
        super(DisplayScreen,self).__init__(**kwargs)
        self.pinyin = self.PinyinGenerator()
        try:
            self.character = random.choice(pinyin_to_character_dict[self.pinyin])
            #print(self.character)
        except:
            self.character = ' '
        
        self.feedback = 'Press the record button'
        self.recorded_tone= 4
        self.image = 'soundwave.png'
        
    def NewQuestion(self):
        #add the current question to history
        history.append('{}    {}    {}'.format(self.ids.PinyinDisplay.text,self.ids.Character.text,1))
       # print(history)
        app = App.get_running_app()
        app.root.ids.History.ids.HistoryScreenLayout.ids.Scroll.text = '\n'.join(history)
        ##print ( app.root.ids.History.ids.HistoryScreenLayout.ids.Scroll.text )
        
        #update the question
        a = self.PinyinGenerator()
        try:
            self.character = random.choice(pinyin_to_character_dict[a])
            #print(self.character)
            self.ids.Character.text = self.character
        except:
            self.character =' '
            self.ids.Character.text = self.character

        self.ids.PinyinDisplay.text = a
        self.ids.Feedback.text = 'Press the record button'
        self.ids.Feedback.color = (1,1,1,1)
        
    def RecordAndCheck(self):
        self.ids.Feedback.text = 'Speak into the Microphone'
        #start recording input: audio output:nparray
        Clock.schedule_once(self.check,1)

    def check(self,dt):
        self.audio,RECORD_SECONDS = audio_test.audio_to_nparray()
        self.ids.Feedback.text ='Processing...'
        x_axis = np.linspace(0,RECORD_SECONDS,len(self.audio))
        soundwave = plt.plot(x_axis,self.audio)
        plt.axis('off')
        plt.savefig('soundwave.png',transparent = True)
        plt.clf()
        
        res = mlab.run_func('pitchcontour2.m',{'arg1':np.array([self.audio]).transpose()}) #ans is a matrix not vector
       # pitch_contour = [273.35,291.57,291.57,291.57,291.57	291.57	273.35	18.223	18.223	18.223
        pitch_contour = res['result']
        pitch_contour = pitch_contour.reshape(21)
        tone = okmodel.predict(pitch_contour)
        print(pitch_contour)
        print(tone)
        
        
        self.ids.Soundwave.reload()
        #print(self.audio)
        

        #analyze the output
        #classifier required... input: nparray output tone 
        
        if int(self.ids.PinyinDisplay.text[-1])==tone:
            self.ids.Feedback.text = 'You are correct!'
            self.ids.Feedback.color = (0,1,0,1)
        else:
            self.ids.Feedback.text = 'Try again'
            self.ids.Feedback.color = (1,0,0,1)
            
    def Play(self):
        filename = self.ids.PinyinDisplay.text[-1]+self.ids.PinyinDisplay.text[:-1]
        try:
            audio_test.play_audio(filename)
        except:
            self.ids.Feedback.text = 'Sorry! No Audio file!'
        
    
    def PinyinGenerator(self):
    #return string showing pinyin 
        with open('all_mandarin_pinyin_trimmed.txt','r') as f:
            pinyinList = f.read().split(' ')
            syllable = random.choice(pinyinList)
        tone = random.choice(['1','2','3','4'])
        
        return syllable+tone
    
    def history_popup(self):
        pop = Popup(title='History',content=Label(text='\n'.join(history[-5:]),font_name='chinese_font',font_size =30),size_hint=(0.5,0.5))
        pop.open()
#plt.plot([1, 23, 2, 4])
#plt.ylabel('some numbers')

class MandarinTrainer(App):
    
    def __init__(self,**kwargs):
        super(MandarinTrainer,self).__init__(**kwargs)
        self.history = StringProperty()
        
        
    def build(self):
#        box = BoxLayout()
#        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return ScreenManagement()

MandarinTrainer().run()
mlab.stop()