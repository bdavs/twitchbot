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

def bot_loop(widget):
    while connected:
        response = s.recv(1024).decode("utf-8")
        log(response)
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("Pong")
        else:
            data = utility.parse_msg(response)
            if data:
                #print(str(data))
                #username = re.search(r"\w+", response).group(0)
                #message = CHAT_MSG.sub("", response)
                final_message = data['user'] + ": " + data['message']
                for pattern in config.SEARCH_PAT:
    #                if username == "bdavs77":
                    if re.search(pattern, data['message']):
    #                    print("matched pattern: " + final_message)
                        widget.write(final_message)
                        #utility.chat(s,"if this prints out, I am communicating with chat properly")
                        break
                    else:
                        print("No match: ") # + final_message)
                        #widget.write(final_message)
        time.sleep(1 / config.RATE)
def log(text):
    printstr = str(datetime.datetime.now()) + ": " + text
    print(printstr)
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
        self.labelText.set("Event")

    def display(self):
        #set up variables
        self.x=0
        self.y=0
        self.forward = 1
        self.down = 1
        headerFont = tkFont.Font(root=disproot,size=24, weight='bold', underline=False)

        #set up window
        disproot.title("Events")
        if config.RPI == 0:
            disproot.attributes("-zoomed",True)
        else:
            disproot.attributes("-fullscreen",True)
        disproot.configure(background='blue')
        self.canvas = tk.Canvas(disproot, bg="blue")
        self.canvas.pack(expand=YES, fill=BOTH)

        #set up text and canvas
        self.header=Label(self.canvas, textvariable=self.labelText, fg='white', bg='blue',font=headerFont)
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
                #print("got some text: " + line)
                if line is None:
                    continue
                else:
                    self.labelText.set(line)

        except queue.Empty:
            #print("empty")
            pass
        self.after(10, self.bounce)
        self.after(10, self.refresh)

    def write(self,text):
        #print("In write func: " + text)
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
