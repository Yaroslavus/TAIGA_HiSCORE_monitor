#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 05:59:17 2021

@author: yaroslav
"""
import datetime
import tkinter as tk
import threading
from time import sleep
import sys
import re
import pytz
import random

timezone_irkutsk = pytz.timezone('Asia/Irkutsk')
timezone_utc = pytz.timezone('UTC')
# =============================================================================
#
# =============================================================================

class station:
    
    list_of_station = []
    
    def __init__ (self, number=0, count_rate=0, time = 0, threshold=0):
        self.number = number
        self.count_rate = count_rate
        self.time = time
        self.threshold = threshold

def today_timemarks():
    
    utc_datetime_now = datetime.datetime.now(timezone_utc) 
    tunka_datetime_now = datetime.datetime.now(timezone_irkutsk)
    
    return utc_datetime_now, tunka_datetime_now
                  
def time_update():
    
    while True:
        
        tunka_datetime_now = datetime.datetime.now(timezone_irkutsk)
        tunka_time_now = tunka_datetime_now.strftime("%H:%M:%S")
        tunka_date_now = tunka_datetime_now.strftime("%d:%m:%Y")

        utc_datetime_now = datetime.datetime.now(timezone_utc)
        utc_time_now = utc_datetime_now.strftime("%H:%M:%S")
        utc_date_now = utc_datetime_now.strftime("%d:%m:%Y")   

        main_form.time_frame.tunka_time_now_label['text'] = tunka_time_now
        main_form.time_frame.utc_time_now_label['text'] = utc_time_now
        main_form.time_frame.tunka_date_now_label['text'] = tunka_date_now
        main_form.time_frame.utc_date_now_label['text'] = utc_date_now

        sleep(1)
        
        
class Time_Window(tk.Frame):
    
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.init_ui()
#        self.root.mainloop()
        
    def init_ui(self):
        
        self.root['padx'] = 5
        self.root['pady'] = 5
        
        utc_datetime_now, tunka_datetime_now = today_timemarks()
                    
        time_frame = tk.Frame(self.root, relief=tk.GROOVE, borderwidth=1)
        time_frame.pack(fill=tk.X)
            
        self.utc_date_title_label = tk.Label(time_frame, text="UTC Date:")
        self.utc_time_title_label = tk.Label(time_frame, text="UTC Time:")
        self.tunka_date_title_label = tk.Label(time_frame, text="Tunka Date:")
        self.tunka_time_title_label = tk.Label(time_frame, text="Tunka Time:")
            
        self.utc_date_title_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
        self.utc_time_title_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
        self.tunka_date_title_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
        self.tunka_time_title_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
        
        self.tunka_time_now_label = tk.Label(time_frame, text=tunka_datetime_now.strftime("%H:%M:%S"))
        self.utc_date_now_label = tk.Label(time_frame, text=utc_datetime_now.strftime("%d:%m:%Y") )
        self.utc_time_now_label = tk.Label(time_frame, text=utc_datetime_now.strftime("%H:%M:%S"))
        self.tunka_date_now_label = tk.Label(time_frame, text=tunka_datetime_now.strftime("%d:%m:%Y"))
    
    #        self.utc_date_title_label.grid(row=0, column=0, ipadx=4, padx=4)
    #        self.utc_date_now_label.grid(row=0, column=1, ipadx=4, padx=4)
    #        self.utc_time_title_label.grid(row=0, column=2, ipadx=4, padx=4)
    #        self.utc_time_now_label.grid(row=0, column=3, ipadx=4, padx=4)
    #        self.tunka_date_title_label.grid(row=0, column=4, ipadx=4, padx=4)
    #        self.tunka_date_now_label.grid(row=0, column=5, ipadx=4, padx=4)
    #        self.tunka_time_title_label.grid(row=0, column=6, ipadx=4, padx=4)
    #        self.tunka_time_now_label.grid(row=0, column=7, ipadx=4, padx=4)
                
        self.utc_date_now_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
        self.utc_time_now_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
        self.tunka_date_now_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
        self.tunka_time_now_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
        
        
#        while True:
#            
#            utc_datetime_now, tunka_datetime_now = today_timemarks()
#            self.tunka_time_now_label['text'] = tunka_datetime_now.strftime("%H:%M:%S")
#            self.utc_date_now_label['text'] = utc_datetime_now.strftime("%d:%m:%Y")
#            self.utc_time_now_label['text'] = utc_datetime_now.strftime("%H:%M:%S")
#            self.tunka_date_now_label['text'] = tunka_datetime_now.strftime("%d:%m:%Y")
#    
#            time_frame.update()
#            sleep(1)
        
#        self.pack(side=tk.LEFT, fill=tk.X)
        
class Info_Window(tk.Frame):
    
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.init_ui()
#        self.root.mainloop()
        
    def init_ui(self):
        
        info_frame = tk.Frame(self.root, relief=tk.GROOVE)
        info_frame.pack(fill=tk.X)
        cluster_frame_list = []
        for i in range (4):
            
            cluster_number_label = tk.Label(info_frame, text="Cluster # " + str(i+1))
            cluster_number_label.grid(row=2*i, column=0)
            cluster_frame = tk.Frame(info_frame, relief=tk.GROOVE, borderwidth=1)
            cluster_frame_list.append(cluster_frame)
            cluster_frame.grid(row=2*i+1, column=0)
            
            
        
        for n in range(len(cluster_frame_list)):
            for i in range(12):
                for j in range(2):
                    station_frame = tk.Frame(cluster_frame_list[n], width=157, height=100, relief=tk.GROOVE, borderwidth=1)
                    station_frame.grid(row=2*n+j, column=i)
                    station_frame.grid_propagate(0)
                    canvas = tk.Canvas(station_frame, width=60, height=95)
                    canvas.create_oval(10, 10, 50, 50, fill="red")
                    canvas.create_rectangle(10, 60, 50, 70, fill='lightblue')
                    canvas.create_oval(10, 80, 20, 90, fill='lightgreen')
                    canvas.grid(row=0, column=0)
                    data_label=tk.Label(station_frame, text = "#: {}\nCR: {}\nTH: {}\nT: {}\nFr: {}".format(0,0,0,0,0))
                    data_label.grid(row=0, column=1, sticky='nw')

#        while True:
#            for n in range(len(cluster_frame_list)):
#                for i in range(12):
#                    for j in range(2):
#                        station_frame = tk.Frame(cluster_frame_list[n], width=157, height=100, relief=tk.GROOVE, borderwidth=1)
#                        station_frame.grid(row=2*n+j, column=i)
#                        station_frame.grid_propagate(0)
#                        canvas = tk.Canvas(station_frame, width=60, height=95)
#                        canvas.create_oval(10, 10, 50, 50, fill="red")
#                        canvas.create_rectangle(10, 60, 50, 70, fill='lightblue')
#                        canvas.create_oval(10, 80, 20, 90, fill='lightgreen')
#                        canvas.grid(row=0, column=0)
#                        data_label=tk.Label(station_frame, text = "#: {}\nCR: {}\nTH: {}\nT: {}\nFr: {}".format(0,0,0,0,0))
#                        data_label.grid(row=0, column=1, sticky='nw')
#            
##            sleep(1)
##            info_frame.update()
    


                 
if __name__ == '__main__':
    
    main_form = tk.Tk()
    main_form.title("HiScore shift monitor for {}".format(today_timemarks()[1].strftime("%d:%m:%Y")))
    time_window = Time_Window(main_form)
    info_window = Info_Window(main_form)
    main_form.geometry("{}x{}".format(1897,930))
    process = threading.Thread(target=time_update)
    process.start()
    main_form.mainloop()
    
    