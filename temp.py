import vlc
from ftplib import FTP

ftp = FTP("192.168.0.107","root","raspberry")
ftp.cwd("/music2")
instance = vlc.Instance()

player=instance.media_player_new()

#txt STORAGE

#txt file save
 
  
media=instance.media_new("ftp://192.168.0.107/music2/a.wav")

player.set_media(media)

player.play()
