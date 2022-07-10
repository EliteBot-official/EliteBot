#!/usr/bin/python3
 
# Bot Settings
BNICK   = 'EliteBot'
BIDENT  = 'EliteBot'
BNAME   = 'EliteBot'
BALT    = 'EliteBot-'
BHOME   = '#EliteBot'

# Connection Settings
BPORT   =  '+6697'
BSERVER = 'irc.technet.chat'
 
# SASL Configuration.
UseSASL = False
SANICK  = 'EliteBot'
SAPASS  = 'password'
 
import ssl
import socket
import base64
import random
 
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

def decode(bytes):
    try: text = bytes.decode('utf-8')
    except UnicodeDecodeError:
        try: text = bytes.decode('latin1')
        except UnicodeDecodeError:
            try: text = bytes.decode('iso-8859-1')
            except UnicodeDecodeError:
                text = bytes.decode('cp1252')			
    return text
    
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
    
print(f'Connecting to {BSERVER} :{BPORT}')
ircsock.connect_ex((BSERVER, BPORT))
   
SendIRC(f'NICK {BNICK}')
SendIRC(f'USER {BIDENT} * * :{BNAME}')

if UseSASL:
   SendIRC('CAP REQ :sasl')

   
while True:
    recvText = ircsock.recv(2048)
    ircmsg = decode(recvText)
    line = ircmsg.strip('\n\r')
    word = line.split(" ")
    print(ircmsg)
 
    if word[0] == "PING":
         pongis = ircmsg.split(' ', 1)[1]
         SendIRC(f'PONG {pongis}')
            
    if line.find('ACK :sasl') != -1 or ircmsg.find('ACK :sasl') != -1:
       SendIRC('AUTHENTICATE PLAIN')
 
    if ircmsg.find('AUTHENTICATE +') != -1:
          authpass = SANICK + '\x00' + SANICK + '\x00' + SAPASS
          ap_encoded = str(base64.b64encode(authpass.encode('UTF-8')), 'UTF-8')
          SendIRC('AUTHENTICATE ' + ap_encoded)
 
    elif ircmsg.find(f' 903 {BNICK} :') != -1:
       SendIRC('CAP END')
    
    if line.find(f' 001 {BNICK} :') != -1:
        SendIRC(f'JOIN {BHOME}')
