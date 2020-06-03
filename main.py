#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import tkinter as tk
from tkinter import *
from tkinter import Frame
import speech_recognition as sr
import time
from datetime import date
import os
from gtts import gTTS
import requests
from pprint import pprint
from newsapi import NewsApiClient
from random import randint
import threading
from pygame import mixer

"""import RPi.GPIO as GPIO


GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(bue_pin, GPIO.OUT)"""


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
city="Nantes"


mixer.init() # use mixer for control sound
fenetre= tk.Tk()  #initialisation of tkinter windows
fenetre.attributes('-fullscreen', 1)  #put windows on full size
fenetre.configure(background='black',cursor="none")   # put windows background to black and delate cursor

windows_size=os.system("xrandr  | grep \* | cut -d' ' -f4")  # get the size of screen use to place all the frame
windows_width  = fenetre.winfo_screenwidth()
windows_height = fenetre.winfo_screenheight()#/2         # delete /2 it's because I work with dual screen
#print("{} x {}".format(windows_width,windows_height))



meteo_frame=Frame(fenetre,bg="black",height="200", width="200",padx="2",pady="2")
meteo_frame.place(anchor= "nw")

actuality_frame=Frame(fenetre,bg="black",width="1000", height="400")
actuality_frame.place(x=50,y=windows_height-400,width="1100", height="400")

agenda_frame=Frame(fenetre,bg="black",height="50", width="50")
agenda_frame.place(x=windows_width-400,y=4,width="400")

music_frame=Frame(fenetre,bg="black")
music_frame.place(x=windows_width-400,y=windows_height-200, width="400", height="50")

welcome_frame=Frame(fenetre,bg="black",height=windows_height, width=windows_width,)
welcome_frame.pack()

"""
Dictionarry for all icon you need
"""

icon_lookup = {
    'clear sky': "weather_img/sun.png",  # clear sky day
    'wind': "weather_img/Wind.png",   #wind
    'light intensity drizzle': "weather_img/Cloud.png",  # cloudy day
    'broken clouds': "weather_img/PartlySunny.png",  # partly cloudy day
    'rain': "weather_img/Rain.png",  # rain day
    'snow': "weather_img/Snow.png",  # snow day
    'snow-thin': "weather_img/Snow.png",  # sleet day
    'fog': "weather_img/Haze.png",  # fog day
    'clear-night': "weather_img/Moon.png",  # clear sky night
    'partly-cloudy-night': "weather_img/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "weather_img/thunderstorm.png",  # thunderstorm
    'tornado': "weather_img/Tornado.png",    # tornado
    'hail': "weather_img/Hail.png",  # hail
    'play': "music/img/play.png",
    'pause': "music/img/pause.png",
}

def calendar():
    """
    fonction use to screen calendar
    """
    while True:
        show_agenda.config(text="Agenda")
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        today_event_list=["","","","","","","","","",""]
        event_list=["","","","","","","","","",""]
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        #print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        i=0
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            #print(start, event['summary'])
            start=start.split("T")
            date= start[0]
            hour= start[1]
            Date= time.strftime("%Y-%m-%d")
            if date == Date:
                event= hour+ " : "+str(event['summary'])
                today_event_list[i]=event
            else:
                event=date+ " : "+str(event['summary'])
                event_list[i]=event
            i+=1
        #print(event_list)
        #print(today_event_list)
        show_today.config(text="Aujourd'hui")
        show_event1.config(text=today_event_list[0])
        show_event2.config(text=today_event_list[1])
        show_event3.config(text=today_event_list[2])
        show_event4.config(text=today_event_list[3])
        show_event5.config(text=today_event_list[4])
        show_event6.config(text=today_event_list[5])
        show_event7.config(text=today_event_list[6])
        show_event8.config(text=today_event_list[7])
        show_event9.config(text=today_event_list[8])
        show_event1O.config(text=today_event_list[9])
        show_other.config(text="Autres")
        show_event11.config(text=event_list[0])
        show_event12.config(text=event_list[1])
        show_event13.config(text=event_list[2])
        show_event14.config(text=event_list[3])
        show_event15.config(text=event_list[4])
        show_event16.config(text=event_list[5])

def blague():
    id = randint(0,100)
    url="https://bridge.buddyweb.fr/api/blagues/blagues/"+str(id)
    response = requests.get(url)
    x=response.json()
    blague=str(x['blagues'])
    speak(blague)

def get_news():
    print("fqsflkdhsfksdfn;qsdnflksdhgkjfds,w")
    url = ('https://newsapi.org/v2/top-headlines?'
       'country=fr&'
       'apiKey=210159da0b834f55a97d2fc35c350201')
    response = requests.get(url)
    x=response.json()
    pprint(x)
    print(x.keys())
    pprint(x['articles'])

def weather():
    """
    fonction use to screen the weather
    """
    last_weather_description=""  # variable to check if weather have change 
    while True:
        Time= time.strftime("%A %d %B %Y %H:%M:%S")
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=eb6938fc6260909507ecb0f42cee3c7b".format(city)  #url for request
        r=requests.get(url)
        x=r.json()    # use json format
        y = x["main"]
        current_temperature = y["temp"] 
        current_humidiy = y["humidity"] 
        z = x["weather"] 
        weather_description = z[0]["description"]
        Temp= str(current_temperature) + " °C"
        Time= time.strftime("%H:%M:%S")
        Date= time.strftime("%A %d %B %Y")
        show_time.config(text=Time)
        show_temperature.config(text=Temp)
        show_date.config(text=Date)
        # if weather have changed change the wheather icon
        if weather_description!= last_weather_description:
            Image= PhotoImage(file=icon_lookup[weather_description])
            show_meteo.create_image(33,33,image=Image)
            last_weather_description=weather_description


def actuality():
    """
    fonction use to screen actuality
    """
    while True:
        show_actuality.config(text="Actualités")
        url = ('https://newsapi.org/v2/top-headlines?'
       'country=fr&'
       'apiKey=210159da0b834f55a97d2fc35c350201')  # url request
        response = requests.get(url) 
        x=response.json()
        # save the first 5 title into a list
        title_list=[]
        for i in range(0,5):
            article=x["articles"]
            article=article[i]
            title=article['title']
            title_list.append(title)
        # print the title on the screen
        show_actuality1.config(text=title_list[0])
        show_actuality2.config(text=title_list[1])
        show_actuality3.config(text=title_list[2])
        show_actuality4.config(text=title_list[3])
        show_actuality5.config(text=title_list[4])

def get_weather(location):
    """
    fonction use for get a weather of a city and speak the result
    """
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=eb6938fc6260909507ecb0f42cee3c7b".format(location)
    print(url)
    r=requests.get(url)
    x=r.json()
    print(x)
    if x["cod"] != "404": 
        y = x["main"] 
        current_temperature = y["temp"] 
        current_pressure = y["pressure"] 
        current_humidiy = y["humidity"]
        z = x["weather"] 
        weather_description = z[0]["description"] 
        weather=[weather_description,current_temperature]
        return current_temperature
    else:
        speak("Nous n'avons pas trouvez la ville")


def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='fr')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")

def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio, language="fr-FR")
        print("Vous avez dis: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data

def voice_assistant():
    while True:
        # Record Audio
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Please wait. Calibrating microphone...")  
            # listen for 5 seconds and create the ambient noise energy level  
            r.adjust_for_ambient_noise(source, duration=1)
            print("Say something!")
            audio = r.listen(source)

        # Speech recognition using Google Speech Recognition
        data = ""
        try:
            # Uses the default API key
            # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            data = r.recognize_google(audio, language="fr-FR")
            print("Vous avez dis: " + data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        if "blague" in data:
            blague()
        if "actualité" in data:
            get_news()
        if "comment tu vas" in data:
            speak("Je vais bien merci")

        if "heure" in data:
            heure=time.strftime("%H")
            minute=time.strftime("%M")
            speak("Il est {} heure {}".format(heure,minute))
        if "quel temps fait-il à" in data or "météo" in data:
            data = data.split(" ")
            print(data)
            location = data[len(data)-1]
            temp=get_weather(location)
            speak("il fait {} degré à {}".format(temp , location))
        if "musique" in data:
            random_song=os.listdir('music/song')
            print(random_song)
            i=randint(0,len(random_song)-1)
            show_title.configure(text=random_song[i])
            song="music/song/"+random_song[i]
            mixer.stop()
            print("je joue {}".format(song))
            Image= PhotoImage(file=icon_lookup["play"])
            play_button.create_image(24,24,image=Image)
            mixer.music.load(song)
            mixer.music.play()
        if "pause" in data:
            mixer.music.pause()
            Image= PhotoImage(file=icon_lookup["pause"])
            play_button.create_image(24,24,image=Image)

def welcome():
    """
    permet de sortir de veille 
    """
    print("welcome")
    time.sleep(5)
    welcome_frame.destroy()

# initialization
if __name__=="__main__":
    """show_welcome=tk.Label(welcome_frame,text="Welcome back",bg="black",foreground="white",font=("Courier", 44))
    show_welcome.pack()"""
    welcome=threading.Thread(target=welcome)
    welcome.start()
    """
    Meteo FRame
    """
    show_temperature= tk.Label(meteo_frame,text="",bg="black",foreground="white",font=("Courier", 20))
    show_time=tk.Label(meteo_frame,text="",bg="black",foreground="white",font=("Courier", 44))
    show_date=tk.Label(meteo_frame,text="",bg="black",foreground="white",font=("Courier", 20))
    show_meteo = tk.Canvas(meteo_frame,width=66,height=66,bg='black',highlightthickness=0)
    show_time.pack()
    show_date.pack()
    show_temperature.pack()
    show_meteo.pack()
    meteo=threading.Thread(target=weather)
    meteo.start()
    """
    Actality Frame
    """
    show_actuality= tk.Label(actuality_frame,text="Actuality",bg="black",foreground="white",font=("Courier", 20))
    show_actuality.pack()
    show_actuality1= tk.Label(actuality_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_actuality1.pack()
    show_actuality2= tk.Label(actuality_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_actuality2.pack()
    show_actuality3= tk.Label(actuality_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_actuality3.pack()
    show_actuality4= tk.Label(actuality_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_actuality4.pack()
    show_actuality5= tk.Label(actuality_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_actuality5.pack()

    actuality=threading.Thread(target=actuality)
    actuality.start()

    """
    Agenda Frame
    """
    calendar=threading.Thread(target=calendar)
    show_agenda= tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 20))
    show_agenda.pack()
    show_today= tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 15))
    show_today.pack()
    show_event1=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event1.pack()
    show_event2=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event2.pack()
    show_event3=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event3.pack()

    show_event4=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event4.pack()

    show_event5=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event5.pack()

    show_event6=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event6.pack()

    show_event7=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event7.pack()

    show_event8=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event8.pack()

    show_event9=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event9.pack()

    show_event1O=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event1O.pack()

    show_other=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 15))
    show_other.pack()

    show_event11=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event11.pack()

    show_event12=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event12.pack()

    show_event13=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event13.pack()

    show_event14=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event14.pack()

    show_event15=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event15.pack()

    show_event16=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event16.pack()

    calendar.start()

    """
    music player
    """
    """music = Music()
    music.play()"""

    show_title=tk.Label(music_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_title.pack()

    album_picture=tk.Canvas(music_frame,width=66,height=66,bg='black',highlightthickness=0)
    album_picture.pack()

    play_button = tk.Canvas(music_frame,width=66,height=66,bg='black',highlightthickness=0)
    #Image= PhotoImage(file=icon_lookup["pause"])
    """play_button.create_image(50,50,image=Image)"""
    play_button.pack()
    """
    voice assistant
    """
    voice_assist=threading.Thread(target=voice_assistant)
    voice_assist.start()

    fenetre.mainloop()
