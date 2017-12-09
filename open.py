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
  

    message = message.ljust(LCD_WIDTH," ")
  

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

def sound(number):
    player.audio_set_volume(number)

def starter():
    index = open('index4.txt','r')
    channelk = index.readline()
    channels = int (channelk)
    listnumk = index.readline()
    listnums = int (listnumk)
    title = index.readline()
    index.close()
    if(serverlist[channels][listnums] == title):
        return channels,listnums
        
    else:
        return 0,1

def sunsetype(listnum, playmode, button,ranlist):
    if(playmode % 3 == 0):
        if(button == 1):
            return listnum+1
        if(button == -1):
            return listnum-1

    if(playmode % 3 == 1):
        return random.randrange(1, len(ranlist)-1)
        

    if(playmode % 3 == 2):
        return listnum

def whattype(playmode):
    if(playmode % 3 == 0):
        return "ORDER"
    if(playmode % 3 == 1):
        return "RANDOM"
    if(playmode % 3 == 2):
        return "REPEAT"
    
def mediaplayer(channel, title):
    dirt = "storage/"
    if(channel == "Non Folder Music"):
        dirt = "storage"
        channel = ""

    media=instance.media_new(PATH+"storage/"+str(channel)+"/"+title)
    player.set_media(media)
    player.play()
    print(player.get_state())
def LCDsetter(changetime,Amode,Bmode,title,ik):
    if(changetime % 8 >= 7):
        lcd_string(title[ik*16:(ik+1)*16],LCD_LINE_1)
        changetime=0
        return True
    else:
        False
    if(Amode != Bmode):
        lcd_string(str(Amode),LCD_LINE_2)
        Bmode = Amode
    else:
        lcd_string(str(Bmode),LCD_LINE_2)

def timeout(sec):
    mint = sec/60
    sec = sec%60
    strmin=""
    strsec=""
    if(mint<10):
        strmin = "0"+str(mint)
    else:
        strmin = mint
    if(sec<10):
        strsec = "0"+str(sec)
    else:
        strsec = sec
    return str(strmin)+":"+str(strsec)