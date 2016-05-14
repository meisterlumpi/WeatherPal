# -*- coding: utf-8 -*-

import kivy
import time
import threading
# import os
import unicodedata
# import urllib
# import cStringIO
# import random

# import MyKeyboardListener
# from MyKeyboardListener import *

# import "Config" and set window size
from kivy.config import Config
# config stuff has to be set before other imports for some reason
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'borderless', '0')
# Config.set('graphics', 'fullscreen', '1')  # run app fullscreen

# Config.set('kivy', 'keyboard_mode', 'systemandmulti')
Config.set('kivy', 'keyboard_mode', 'dock')


Config.write()

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle, Line
# from kivy.uix.scrollview import ScrollView
from kivy.uix.carousel import Carousel
# from kivy.uix.image import AsyncImage
# from kivy.uix.vkeyboard import VKeyboard
from kivy.clock import Clock, _default_time as def_time  # mainthread
# from kivy.event import EventDispatcher
from kivy.base import runTouchApp
# from kivy.properties import ListProperty
# from functools import partial
# from Queue import Queue
from pyowm import OWM
from pyowm.exceptions import api_call_error

# check kivy version
kivy.require('1.0.8')

# temporary global parameters
API_key = '<enter api key here>'    # OpenWeatherMap API key
location_str = 'Hallbergmoos, DE'               # location for which to check weather
language_str = 'de'                             # language
owm_fetch_sleep_time = 120                      # in seconds

# MAX_TIME = 1/60.

# load layout file
Builder.load_file("Main.kv")


# declare both screens
class HomeScreen(Screen):
    def __init__(self, name):
        super(HomeScreen, self).__init__()
        self.name = name
        self.location_str_prev = None
        self.ref_time_prev = None
        self.owm_ico_base_path = 'images\icons\openweathermap'


    @staticmethod
    def toggle_fullscreen():
        Window.fullscreen = not Window.fullscreen

    def update_screen_owm(self, weather):

        ref_time = weather.get_reference_time()

        # this could be done better
        if self.location_str_prev != location_str or self.ref_time_prev != ref_time:
            self.location_str_prev = location_str
            self.ref_time_prev = ref_time

            self.lbl_city.text = location_str

            img_file_name = unicodedata.normalize('NFKD', weather.get_weather_icon_name()).encode('ascii', 'ignore')
            img_file_path = self.owm_ico_base_path + '\\' + img_file_name + '.png'

            self.img_weather_icon.source = img_file_path


            temp = weather.get_temperature(unit='celsius')

            self.lab_2.text = weather.get_reference_time(timeformat='iso')
            self.lbl_temp.text = ("Temp: " + "{:.2f} °C".format(temp.get('temp')) + '\n' +
                                  "Temp (min): " + "{:.2f} °C".format(temp.get('temp_min')) + '\n' +
                                  "Temp (max): " + "{:.2f} °C".format(temp.get('temp_max')))

            print(weather.get_reference_time())                             # get time of observation in GMT UNIXtime
            print(weather.get_reference_time(timeformat='iso'))             # ...or in ISO8601
            print(weather.get_clouds())                                     # Get cloud coverage
            print(weather.get_rain())                                       # Get rain volume
            print(weather.get_snow())                                       # Get snow volume
            print(weather.get_wind())                                       # Get wind degree and speed



class SettingsScreen(Screen):
    def __init__(self, name):
        super(SettingsScreen, self).__init__()
        self.name = name

    @staticmethod
    def get_location():
        return location_str

    def set_location(self):
        global location_str

        new_location_str = self.tb_location.text
        if new_location_str == location_str:
            print 'location_str was not changed'
        else:
            location_str = new_location_str
            print 'location_str was changed to ' + location_str


class DrawScreen(Screen):
    def on_touch_down(self, touch):
        print(touch)
        with self.canvas:
            touch.ud["line"] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        print(touch)
        touch.ud["line"].points += (touch.x, touch.y)

    def on_touch_up(self, touch):
        print(touch)


class OWMLink:
    def __init__(self, instance):
        self.instance = instance
        self.link = OWM(API_key, language=language_str)  # setup OpenWeatherMap connection
        self.keep_running = True

    def run(self):
        con_error_cnt = 0
        while self.keep_running:
            print 'connecting to weather'
            try:
                owm_is_online = self.link.is_API_online()
            except:  # api_call_error.APICallError
                con_error_cnt += 1
                print 'connection to OWM API failed'
                if con_error_cnt < 10:
                    print 'will try again in 2 seconds'
                    time.sleep(2)  # wait 2 seconds before trying it again
                    continue
                else:
                    # quit if connection could not be est. 10 times in a row
                    print 'OWM API seems to be offline, quitting'
                    break
            con_error_cnt = 0  # reset connection error counter if connection was successful
            if owm_is_online:
                obs = self.link.weather_at_place(location_str)
                App.get_running_app().owm_thread_weather = obs.get_weather()
            else:
                App.get_running_app().owm_thread_weather = None
                print('OWM service is offline')
            time.sleep(owm_fetch_sleep_time)  # should be last statement in while loop


class CarouCntrl(Widget):
    # root
    def __init__(self):
        super(CarouCntrl, self).__init__()

        # init screens
        self.home_screen = HomeScreen(name='home')
        self.settings_screen = SettingsScreen(name='settings')
        # self.draw_screen = DrawScreen(name='draw')

        # init carousel
        self.carousel = Carousel(direction='right', loop=True)

        # add widgets to carousel
        # for i in range(3):
        #     self.carousel.add_widget(self.home_screen)

        self.carousel.add_widget(self.home_screen)
        self.carousel.add_widget(self.settings_screen)
        # self.carousel.add_widget(self.draw_screen)

        # start getting data from OWM
        self.owm_link = OWMLink(self)
        self.owm_thread = threading.Thread(target=self.owm_link.run, args=())
        self.owm_thread.start()

    def shutdown(self):
        self.owm_link.keep_running = False


class MainApp(App):

    owm_thread_weather = None

    def __init__(self):
        super(MainApp, self).__init__()
        self.CarouCntrl = CarouCntrl()

    def build(self):
        Clock.schedule_interval(self.owm_thread_grab, 2)

        # return carousel on desktop computers
        return self.CarouCntrl.carousel
        # return carousel as touch app if on Android/iOS
        #return runTouchApp(self.CarouCntrl.carousel)  # introd. event handler --> not necessary, kivy.config for touch keyboard is enough?

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.CarouCntrl.shutdown()
        print 'program will now exit'

    def load_next_slide(self):
        self.root.load_next(mode='next')

    # def owm_thread_grab(self, *args):
    def owm_thread_grab(self, *args):
        if self.owm_thread_weather is None:
            # weather from OpenWeatherMap was not requested yet or it could ne be retrieved
            # indicate to user?
            print 'weather from OpenWeatherMap was not requested yet or it could not be retrieved'
        else:
            # while def_time() < (Clock.get_time() + MAX_TIME):
            self.CarouCntrl.home_screen.update_screen_owm(self.owm_thread_weather)

if __name__ == "__main__":
    MainApp().run()
