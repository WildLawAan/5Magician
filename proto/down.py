import os
from ftplib import FTP
inner=0

incomlist=[]

inconlist=os.listdir("/home/pi/Music/")
 
ftp = FTP("192.168.0.42","root","raspberry")
#ftp.retrlines("LIST")
 
ftp.cwd("/storage")
 
listing=[]
 
ftp.retrlines("LIST",listing.append)
print(listing)

while inner<len(listing):
    word = listing[inner].split(None,8)
    print(word)
    filename=word[-1].lstrip()
    print(filename)
    if filename in incomlist:
        incomlist.remove(filename)
inner=0
print(incomlist)
while inner<len(listing):
    local_filename = os.path.join("/home/pi/Music/"+incomlist[inner])
    print(local_filename)
    If=open(local_filename,"wb")
    ftp.retrbinary("RETR "+filename, If.write, 1024)
    If.close()
    inner+=1
