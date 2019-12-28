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

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


city="Nantes"


fenetre= tk.Tk()
fenetre.attributes('-fullscreen', 1)
fenetre.configure(background='black',cursor="none")

windows_size=os.system("xrandr  | grep \* | cut -d' ' -f4")
windows_width  = fenetre.winfo_screenwidth()
windows_height = fenetre.winfo_screenheight()/2         # delete /2 it's because I work with dual screen
print("{} x {}".format(windows_width,windows_height))

meteo_frame=Frame(fenetre,bg="black",height="200", width="200",padx="2",pady="2")
meteo_frame.place(anchor= "nw")

actuality_frame=Frame(fenetre,bg="black",width="1000", height="400")
actuality_frame.place(x=50,y=windows_height-400,width="1100", height="400")

agenda_frame=Frame(fenetre,bg="black",height="50", width="50")
agenda_frame.place(x=windows_width-400,y=4,width="400")

music_frame=Frame(fenetre,bg="green",height="50", width="50")
music_frame.place(anchor= "e")


icon_lookup = {
    'clear sky': "weather_img/sun.png",  # clear sky day
    'wind': "weather_img/Wind.png",   #wind
    'cloudy': "weather_img/Cloud.png",  # cloudy day
    'overcast clouds': "weather_img/PartlySunny.png",  # partly cloudy day
    'rain': "weather_img/Rain.png",  # rain day
    'snow': "weather_img/Snow.png",  # snow day
    'snow-thin': "weather_img/Snow.png",  # sleet day
    'fog': "weather_img/Haze.png",  # fog day
    'clear-night': "weather_img/Moon.png",  # clear sky night
    'partly-cloudy-night': "weather_img/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "weather_img/thunderstorm.png",  # thunderstorm
    'tornado': "weather_img/Tornado.png",    # tornado
    'hail': "weather_img/Hail.png"  # hail
}

def calendar():
    show_agenda.config(text="Agenda")
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    event_list=[]
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
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        event=start+event['summary']
        event_list.append(event)
    show_event1.config(text=event_list[0])
    show_event2.config(text=event_list[1])
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
    last_weather_description=""
    while True:
        Time= time.strftime("%A %d %B %Y %H:%M:%S")
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=eb6938fc6260909507ecb0f42cee3c7b".format(city)
        r=requests.get(url)
        x=r.json() 
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
        if weather_description!= last_weather_description:
            Image= PhotoImage(file=icon_lookup[weather_description])
            show_meteo.create_image(33,33,image=Image)
            last_weather_description=weather_description

def actuality():
    while True:
        show_actuality.config(text="Actualitées")
        url = ('https://newsapi.org/v2/top-headlines?'
       'country=fr&'
       'apiKey=210159da0b834f55a97d2fc35c350201')
        response = requests.get(url)
        x=response.json()
        title_list=[]
        for i in range(0,5):
            article=x["articles"]
            article=article[i]
            title=article['title']
            title_list.append(title)
        show_actuality1.config(text=title_list[0])
        show_actuality2.config(text=title_list[1])
        show_actuality3.config(text=title_list[2])
        show_actuality4.config(text=title_list[3])
        show_actuality5.config(text=title_list[4])

def get_weather(location):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=eb6938fc6260909507ecb0f42cee3c7b".format(location)
    print(url)
    r=requests.get(url)
    x=r.json()
    print(x)
    if x["cod"] != "404": 
        # store the value of "main" 
        # key in variable y 
        y = x["main"] 
    
        # store the value corresponding 
        # to the "temp" key of y 
        current_temperature = y["temp"] 
    
        # store the value corresponding 
        # to the "pressure" key of y 
        current_pressure = y["pressure"] 
    
        # store the value corresponding 
        # to the "humidity" key of y 
        current_humidiy = y["humidity"] 
    
        # store the value of "weather" 
        # key in variable z 
        z = x["weather"] 
    
        # store the value corresponding  
        # to the "description" key at  
        # the 0th index of z 
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
            minrequte=time.strftime("%M")
            speak("Il est {} heure {}".format(heure,minute))
        if "quel temps fait-il à" in data or "météo" in data:
            data = data.split(" ")
            print(data)
            location = data[len(data)-1]
            temp=get_weather(location)
            speak("il fait {} degré à {}".format(int(temp) , location))



# initialization
if __name__=="__main__":
    voice_assist=threading.Thread(target=voice_assistant)
    voice_assist.start()
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
    show_event1=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event1.pack()
    show_event2=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event2.pack()
    show_event3=tk.Label(agenda_frame,text="",bg="black",foreground="white",font=("Courier", 10))
    show_event3.pack()
    calendar.start()

    fenetre.mainloop()
