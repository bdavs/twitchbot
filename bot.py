#!/usr/bin/env python
import config
import utility
import socket
import time
import re
#import os, sys

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

try:
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN {}\r\n".format(config.CHAN).encode("utf-8"))
    connected = True #Socket succefully connected
except Exception as e:
    print(str(e))
    connected = False #Socket failed to connect

def bot_loop():
    while connected:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("Pong")
        else:
            username = re.search(r"\w+", response).group(0) 
            message = CHAT_MSG.sub("", response)
            #print(username + ": " + response)
            print(username + ": " + message)
            for pattern in config.SEARCH_PAT:
                if re.search(pattern, message):
                    print("matched pattern")
                    
                    #utility.chat(s,"if this prints out, I am communicating with chat properly")
                    #utility.ban(s, username)
                    #utility.test(s, username)
                    break
        time.sleep(1 / config.RATE)
if __name__ == "__main__":
    bot_loop()
