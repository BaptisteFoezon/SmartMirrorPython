import os
"""
permet de telecharger tout les module et configuration que l'on à besoin
"""
os.syteme("sudo apt-get update")
#install tkinter 
os.system("sudo apt-get install python-tk")

#install google text to speech
os.system("pip install gTTS")

#install speechRecognition
os.system("sudo pip3 install SpeechRecognition")
choice=input("Are you shure wou want to execute automaticaly Samrt_Miror when raspberry boot ? Y/N")

if choice=="Y" or choice=="y":
    os.system("sudo nano /etc/rc.local") 
    with open("sudo nano /etc/rc.local","r")as file:
        content=[]
        for ligne in file:
            content.append(ligne)
        content.index("# Print the IP address")  # on veux ajouter la comande juste avant


    add="sudo python /home/pi/SmartMiror/main.py.py"
