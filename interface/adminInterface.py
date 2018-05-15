from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import readingfile as r
import writingfile as w
import time
import datetime
import sys
import calendarApp as cal



content = [] #StringVar()
e2 = [] #entry
choose_btn = [] #button

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    def add_field(self,root,dic,saveButton, addRow):
        i=len(content)
        e1=Entry(root, text='')
        content.append(StringVar())
        e2.append(Entry(root, textvariable=content[i]))
        choose_btn.append(Button(root, text='Choose',command=lambda q=i:self.popup(root,content[q])))
        e3=Entry(root, text='')
        e1.grid(row=i+1, column=0)
        e2[i].grid(row=i+1, column=1)
        choose_btn[i].grid(row=i+1, column=2)
        e3.grid(row=i+1, column=3)
        dic['name'].append(e1)
        dic['date'].append(e2[i])
        dic['speaker'].append(e3)
        root.heightvar+=1
        saveButton.grid(row=root.heightvar+1, column=2)
        addRow.grid(row=root.heightvar+1, column=0)

    def save_entries(self,dic,saveButton,root):
        valueDict = {}
#        print(root.data)
        valueDict['name'] = []
        valueDict['date'] = []
        valueDict['speaker'] = []
        tempvar = ''
        for key,value in dic.items():
            for v in value:
                tempvar = v.get()
                valueDict[key].append(tempvar)

        for i in reversed(range(len(valueDict['name']))):
            if valueDict['name'][i] is '' and valueDict['date'][i] is '' and valueDict['speaker'][i] is '' :
                del valueDict['name'][i]
                del valueDict['date'][i]
                del valueDict['speaker'][i]
        w.writeToFile(valueDict)
        saveButton.config(text="SAVED!")


    def adminScreen(self):

        root.data = {} #is this still used
        root.heightvar = 3 #default number of new entries
        dic = {}
        dic['name'] = []
        dic['date'] = []
        dic['speaker'] = []


        for i in range(root.heightvar): #Rows
            e1=Entry(root, text='')
            content.append(StringVar())
            e2.append(Entry(root, textvariable=content[i]))
            choose_btn.append(Button(root, text='Choose',command=lambda q=i:self.popup(root,content[q])))
            e3=Entry(root, text='')
            e1.grid(row=i+1, column=0)
            e2[i].grid(row=i+1, column=1)
            choose_btn[i].grid(row=i+1, column=2)
            e3.grid(row=i+1, column=3)
            dic['name'].append(e1)
            dic['date'].append(e2[i])
            dic['speaker'].append(e3)

        header=Label(root, text="Event Name")
        header.grid(row=0,column=0)
        header=Label(root, text="Date and Time")
        header.grid(row=0,column=1)
        header=Label(root, text="Speaker")
        header.grid(row=0,column=3)

        saveButton = Button(root, text='SAVE', command=lambda: self.save_entries(dic,saveButton,root))
        saveButton.grid(row=root.heightvar+1, column=2)
        addRow = Button(root, text='+', command=lambda: self.add_field(root,dic,saveButton,addRow))
        addRow.grid(row=root.heightvar+1, column=0)
        root.title("Admin Screen")

    def popup(self,root,content):
        a = ['']
        new = tk.Toplevel(self)             #make new subwindow
        calendar1 = cal.Calendar(new, a)    #make calendar window
#        root.withdraw()
        new.grab_set()
        root.wait_window(new)               #wait until window closes
        new.grab_release()
#        root.deiconify()
        content.set(a[0])                   #set entry as selected datetime

if __name__ == '__main__':

    root = tk.Tk()
    MainApplication(root).adminScreen()
#    display()
    root.mainloop()

