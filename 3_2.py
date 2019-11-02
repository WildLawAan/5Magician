#!/usr/bin/env python
import vlc
import time
import RPi.GPIO as GPIO
import os

file = "/home/pi/Desktop/snow.wav"

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)

instance = vlc.Instance()

player=instance.media_player_new()

media=instance.media_new(file)

player.set_media(media)

player.play()

time.sleep(10)

a=player.get_state()




while True:
    if a==5:
        break
    if(GPIO.input(23)==0):
        a=player.get_state()
        print( "BUtton Pressed!")
        player.pause()
        time.sleep(1)

    if(GPIO.input(24)==0):
        a=player.get_state()
        if(a==3):
            print("exit button press")
           
            player.stop()
            


    
    
    

