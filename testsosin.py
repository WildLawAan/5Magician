#!/usr/bin/env python
#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#  lcd_i2c.py
#  LCD test script using I2C backpack.
#  Supports 16x2 and 20x4 screens.
#
# Author : Matt Hawkins
# Date   : 20/09/2015
#
# http://www.raspberrypi-spy.co.uk/
#
# Copyright 2015 Matt Hawkins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------
import smbus
import time
import RPi.GPIO as GPIO
import os
import vlc
from ftplib import FTP
import random
comlist=os.listdir("/home/pi/Music")
ftp = FTP("192.168.0.107","root","raspberry")

def download(filename):
    #ftp.pwd()

    local_filename = os.path.join("/home/pi/Music/"+filename)
    If=open(local_filename,"wb")
    ftp.retrbinary("RETR "+filename, If.write, 1024)
    If.close()
def down():
    i=0
    newone=False
    #ftp.retrlines("LIST")
     
    ftp.cwd("/music2")
     
    listing=[]
     
    ftp.retrlines("LIST",listing.append)

    print(listing)
     
    while i<len(listing):
        isthere=False
        word = listing[i].split(None,8)
        print(word)
        filename=word[-1].lstrip()
        print(filename)
        for localname in comlist:
            if (localname==filename and isthere==False):
                isthere=True
        if (isthere==False):
            download(filename)
            newone=True
        i+=1
    return True

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display
  

  message = message.rjust(LCD_WIDTH," ")
  

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def main():
  index = open('index2.txt','r')
  indexcontent = int(index.read())
  index.close()
  
  # Main program block
  downloading=False

  lcd_string(" DOWNLOADING...",LCD_LINE_1)
  lcd_string(" Please Wait...",LCD_LINE_2)
  downloading=down()
  time.sleep(10)

  # Initialise display
  lcd_init()
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(20, GPIO.IN)
  GPIO.setup(21, GPIO.IN)
  GPIO.setup(23, GPIO.IN)
  GPIO.setup(24, GPIO.IN)
  GPIO.setup(16, GPIO.IN)


  path = "/home/pi/Music/"

  mlist = os.listdir(path)

  instance = vlc.Instance()

  player=instance.media_player_new()

  sunse=indexcontent
  #txt STORAGE

  #txt file save
 
  

  media=instance.media_new("/home/pi/Music/"+mlist[sunse])

  player.set_media(media)

  player.play()

  time.sleep(1)
     
  a = player.get_state()
  k=0
  while downloading:
      
      if(k==12):
          k=0
      a = player.get_state()
      k=k+1
      time.sleep(0.2)
      lcd_string(mlist[sunse]+ str(" ")*k,LCD_LINE_1)
      lcd_string(str(a)+ str(" ")*k,LCD_LINE_2)
      
      if (a==3):
          if GPIO.input(16) == 0 :
              sunse=random.randint(0,len(mlist)-1)
              media=instance.media_new("/home/pi/Music/"+mlist[sunse])
              player.set_media(media)
              if (len(mlist[sunse])>=10):
                  lcd_string(mlist[sunse][:8]+ str(" ")*k, LCD_LINE_1)
                  time.sleep(2)
            
                  lcd_string(mlist[sunse][8:]+ str(" ")*k, LCD_LINE_1)
                  lcd_string(str(a)+str(" ")*k,LCD_LINE_2)
              else:
                  lcd_string(mlist[sunse]+ str(" ")*k,LCD_LINE_1)
                  lcd_string(str(a)+ str(" ")*k,LCD_LINE_2)
              player.play()
              time.sleep(1)
              k=k+1
              
      if a== 6:
          sunse=sunse+1
          if sunse==len(mlist):
              sunse=0
          media=instance.media_new("/home/pi/Music/"+mlist[sunse])
          player.set_media(media)
          if (len(mlist[sunse])>=10):
              lcd_string(mlist[sunse][:8]+ str(" ")*k, LCD_LINE_1)
              time.sleep(2)
              
              lcd_string(mlist[sunse][8:]+ str(" ")*k, LCD_LINE_1)
              lcd_string(str(a)+str(" ")*k,LCD_LINE_2)
          else:
              lcd_string(mlist[sunse]+ str(" ")*k,LCD_LINE_1)
              lcd_string(str(a)+ str(" ")*k,LCD_LINE_2)
          player.play()
          
          time.sleep(1)
          k=k+1
          
           
      if a == 5:
          break
            
      if GPIO.input(20) == 0 :
        #back
         k=0
         player.stop()
         sunse=sunse-1
         if sunse==-1:
             sunse=len(mlist)-1
         media=instance.media_new("/home/pi/Music/"+mlist[sunse])

         player.set_media(media)

         player.play()
         if (len(mlist[sunse])>=10):
             lcd_string(mlist[sunse][:8]+ str(" ")*k, LCD_LINE_1)
             time.sleep(2)
             
             lcd_string(mlist[sunse][8:]+ str(" ")*k, LCD_LINE_1)
             lcd_string(str(a)+str(" ")*k,LCD_LINE_2)
         else:
             lcd_string(mlist[sunse] + str(" ")*k ,LCD_LINE_1)
             lcd_string(str(a) + str(" ")*k ,LCD_LINE_2)
            
                 
         a = player.get_state()
         time.sleep(1)
         k=k+1
      if GPIO.input(21) == 0 :
          k=0
          #go
          player.stop()
          sunse=sunse+1
          if sunse==len(mlist):
              sunse=0
          media=instance.media_new("/home/pi/Music/"+mlist[sunse])
          player.set_media(media)
          player.play()
          if (len(mlist[sunse])>=10):
              lcd_string(mlist[sunse][:8]+ str(" ")*k, LCD_LINE_1)
              time.sleep(2)
              
              lcd_string(mlist[sunse][8:]+ str(" ")*k, LCD_LINE_1)
              lcd_string(str(a)+str(" ")*k,LCD_LINE_2)
          else:
              lcd_string(mlist[sunse] + str(" ")*k,LCD_LINE_1)
              lcd_string(str(a) + str(" ")*k ,LCD_LINE_2)
          
          time.sleep(1)
          k=k+1

      if GPIO.input(23) == 0 :
          k=0
          #pause
          player.pause()
          a = player.get_state()
          if (len(mlist[sunse])>=10):
              lcd_string(mlist[sunse][:8]+ str(" ")*k, LCD_LINE_1)
              time.sleep(2)
              k=1
              lcd_string(mlist[sunse][8:]+ str(" ")*k, LCD_LINE_1)
              lcd_string(str(a)+str(" ")*k,LCD_LINE_2)
          else:
              lcd_string(mlist[sunse] + str(" ")*k ,LCD_LINE_1)
              lcd_string(str(a) + str(" ")*k ,LCD_LINE_2)
          
          time.sleep(1)
          k=k+1
          
      if GPIO.input(24) == 0 :
          #shutdown
          a = player.get_state()
          if a == 3:
              player.stop()
  os.remove("/home/pi/Desktop/index2.txt")
  indexnum=str(sunse)
  index = open('index2.txt','w')
  index.write(indexnum)
  index.close()
   
   
    


if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)




