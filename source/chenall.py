from ftplib import FTP
 
allmusic = []
junklist = []
musiclist = []
channellist = []
musicfolderlist=[]
channel = []
ftp = FTP("192.168.0.107","root","raspberry")
ftp.cwd("/music2")
ftp.retrlines("LIST", junklist.append)
print(junklist)
i=0
 
while i<len(junklist):
    word = junklist[i].split(None,8)
    filename=word[-1].lstrip()
    musiclist.append(filename)
    i+=1
print(musiclist)
i=0
junklist = []
junklist.append("Non")
 
while i<len(musiclist):
    name = musiclist[i]
    print(name)
    if(len(name)>4):
        if(name[-4]!="." and name[-5]!="."):
            channellist.append(name)
        else:
            junklist.append(name)
    else:
        channellist.append(name)
    i+=1
channellist.append(junklist)
#channellist(앞부분: 채 널종 류/ 뒷부분: 잉여곡 명)
print (channellist)
junklist=[]
i=0
j=0
while i<(len(channellist)-1):
    channelname = channellist[i]
    ftp.cwd("/music2/"+channelname)
    ftp.retrlines("LIST", junklist.append)
    musiclist=[]
    musiclist.append(channelname)
    channel.append(channelname)
    #musiclist[0]에 채널이름 넣기
    while j<len(junklist):
        word = junklist[j].split(None,8)
        filename = word[-1].lstrip()
        musiclist.append(filename)
        allmusic.append(filename)
        j+=1
        #musiclist[1:]해당채널의 음악
    print(musiclist)
    i+=1
 
    musicfolderlist.append(musiclist)
    #채널 별 정리
musicfolderlist.append(channellist[-1])
#channellist[-1]:정 리안 된잉여곡 들
#musicfolderlist[-1]:정리안된 곡들
#musicfolderlist[n][0]:채널이름들
 
print(musicfolderlist)
