from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont

import threading
import queue
#import bot
#import readingfile as r
#import writingfile as w

import datetime

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

def bot_loop(disproot):
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
#                if username == "bdavs77":
                if re.search(pattern, message):
                    print("matched pattern")
                    widget.write(message)
                    #utility.chat(s,"if this prints out, I am communicating with chat properly")
                    #utility.ban(s, username)
                    #utility.test(s, username)
                    break
        time.sleep(1 / config.RATE)


class myThread (threading.Thread):
    def __init__(self, threadID, name, widget):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.disproot = disproot
    def run(self):
        print ("Starting " + self.name)
        if self.threadID == 1:
            print("bot loop")
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
        #set up window
        disproot.title("Events")
        disproot.attributes("-zoomed",True) #fullscreen
        #disproot.attributes("-fullscreen",True) #fullscreen
        disproot.configure(background='blue')
        #disproot.data = {}

        #setup fonts
        headerFont = tkFont.Font(root=disproot,size=20,underline=True)
        header=Label(disproot, textvariable=self.labelText, fg='white', bg='blue',font=headerFont)
        header.grid() #row=0,column=0,padx=3,pady=3)
        self.refresh()
        #self.labelText.set("TEST")
    def refresh(self):
    #refresh destroys all widgets in the current window and redraws them.

#        for w in disproot.winfo_children():
#            w.destroy()

#        self.display()
        try:
            while 1:
                line = self.queue.get_nowait()
                print("got some text: " + line)
                if line is None:
                    continue #self.delete(1.0, END)
                else:
#                    self.insert(END, str(line))
#                    self.see(END)
#                    self.update_idletasks()
                   
                    self.labelText.set(line)
        except queue.Empty:
            #print("empty")
            pass
        self.after(100, self.refresh)
    def write(self,text):
        print("In write func: " + text)
        self.queue.put(text)
        #self.labelText.set(text)
#        print("label set in write")
        #self.refresh(disproot)
if __name__ == "__main__":

    disproot = tk.Tk()
    widget = MainApplication(disproot)
    widget.display()

    # Create bot thread
    botThread = myThread(1, "Bot Thread", widget)

    # Start bot Thread
    botThread.start()

    #start tk instance from main thread
    disproot.mainloop()

    #rejoin bot thread if needed
    botThread.join()
    print ("Exiting Main Thread")
