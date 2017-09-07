#! /usr/bin/python3

import socket
import os
import csv
import time
import smtplib
import mimetypes

#Title:Run-NetworkScout.py
#summary: this script will query the network to determine network services that are running
#Created by: Evan Costa
#Last modified: 2/8/17

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

msg = MIMEMultipart()


#------------------------Get the network information------------------------------------------------------------
ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0] #gets the IP address
maskBits = int(os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[1].split(" ")[0]) #gets the mask
#----------------------------------------------------------------------------------------------------------------

#-----------------------Setup the output file--------------------------------------------------------------------
from datetime import date
today = str(date.today())

fileName = 'NetworkStats'
fileName += today
emSubject = fileName
fileName += '.csv'

outvar = "Computer IP address,Service\n"
#touch fileName

File = open(fileName, 'w')
File.write(outvar)
#----------------------------------------------------------------------------------------------------------------
#-----------------------Detect if network is class C-------------------------------------------------------------
numAddresses = 0
if maskBits == 24: #limit to a class c address
    numAddresses = 255
    netWork = ipv4.split(".")[0]
    netWork += '.'
    netWork += ipv4.split(".")[1]
    netWork += '.'
    netWork += ipv4.split(".")[2]
else:
    print('network not supported by this script! exiting....')
    exit()
#---------------------------------------------------------------------------------------------------------------

#--------------for each number less than 255, attempt to conenct using sockets----------------------------------
count = 1
while (count < numAddresses):
    
    IPAddress = netWork
    IPAddress += '.'
    IPAddress += str(count)
    
    print("checking {}".format(IPAddress))
    
    #check for FTP service-------------------------------------------------------------------------------------  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(.01)
    result = s.connect_ex((IPAddress, 21))
    if result == 0:
        IPAddressN ='	Found FTP'
        IPAddressO = IPAddress
        IPAddressO += ",FTP\n" 
        File.write(IPAddressO)
        print(IPAddressN)
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(.01)

    #check for smtp service------------------------------------------------------------------------------------
    result = s.connect_ex((IPAddress, 25))
    if result == 0:
        IPAdressN  ='	Found email'
        IPAddressO = IPAddress
        IPAddressO += ",email\n"
        File.write(IPAddressO)
        print(IPAddressN)
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #check for DHCP service-------------------------------------------------------------------------------------
    result = s.connect_ex((IPAddress, 68)
    if result == 0:
        IPAddressN  ='	Found DHCP'
        IPAddressO = IPAddress
        IPAddressO += ",DHCP\n"
        File.write(IPAddressO)
        print(IPAddressN)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(.01)
   
    #check for DNS service---------------------------------------------------------------------------------------
    result = s.connect_ex((IPAddress, 53))
    if result == 0:
        IPAddressN ='	Found DNS'
        IPAddressO = IPAddress
        IPAddressO += ",DNS\n"
        File.write(IPAddressO)
        print(IPAddressN)
    s.close()
    count +=1
File.close()
#-----------------------------------------------------------------------------------------------------------------
#Send Email section
#Attach CSV as an attachment
#specify account details, message, and addresses
#Send Email using GMAIL's smtp server

fromAddress = "evan.c.costa@gmail.com"
toAddress   = "ecc1655@g.rit.edu"

msg['Subject'] = emSubject
msg['From'] = fromAddress
msg['To'] = toAddress

body = "Run-NetworkScout.py has completed. Please see attached file"

msg.attach(MIMEText(body, 'plain'))

attachment = open(fileName, "rb")
 
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; fileName= %s" % fileName)
 
msg.attach(part)
 
server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login(fromAddress,"drjesaygbmzwzilo")
server.sendmail(fromAddress,toAddress, msg.as_string())
server.quit()
print('Task Complete. Please check email for file'
#-------------------------------------------------------------------------------------
