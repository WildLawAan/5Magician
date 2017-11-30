import os
from ftplib import FTP

def(serfile, locallist):
    for serfile in locallist:
        locallist.remove(serfile)
    

inner=0

incomlist=os.listdir("/home/pi/Music")

 
ftp = FTP("192.168.0.42","root","raspberry")
#ftp.retrlines("LIST")
 
ftp.cwd("/storage")
 
listing=[]
 
ftp.retrlines("LIST",listing.append)
print(listing)
 
while inner<len(listing):
    word = listing[inner].split(None,8)
    filename=word[-1].lstrip()
    
    local_filename = os.path.join("/home/pi/Music/"+filename)
    print(local_filename)
    If=open(local_filename,"wb")
    ftp.retrbinary("RETR "+filename, If.write, 1024)
    If.close()
    inner+=1
