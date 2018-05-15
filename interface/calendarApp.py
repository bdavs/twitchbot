import calendar
import datetime
import sys
if sys.version[0] == '2':
    import Tkinter as tk
else:
    import tkinter as tk
from tkinter import *
class Calendar:
    def __init__(self, parent, values):
        self.values = values
#        values(self.values)
        self.parent = parent
        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        self.wid = []
        self.day_selected = 1
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = ''
        self.hour=0
        self.minute=0

        self.setup(self.year, self.month, self.hour, self.minute)

    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            #w.destroy()
            self.wid.remove(w)

    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1
        #self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month, self.hour, self.minute)

    def go_next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1

        #self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month, self.hour, self.minute)

    def selection(self, day, name, hour, minute):
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        self.hour=hour
        self.minute=minute
        self.day_name = name

        #data

#        self.values['day_selected'] = day
#        self.values['month_selected'] = self.month
#        self.values['year_selected'] = self.year
#        self.values['day_name'] = name
#        self.values['month_name'] = calendar.month_name[self.month_selected]

        self.values[0] = str(datetime.datetime(self.year, self.month, day, int(self.hour),int(self.minute)))

#        s = tempval
#        print(str(tempval) + "    " + str(self.values))
#        values = self.values
        self.clear()
        self.setup(self.year, self.month, self.hour, self.minute)

    def setup(self, y, m, h, minu):
        left = tk.Button(self.parent, text='<', command=self.go_prev)
        self.wid.append(left)
        left.grid(row=1, column=1)

        header = tk.Label(self.parent, height=2, text='{}   {}'.format(calendar.month_abbr[m], str(y)))
        self.wid.append(header)
        header.grid(row=1, column=2, columnspan=3)

        right = tk.Button(self.parent, text='>', command=self.go_next)
        self.wid.append(right)
        right.grid(row=1, column=5)

        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for num, name in enumerate(days):
            t = tk.Label(self.parent, text=name[:3])
            self.wid.append(t)
            t.grid(row=2, column=num)

        for w, week in enumerate(self.cal.monthdayscalendar(y, m), 2):
            for d, day in enumerate(week):
                if day:
                    #print(calendar.day_name[day])
                    b = tk.Button(self.parent, width=1, text=day, command=lambda day=day:self.selection(day, calendar.day_name[(day-1) % 7], self.hour, self.minute))
                    self.wid.append(b)
                    b.grid(row=w, column=d)

        sel = tk.Label(self.parent, height=2, text='{}:{} {} {} {} {}'.format(
            self.hour, self.minute, self.day_name, calendar.month_name[self.month_selected], self.day_selected, self.year_selected))
        self.wid.append(sel)
        sel.grid(row=9, column=0, columnspan=7)

        hour = tk.Spinbox(self.parent, width =2,from_=0, to=23, format="%02.0f", command=lambda:self.updatehour(hour))
        hour.delete(0,"end")
        hour.insert(0,h)
        self.wid.append(hour)
        hour.grid(row=0, column=4)
       # self.hour=hour_data

        minutes = tk.Spinbox(self.parent, width = 2, from_=00, to=55, increment=5, format="%02.0f",command=lambda:self.updateminute(minutes))
        minutes.delete(0,"end")
        minutes.insert(0,minu)
        self.wid.append(minutes)
        minutes.grid(row=0, column=5)
       # self.minute=minute_data

        timeLabel = tk.Label(self.parent, text="Enter Time:")
        self.wid.append(timeLabel)
        timeLabel.grid(row=0, column=1,columnspan=2,pady=10)

        ok = tk.Button(self.parent, width=5, text='OK', command=self.kill_and_save)
        self.wid.append(ok)
        ok.grid(row=10, column=2, columnspan=3, pady=10)

    def updatehour(self,hour):
       hour_data=hour.get()
       self.hour=hour_data
       #print(hour_data)
       #print(self.hour)

    def updateminute(self,minutes):
       minute_data=minutes.get()
       self.minute=minute_data

    def kill_and_save(self):
        self.parent.destroy()


if __name__ == '__main__':

    class Control:
        def __init__(self, parent):
            self.parent = parent
            self.choose_btn =  tk.Button(self.parent, text='Choose',command=self.popup)
            self.show_btn = tk.Button(self.parent, text='Show Selected',command=self.print_selected_date)
            self.choose_btn.grid()
            self.show_btn.grid()
            self.data = [''] #[StringVar(datetime.date.today())]

        def popup(self):
            child = tk.Toplevel()
            cal = Calendar(child, self.data)

        def print_selected_date(self):
            print(self.data)


    root = tk.Tk()
    app = Control(root)
    root.mainloop()
