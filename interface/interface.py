from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont

import readingfile as r
import writingfile as w
import adminInterface as adminInterface
import calendarApp as cal

import datetime

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    def display(self):
#        disproot = Tk()
        disproot.configure(background='blue')
        disproot.data = {}
        offset = 1

        #setup fonts
        headerFont = tkFont.Font(root=disproot,size=20,underline=True)
        currentEventFont = tkFont.Font(root=disproot,size=20,weight='bold')
        eventFont = tkFont.Font(root=disproot,size=10)

        d = r.fileToDict() #import data from file

        #error checking
        #may require own function
        if d is -1:
            error=Label(disproot, text="No entries in table")
            error.grid(row=0,column=0)
            mainloop()

        currentEvent = True


#        temp = datetime.datetime.now().strftime("%A, %-d %B %Y %-I:%M%p")

        #Sort the list
        newD = {'name':[], 'date':[], 'speaker':[] }
        while(len(d['name']) > 0):
            minIndex, minValue = min(enumerate(d['date']), key=lambda v: v[1])
            tempName = d['name'].pop(minIndex)
            tempDate = d['date'].pop(minIndex)
            tempDatePrime = datetime.datetime.strptime(tempDate,"%Y-%m-%d %H:%M:%S")
            tempSpeaker = d['speaker'].pop(minIndex)
            if tempDate > str(datetime.datetime.now()):
                newD['name'].append(tempName)
                newD['date'].append(tempDate)
                newD['speaker'].append(tempSpeaker)
        d=newD


        for i in range(len(d['name'])): #Rows
            #current events in bold
            if currentEvent is True:
                l1=Label(disproot, text=d['name'][i], fg='white', bg='blue', font=currentEventFont)
                l2=Label(disproot, text=d['date'][i],fg='white', bg='blue',font=currentEventFont)
                l3=Label(disproot, text=d['speaker'][i],fg='white', bg='blue',font=currentEventFont)
                currentEvent = False
            #other events smaller
            else:
                l1=Label(disproot, text=d['name'][i],fg='white', bg='blue',font=eventFont)
                l2=Label(disproot, text=d['date'][i],fg='white', bg='blue',font=eventFont)
                l3=Label(disproot, text=d['speaker'][i],fg='white', bg='blue',font=eventFont)
            l1.grid(row=i+1, column=0)
            l2.grid(row=i+1, column=1)
            l3.grid(row=i+1, column=2)

        #set up headers in larger font
        header=Label(disproot, text="Event Name",fg='white', bg='blue',font=headerFont)
        header.grid(row=0,column=0,padx=3,pady=3)
        header=Label(disproot, text="Date and Time",fg='white', bg='blue',font=headerFont)
        header.grid(row=0,column=1,padx=3,pady=3)
        header=Label(disproot, text="Speaker",fg='white', bg='blue',font=headerFont)
        header.grid(row=0,column=2,padx=3,pady=3)

        #add refresh button
#        Button(disproot,text="Refresh",width=7,command=lambda:self.refresh(disproot)).grid(row=0,column=3)

#        temp = datetime.datetime.now().strftime("%A, %-d %B %Y %-I:%M%p")
#        Label(disproot,text=temp).grid(row=2,column=3)

        #set up window
        disproot.title("Events")
#        disproot.attributes("-zoomed",True) #fullscreen
        disproot.attributes("-fullscreen",True) #fullscreen
        disproot.grid_columnconfigure([0,1,2,3],weight=1)

    def refresh(self,disproot):
    #refresh destroys all widgets in the current window and redraws them.

        for w in disproot.winfo_children():
            w.destroy()

        self.display()

if __name__ == "__main__":

    disproot = tk.Tk()

    MainApplication(disproot).display()
#    adminInterface.MainApplication.adminScreen(self) #starts admin screen (maybe)
    disproot.mainloop()

