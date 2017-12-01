from ftplib
import FTP_TLS
print("a")

ftp = FTP_TLS()
print("a")
ftp.connect('192.168.0.107', 21)
print("a")
ftp.login('root','raspberry')
print("a")
ftp.prot_p()
print("a")
ftp.nlst()
raspberry
