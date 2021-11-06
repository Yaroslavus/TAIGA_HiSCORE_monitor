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
import pytz
import random
from colour import Color
import os
import re

timezone_irkutsk = pytz.timezone('Asia/Irkutsk')
timezone_utc = pytz.timezone('UTC')

SCRIPT_DIR = os.getcwd()
# =============================================================================
#
# =============================================================================

class Station:
    
    list_of_station = []
    list_of_count_rates = []
    list_of_times = []
    
    def __init__ (self, cluster_number=0, station_number=0, count_rate=0, time=0, threshold=0, frequency=0):
        self.cluster_number = cluster_number
        self.station_number = station_number
        self.count_rate = count_rate
        self.time = time
        self.threshold = threshold
        self.frequency = frequency
        self.list_of_station.append(self)
        self.list_of_count_rates.append(self.count_rate)
        self.list_of_times.append(self.time)

def today_timemarks():
    
    return datetime.datetime.now(timezone_utc), datetime.datetime.now(timezone_irkutsk)

                  
def time_update():
    
    while True:
        
        tunka_time_now_label['text'] = datetime.datetime.now(timezone_irkutsk).strftime("%H:%M:%S")
        utc_time_now_label['text'] = datetime.datetime.now(timezone_utc).strftime("%H:%M:%S")
        tunka_date_now_label['text'] = datetime.datetime.now(timezone_irkutsk).strftime("%d:%m:%Y")
        utc_date_now_label['text'] = datetime.datetime.now(timezone_utc).strftime("%d:%m:%Y")  

        sleep(1)
        
def info_update():
            
    while True:        
                
        for n in range(len(cluster_frame_list)):
            for i in range(12):
                for j in range(2):
                    station_frame = tk.Frame(cluster_frame_list[n], width=157, height=100, relief=tk.GROOVE, borderwidth=1)
                    station_frame.grid(row=2*n+j, column=i)
                    station_frame.grid_propagate(0)
                    canvas = tk.Canvas(station_frame, width=60, height=95)
                    
                    frequency_color = random.choice(["darkred", "lightgreen"])
                    count_rate_color = random.choice(["dark salmon", "salmon", "light salmon", "tomato", "orange red", "red"])
                    
                    canvas.create_oval(10, 10, 50, 50, fill=count_rate_color)
                    canvas.create_rectangle(10, 60, 50, 70, fill='lightblue')
                    canvas.create_oval(10, 80, 20, 90, fill=frequency_color)
                    canvas.grid(row=0, column=0)
                
                    number = random.randint(0, 200)
                    count_rate = random.randint(0, 200)
                    time = random.randint(0, 200)
                    threshold = random.randint(0, 200)
                    frequency = random.choice(["OK", "NOT OK", "UNKNOWN"])
                    
                    Station(
                            number = number,
                            count_rate = count_rate,
                            time = time,
                            threshold = threshold,
                            frequency = frequency
                            )
                    data_label=tk.Label(station_frame, text = "#: {}\nCR: {}\nTH: {}\nT: {}\nFr: {}".format(
                                        number,count_rate,time,threshold,frequency))
                    data_label.grid(row=0, column=1, sticky='nw')            
                
        sleep(5)

def values_to_hex_color(list_of_values):
    
    list_of_values.sort()
    bottom_color = Color.black
    top_color = Color.red
    gradient = list(bottom_color.range_to(top_color, 20))
    grad_rgb = [x.rgb for x in gradient]
    grad_rgb_255 = [list(map(lambda x: int(x*255), i)) for i in grad_rgb]
    hex_colors_list = []
    for rgb_color in grad_rgb_255:
        hex_color = rgbtohex(rgb_color)
        hex_colors_list.append(hex_color)
    return hex_colors_list
    
def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

        
utc_datetime_now, tunka_datetime_now = today_timemarks()

main_form = tk.Tk()
main_form.title("HiScore shift monitor for {}".format(utc_datetime_now.strftime("%d:%m:%Y")))
main_form.geometry("{}x{}".format(1897,930))

time_frame = tk.Frame(main_form, relief=tk.GROOVE, borderwidth=1)
time_frame.pack(fill=tk.X)
            
utc_date_title_label = tk.Label(time_frame, text="UTC Date:")
utc_time_title_label = tk.Label(time_frame, text="UTC Time:")
tunka_date_title_label = tk.Label(time_frame, text="Tunka Date:")
tunka_time_title_label = tk.Label(time_frame, text="Tunka Time:")
            
utc_date_title_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
utc_time_title_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
tunka_date_title_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
tunka_time_title_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
        
tunka_time_now_label = tk.Label(time_frame, text=tunka_datetime_now.strftime("%H:%M:%S"))
utc_date_now_label = tk.Label(time_frame, text=utc_datetime_now.strftime("%d:%m:%Y") )
utc_time_now_label = tk.Label(time_frame, text=utc_datetime_now.strftime("%H:%M:%S"))
tunka_date_now_label = tk.Label(time_frame, text=tunka_datetime_now.strftime("%d:%m:%Y"))
                
utc_date_now_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
utc_time_now_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
tunka_date_now_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
tunka_time_now_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
        
info_frame = tk.Frame(main_form, relief=tk.GROOVE)
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
            
            frequency_color = random.choice(["darkred", "lightgreen"])
            count_rate_color = random.choice(["dark salmon", "salmon", "light salmon", "tomato", "orange red", "red"])
            
            canvas = tk.Canvas(station_frame, width=60, height=95)
            canvas.create_oval(10, 10, 50, 50, fill=count_rate_color)
            canvas.create_rectangle(10, 60, 50, 70, fill='lightblue')
            canvas.create_oval(10, 80, 20, 90, fill=frequency_color)
            canvas.grid(row=0, column=0)
            
            number = random.randint(0, 200)
            count_rate = random.randint(0, 200)
            time = random.randint(0, 200)
            threshold = random.randint(0, 200)
            frequency = random.choice(["OK", "NOT OK", "UNKNOWN"])

            
            Station(
                    number = number,
                    count_rate = count_rate,
                    time = time,
                    threshold = threshold,
                    frequency = frequency
                    )
            data_label=tk.Label(station_frame, text = "#: {}\nCR: {}\nTH: {}\nT: {}\nFr: {}".format(
                                number,count_rate,time,threshold,frequency))
            data_label.grid(row=0, column=1, sticky='nw')

time_process = threading.Thread(target=time_update)
info_process = threading.Thread(target=info_update)
time_process.start()
info_process.start()
main_form.mainloop()
    
    