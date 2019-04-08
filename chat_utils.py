import socket
import time

# use local loop back address by default
#CHAT_IP = '127.0.0.1'
CHAT_IP = "0.0.0.0"
CHAT_PORT = 1278
SERVER = (CHAT_IP, CHAT_PORT)

menu = "\nFollowing are the command and function you get from this community:\n\
\n++++ Choose one of the following commands\n \n\
        1). without any further state change, you can type in :\n\
        time: calendar time in the system\n \
        p _#_: to get number <#> sonnet\n \
        who: to find out who else are in this community\n \n\
        2). by using the following command, you can connect with people in this community and discuss\n\
        c _peer_: to connect to the _peer_ and chat\n \
        q: to leave the chat system\n\
         ? _term_: to search your chat logs where _term_ appears\n\n \
        3). You can also pair up and play the Game 'Conquering Finance':\n\
        g: to play the game 'Conquering Finance~~'\n\
        After entering the game state, you would be given a choice for the role 'conqueror'\n\
        who answers questions, or the role 'defendant', who chooses questions\n\
        After choosing the role, type 'next' and the system would automatically pair you up  "

        
        
        
       

S_OFFLINE   = 0
S_CONNECTED = 1
S_LOGGEDIN  = 2
S_CHATTING  = 3
S_START = 4
S_PENDING=5
S_JUDGING = 6
S_INGAME =7

SIZE_SPEC = 5

CHAT_WAIT = 0.2

def print_state(state):
    print('**** State *****::::: ')
    if state == S_OFFLINE:
        print('Offline')
    elif state == S_CONNECTED:
        print('Connected')
    elif state == S_LOGGEDIN:
        print('Logged in')
    elif state == S_CHATTING:
        print('Chatting')
    elif state == S_START:
        print("enter the game")
    elif state == S_PENDING:
        print("pending")
    elif state == S_JUDGING:
        print("judging")
    elif state == S_INGAME:
        print("in game")
    else:
        print('Error: wrong state')

def mysend(s, msg):
    #append size to message and send it
    msg = ('0' * SIZE_SPEC + str(len(msg)))[-SIZE_SPEC:] + str(msg)
    msg = msg.encode()
    total_sent = 0
    while total_sent < len(msg) :
        sent = s.send(msg[total_sent:])
        if sent==0:
            print('server disconnected')
            break
        total_sent += sent

def myrecv(s):
    #receive size first
    size = ''
    while len(size) < SIZE_SPEC:
        text = s.recv(SIZE_SPEC - len(size)).decode()
        if not text:
            print('disconnected')
            return('')
        size += text
    size = int(size)
    #now receive message
    msg = ''
    while len(msg) < size:
        text = s.recv(size-len(msg)).decode()
        if text == b'':
            print('disconnected')
            break
        msg += text
    #print ('received '+message)
    return (msg)

def text_proc(text, user):
    ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
    return('(' + ctime + ') ' + user + ' : ' + text) # message goes directly to screen

