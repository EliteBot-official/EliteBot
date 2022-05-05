#!/usr/bin/python3

import ssl
import socket
import base64
import random
import src.*
from EliteBotConfig import *

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

if str(BPORT)[:1] == '+':
    print('Use SSL')
    ircsock = ssl.wrap_socket(ircsock)
    BPORT = int(BPORT[1:])
else:
    BPORT = int(BPORT)

ircsock.settimeout(240)

def SendIRC(msg):
    if msg != '': ircsock.send(bytes(f'{msg}\r\n','utf-8'))

def SendMsg(msg, target=BHOME):
    SendIRC("PRIVMSG "+ target +" :"+ msg)
    
def connect(): 
   print(f'Connecting to {BSERVER} :{BPORT}')
   ircsock.connect_ex((BSERVER, BPORT))
   if UseSASL:
      SendIRC('CAP REQ :sasl')
   if USPASS:
      SendIRC(f'PASS {SPASS}')
   SendIRC(f'NICK {BNICK}')
   SendIRC(f'USER {BIDENT} * * :{BNAME}')
   
def decode(bytes):
    try: text = bytes.decode('utf-8')
    except UnicodeDecodeError:
        try: text = bytes.decode('latin1')
        except UnicodeDecodeError:
            try: text = bytes.decode('iso-8859-1')
            except UnicodeDecodeError:
                text = bytes.decode('cp1252')			
    return text

while True:
    recvText = ircsock.recv(2048)
    ircmsg = decode(recvText)
    line = ircmsg.strip('\n\r')
    linx = line.replace(':','')
    print(linx)

    if ircmsg.find(f' 001 {BNICK} :') != -1:
       SendIRC(f'JOIN {BHOME}')

    elif ircmsg.find('PING') != -1:
        pongis = ircmsg.split(' ', 1)[1] 
        SendIRC(f'PONG {pongis}')
        
    elif ircmsg.find(f' 433 * {BNICK} :') != -1:
        BNICK = f'{BNICK}{str(random.randint(10000,99999))}'
        SendIRC(f'NICK {BNICK}')
        
    elif ircmsg.find('say hi to') != -1:
        Nick2TellFkOff = ircmsg.split('say hi to ')[1]
        SendMsg(f'No! Fuck {Nick2TellFkOff}.')
        
    elif ircmsg.find('ACK :sasl') != -1:
       print('Authenticating with SASL PLAIN.')
       SendIRC('AUTHENTICATE PLAIN')

    elif ircmsg.find('AUTHENTICATE +') != -1:
          authpass = SANICK + '\x00' + SANICK + '\x00' + SAPASS
          ap_encoded = str(base64.b64encode(authpass.encode('UTF-8')), 'UTF-8')
          SendIRC('AUTHENTICATE ' + ap_encoded)

    elif ircmsg.find(f' 903 {BNICK} :') != -1:
       print('Sending CAP END command.')
       SendIRC('CAP END')
