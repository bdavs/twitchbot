from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont

import threading
import queue
#import bot
import datetime

import config
import utility
import socket
import time
import re

#response =  {'meta':meta, 'user':user, 'msgtype':msgtype, 'channel':channel, 'message':message}
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
w = open('logfile.txt', 'w+')
try:
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN {}\r\n".format(config.CHAN).encode("utf-8"))
    s.send("CAP REQ :twitch.tv/membership\r\n".encode("utf-8"))
    s.send("CAP REQ :twitch.tv/tags\r\n".encode("utf-8"))
    s.send("CAP REQ :twitch.tv/commands\r\n".encode("utf-8"))
    connected = True #Socket succefully connected
    print("Connected to twitch irc")
except Exception as e:
    print(str(e))
    connected = False #Socket failed to connect
    print("Failed to connected to twitch irc")
def bot_loop(widget):
    while connected:
        response = s.recv(1024).decode("utf-8")
        #log everything currently
        log(response)
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("Pong")
        else:
            #actually parse the data
            data = utility.parse_msg(response)
            if data:
                #print(str(data))
                #username = re.search(r"\w+", response).group(0)
                #message = CHAT_MSG.sub("", response)
                #final_message = data['user'] + ": " + data['message']

                #check if someone sent bits or subbed
                if 'bits' in data['meta']:
                    somebits = int(data['meta']['bits']) - 7
                    if somebits > 0:
                        addon = "\nThat's like " + str(somebits) + " more than 7!"
                    else:
                        addon = ""
                    final_message = data['user'] + " just sent " + data['meta']['bits'] + " bits!" + addon + "/n" + data['message']
                    print(final_message)
                    widget.write(final_message)
                if 'msg-id' in data['meta']:
                    if data['meta']['msg-id'] == "sub":
                        final_message = data['user'] + " just subscribed!\nSay what?!?!"
                        print(final_message)
                        widget.write(final_message)
                    elif data['meta']['msg-id'] == "resub":
                        final_message = data['user'] + " just resubscribed for their "+ data['meta']['msg-param-months'] + " month!\nThat's commitment!"
                        print(final_message)
                        widget.write(final_message)
                    elif data['meta']['msg-id'] == "subgift":
                        final_message = data['user'] + " just gifted a subscription to " + data['meta']['msg-param-recipient-user-name'] + "!\nThank you!"
                        print(final_message)
                        widget.write(final_message)
                    else:
                        print("error: different msg-id: " + data['meta']['msg-id'])

#                if data['user'] == "bdavs77" and data['msgtype'] == "PRIVMSG":
                if (data['meta']['mod'] == 1 or data['user'] == data['channel'][1:]) and data['msgtype'] == "PRIVMSG":
                    if re.search(config.MOD_COMMAND, data['message']):
                        message = re.sub(config.MOD_COMMAND,"", data['message'])
                        final_message = data['user'] + ": " + message #data['message']
                        print(final_message)
                        widget.write(final_message)
                #for pattern in config.SEARCH_PAT:
    #                if username == "bdavs77":
                 #   if re.search(pattern, data['message']):
    #                    print("matched pattern: " + final_message)
                        #widget.write(final_message)
                        #utility.chat(s,"if this prints out, I am communicating with chat properly")
                  #      break
                   # else:
                    #    print("No match: ") # + final_message)
                        #widget.write(final_message)

        time.sleep(1 / config.RATE)

def log(text):
    printstr = str(datetime.datetime.now()) + ": " + text
#    print(printstr)
    w.write(printstr)
    w.flush()
class myThread (threading.Thread):
    def __init__(self, threadID, name, widget):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("Starting " + self.name)
        if self.threadID == 1:
#            print("bot loop")
            bot_loop(widget)
        else:
            print("Threading error")
            exit(1)
        print ("Exiting " + self.name)

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.queue = queue.Queue()
        self.labelText=StringVar()
#        self.labelText.set("Welcome to the bdavs stream!")
        self.labelText.set("Testing!")
        self.timeout = 0
    def display(self):
        #set up variables
        self.x=0
        self.y=0
        self.forward = 1
        self.down = 1
        headerFont = tkFont.Font(root=disproot,size=config.FONT_SIZE, 
weight='bold', underline=False)

        #set up window
        disproot.title("Events")
        if config.RPI == 0:
            disproot.attributes("-zoomed",True)
        else:
            disproot.attributes("-fullscreen",True)
        disproot.configure(background=config.BG)
        self.canvas = tk.Canvas(disproot, bg=config.BG)
        self.canvas.pack(expand=YES, fill=BOTH)

        #set up text and canvas
        self.header=Label(self.canvas, textvariable=self.labelText,
        fg=config.FG, bg=config.BG,font=headerFont)
        self.header.pack()
        self.hwindow = self.canvas.create_window(self.x,self.y, anchor='nw', window=self.header)
        self.canvas.update()
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()

        #enter main loop
        self.refresh()

    def bounce(self):
        #bbox for bounds
        bbox = self.canvas.bbox(self.hwindow)

        #horizontal movement
        self.x = config.SPEEDX if self.forward == 1 else -config.SPEEDX
        if bbox[2] + self.x >= self.width:
            self.forward = 0
        elif bbox[0] + self.x <= 0:
            self.forward = 1

        #vertical movement
        self.y = config.SPEEDY if self.down == 1 else -config.SPEEDY
        if bbox[3] + self.y >= self.height:
            self.down = 0
        elif bbox[1] + self.y <= 0:
            self.down = 1

        #actually move
        self.canvas.move(self.hwindow, self.x, self.y)

    def refresh(self):
        try:
            while 1:
                line = self.queue.get_nowait()
                if line is None:
                    continue
                else:
                    self.labelText.set(line)
                    self.timeout = 0
        except queue.Empty:
            pass

        self.after(config.REFRESH, self.bounce)

        #only leave message up for certain time
        if self.timeout > config.TIMEOUT:
            self.labelText.set("")
            self.timeout = 0
        else:
            self.timeout += 1

        self.after(config.REFRESH, self.refresh)

    def write(self,text):
        self.queue.put(text)

    def shift(self, text):
        text = text[1:] + text[0]
        return(text)

if __name__ == "__main__":

    #set up app
    disproot = tk.Tk()
    widget = MainApplication(disproot)
    widget.display()

    #Create and start bot thread
    botThread = myThread(1, "Bot Thread", widget)
    botThread.start()

    #start tk instance from main thread
    disproot.mainloop()

    #rejoin bot thread if needed
    botThread.join()
    print ("Exiting Main Thread")
