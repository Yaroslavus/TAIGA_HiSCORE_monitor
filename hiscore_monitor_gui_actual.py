#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 05:59:17 2021

@author: yaroslav
"""
import datetime
#import tkinter as tk
import threading
import time
#import pytz
import random
#from colour import Color
import os
import re
import subprocess
from operator import attrgetter

#timezone_irkutsk = pytz.timezone('Asia/Irkutsk')
#timezone_utc = pytz.timezone('UTC')

SCRIPT_DIR = os.getcwd()
PORTION_REGULAR_PATTERN = r'Portion=(\d*)' 
FREQUENCE_REGULAR_PATTERN = r'^Station # .* Frequence=(\d*\w*)' 
COUNT_RATE_REGULAR_PATTERN = r'Count Rate = (\d*\.\d*) Hz' 
THRESHOLD_REGULAR_PATTERN = r'Threshold = (\d*)' 
STATION_NUMBER_REGULAR_PATTERN = r'Station # (\d*)' 
TIME_REGULAR_PATTERN = r'Time::  (.*)$'
HOST_CONF_REGULAR_PATTERN = r'.*ID.*'
TLEVEL_REGULAR_PATTERN = r'.*TLevel=(\d*)'
IP_REG = r'^IP.*' 
# =============================================================================
#
# =============================================================================

class Station:
    
    list_of_station = []
    list_of_count_rates = []
    list_of_times = []
    
    def __init__ (self, station_id=0, cluster_number=0, station_number=0, count_rate=0, station_time=0, threshold=0, frequency=0):
        self.station_id = station_id
        self.cluster_number = cluster_number
        self.station_number = station_number
        self.count_rate = count_rate
        self.station_time = station_time
        self.threshold = threshold
        self.frequency = frequency
        self.list_of_station.append(self)
        self.list_of_count_rates.append(self.count_rate)
        self.list_of_times.append(self.station_time)
        
    def show_station(self):
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                self.station_id, self.cluster_number, self.station_number,
                self.count_rate, self.station_time, self.threshold, self.frequency
                ))        
# =============================================================================
#
# =============================================================================

def open_files():
    
    opening_indicator = [0,0,0,0]
    status_files_list = []
    while sum(opening_indicator) < 8:
        print("Try to open status file from CLUSTER 1...")
        try:
            t = time.monotonic()
            subprocess.run(["scp", "hiscore@192.168.1.115:/home/hiscore/krs/NEW_PROGRAMS/hiscore_2018/291021/gro10_status.txt", SCRIPT_DIR + "/out_cluster_1.txt"])
            status_files_list.append("out_cluster_1.txt")
            opening_indicator[0] += 2
        except Exception:
            print("Waiting for CLUSTER_1 status file...")
            opening_indicator[0] += 1
        print("Try to open status file from CLUSTER 2...")
        try:
            t = time.monotonic()
            subprocess.run(["scp", "hiscore@192.168.1.116:/home/hiscore/krs/NEW_PROGRAMS/hiscore_2018/291021/gro10_status.txt", SCRIPT_DIR + "/out_cluster_2.txt"])
            status_files_list.append("out_cluster_2.txt")
            opening_indicator[1] += 2
        except Exception:
            print("Waiting for CLUSTER_2 status files...")
            opening_indicator[1] += 1
        print("Try to open status file from CLUSTER 3...")
        try:
            t = time.monotonic()
            subprocess.run(["scp", "hiscore@192.168.1.119:/home/hiscore/krs/NEW_PROGRAMS/hiscore_2018/291021/gro10_status.txt", SCRIPT_DIR + "/out_cluster_3.txt"])
            status_files_list.append("out_cluster_3.txt")
            opening_indicator[2] += 2
        except Exception:
            print("Waiting for CLUSTER_3 status files...")
            opening_indicator[2] += 1
        print("Try to open status file from CLUSTER 4...")
        try:
            t = time.monotonic()
            subprocess.run(["scp", "hiscore@192.168.1.119:/home/hiscore/krs/NEW_PROGRAMS/HiSCORE_4/291021/gro10_status.txt", SCRIPT_DIR + "/out_cluster_4.txt"])
            status_files_list.append("out_cluster_4.txt")
            opening_indicator[3] += 2
        except Exception:
            print("Waiting for CLUSTER_4 status files...")
            opening_indicator[3] += 1
        print(opening_indicator, sum(opening_indicator))
            
    return status_files_list
# =============================================================================
#
# =============================================================================
    
def start_initialization(file_name):
        
    host_dict = {}
    with open(file_name, "r") as fin:
        file_content = fin.readlines()
        for line in file_content:
            if (re.findall(IP_REG, line)) and (int(line.split()[3])%10 != 0):
                host_dict[int(line.split()[3])] = [int(x) for x in line.split()[6:] if int(x) != 0]
                
    for key, value in host_dict.items():
        for station_id in value:
            if len(str(station_id)) == 3:
                Station(station_id = station_id,
                        cluster_number = int(str(station_id)[0]),
                        station_number = int(str(station_id)[1:])
                        )
            else:
                Station(station_id = station_id,
                        cluster_number = 0,
                        station_number = station_id)
# =============================================================================
#
# =============================================================================

def max_portion_initialization(file_name):
    portion_list = []
    with open(file_name, "r") as fin:
        file_content = fin.readlines()
    for i in range(len(file_content)):
        if (re.findall(PORTION_REGULAR_PATTERN, file_content[i])):
            portion_list.append(int(*list(re.findall(PORTION_REGULAR_PATTERN, file_content[i]))))
    max_portion = max(portion_list)
    for i in range(len(file_content)):
        if (re.findall(PORTION_REGULAR_PATTERN, file_content[i])):
            portion_number = int(*list(re.findall(PORTION_REGULAR_PATTERN, file_content[i])))
            if portion_number == max_portion:
                block_bottom = i 
                block_top = i 
    empty_string_counter = 0 
    while empty_string_counter < 2: 
        block_bottom += 1 
        if file_content[block_bottom] in ("", "\n"): empty_string_counter += 1 
    empty_string_counter = 0 
    while empty_string_counter < 3: 
        block_top -= 1 
        if (file_content[block_top] in ("", "\n")) or len(re.findall("Start DATA", file_content[block_top])) != 0: 
            empty_string_counter += 1 
    chunk = file_content[block_top+1:block_bottom] 
    for station in Station.list_of_station: 
        for line in chunk:
            if re.findall("Frequence", line): 
                if station.station_id == int(line.split()[2]): station.frequency = int(line.split()[-1].split("=")[1], 16) 
            if re.findall(TIME_REGULAR_PATTERN, line): 
                if station.station_id == int(line.split()[2]): station.station_time = line.split()[-1] 
            if re.findall(COUNT_RATE_REGULAR_PATTERN, line): 
                if station.station_id == int(line.split()[2]): station.count_rate = float(line.split()[7]) 
            if re.findall(THRESHOLD_REGULAR_PATTERN, line): 
                if station.station_id == int(line.split()[2]): station.threshold =  int(line.split()[-1])
                
    return max_portion
# =============================================================================
#
# =============================================================================

def main_infinity_loop():

    while sum(while_cycle_bool) != 0:
        print("start new loop")
#        status_files_list = ["gro_1.txt", "gro_2.txt", "gro_3.txt"]
        status_files_list = open_files()   
        print(status_files_list) 
        for i in range(len(status_files_list)):
            print(i)
            current_max_portion = max_portion_initialization(status_files_list[i])
            print("Portion # {} from file {}".format(current_max_portion, status_files_list[i]))
#            for station in sorted(Station.list_of_station, key=attrgetter('cluster_number', 'station_number')): station.show_station()
            print("station list printed")
            if current_max_portion != max_portion[i]:
                max_portion[i] = current_max_portion
            else:
                while_cycle_bool[i] = 0
            print("max portion checked")

#        info_update()
        time.sleep(20)
# =============================================================================
#
# =============================================================================
    
#def today_timemarks():
    
#    return datetime.datetime.now(timezone_utc), datetime.datetime.now(timezone_irkutsk)
# =============================================================================
#
# =============================================================================
#def time_update():
    
#    while True:
        
#        tunka_time_now_label['text'] = datetime.datetime.now(timezone_irkutsk).strftime("%H:%M:%S")
#        utc_time_now_label['text'] = datetime.datetime.now(timezone_utc).strftime("%H:%M:%S")
#        tunka_date_now_label['text'] = datetime.datetime.now(timezone_irkutsk).strftime("%d:%m:%Y")
#        utc_date_now_label['text'] = datetime.datetime.now(timezone_utc).strftime("%d:%m:%Y")  

#        time.sleep(1)
        
#def info_update():
            
#    while True:        
                
#        for n in range(len(cluster_frame_list)):
#            for i in range(16):
#                for j in range(2):
#                    station_frame = tk.Frame(cluster_frame_list[n], width=118, height=100, relief=tk.GROOVE, borderwidth=1)
#                    station_frame.grid(row=2*n+j, column=i)
#                    station_frame.grid_propagate(0)
#                    canvas = tk.Canvas(station_frame, width=45, height=95)
                    
#                    frequency_color = random.choice(["darkred", "lightgreen"])
#                    count_rate_color = random.choice(["dark salmon", "salmon", "light salmon", "tomato", "orange red", "red"])
                    
#                    canvas.create_oval(10, 10, 40, 40, fill=count_rate_color)
#                    canvas.create_rectangle(10, 60, 30, 70, fill='lightblue')
#                    canvas.create_oval(10, 80, 20, 90, fill=frequency_color)
#                    canvas.grid(row=0, column=0)
                
#                    cluster_number = random.randint(0, 200)
#                    station_number = random.randint(0, 200)
#                    count_rate = random.randint(0, 200)
#                    station_time = random.randint(0, 200)
#                    threshold = random.randint(0, 200)
#                    frequency = random.choice(["OK", "NOT OK", "UNKNOWN"])
                    
#                    Station(
#                            station_number = station_number,
#                            cluster_number = cluster_number,
#                            count_rate = count_rate,
#                            station_time = station_time,
#                            threshold = threshold,
#                            frequency = frequency
#                            )
#                    data_label=tk.Label(station_frame, text = "#: {}\nCR: {}\nTH: {}\nT: {}\nFr: {}".format(
#                                        station_number, count_rate, station_time, threshold, frequency), font=('Times', '9'))
#                    data_label.grid(row=0, column=1, sticky='nw')
#        time.sleep(120)
# =============================================================================
#
# =============================================================================
        
#def values_to_hex_color(list_of_values):
#    
#    list_of_values.sort()
#    bottom_color = Color.black
#    top_color = Color.red
#    gradient = list(bottom_color.range_to(top_color, 20))
#    grad_rgb = [x.rgb for x in gradient]
#    grad_rgb_255 = [list(map(lambda x: int(x*255), i)) for i in grad_rgb]
#    hex_colors_list = []
#    for rgb_color in grad_rgb_255:
#        hex_color = rgbtohex(rgb_color)
#        hex_colors_list.append(hex_color)
#    return hex_colors_list
## =============================================================================
##
## =============================================================================
#    
#def rgbtohex(r,g,b):
#    return f'#{r:02x}{g:02x}{b:02x}'
# =============================================================================
#
# =============================================================================

#utc_datetime_now, tunka_datetime_now = today_timemarks()

#main_form = tk.Tk()
#main_form.title("HiScore shift monitor for {}".format(utc_datetime_now.strftime("%d:%m:%Y")))
#main_form.geometry("{}x{}".format(1897,930))

#time_frame = tk.Frame(main_form, relief=tk.GROOVE, borderwidth=1)
#time_frame.pack(fill=tk.X)
            
#utc_date_title_label = tk.Label(time_frame, text="UTC Date:")
#utc_time_title_label = tk.Label(time_frame, text="UTC Time:")
#tunka_date_title_label = tk.Label(time_frame, text="Tunka Date:")
#tunka_time_title_label = tk.Label(time_frame, text="Tunka Time:")
            
#utc_date_title_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
#utc_time_title_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
#tunka_date_title_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
#tunka_time_title_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
        
#tunka_time_now_label = tk.Label(time_frame, text=tunka_datetime_now.strftime("%H:%M:%S"))
#utc_date_now_label = tk.Label(time_frame, text=utc_datetime_now.strftime("%d:%m:%Y") )
#utc_time_now_label = tk.Label(time_frame, text=utc_datetime_now.strftime("%H:%M:%S"))
#tunka_date_now_label = tk.Label(time_frame, text=tunka_datetime_now.strftime("%d:%m:%Y"))
                
#utc_date_now_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
#utc_time_now_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
#tunka_date_now_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
#tunka_time_now_label.pack(side=tk.LEFT, ipadx=4, padx=4, fill=tk.X)
        
#info_frame = tk.Frame(main_form, relief=tk.GROOVE)
#info_frame.pack(fill=tk.X)
#cluster_frame_list = []
#for i in range (4):
            
#    cluster_number_label = tk.Label(info_frame, text="Cluster # " + str(i+1))
#    cluster_number_label.grid(row=2*i, column=0)
#    cluster_frame = tk.Frame(info_frame, relief=tk.GROOVE, borderwidth=1)
#    cluster_frame_list.append(cluster_frame)
#    cluster_frame.grid(row=2*i+1, column=0)
            
            
        
#for n in range(len(cluster_frame_list)):
#    for i in range(12):
#        for j in range(2):
#            station_frame = tk.Frame(cluster_frame_list[n], width=118, height=100, relief=tk.GROOVE, borderwidth=1)
#            station_frame.grid(row=2*n+j, column=i)
#            station_frame.grid_propagate(0)
            
#            frequency_color = random.choice(["darkred", "lightgreen"])
#            count_rate_color = random.choice(["dark salmon", "salmon", "light salmon", "tomato", "orange red", "red"])
            
#            canvas = tk.Canvas(station_frame, width=45, height=95)
#            canvas.create_oval(10, 10, 40, 40, fill="black")
#            canvas.create_rectangle(10, 60, 30, 70, fill='lightblue')
#            canvas.create_oval(10, 80, 20, 90, fill=frequency_color)
#            canvas.grid(row=0, column=0)
            
#            station_number = random.randint(0, 200)
#            cluster_number = random.randint(0, 200)
#            count_rate = random.randint(0, 200)
#            station_time = random.randint(0, 200)
#            threshold = random.randint(0, 200)
#            frequency = random.choice(["OK", "NOT OK", "UNKNOWN"])

#            Station(
#                    cluster_number = cluster_number,
#                    station_number = station_number,
#                    count_rate = count_rate,
#                    station_time = station_time,
#                    threshold = threshold,
#                    frequency = frequency
#                    )
#            data_label=tk.Label(station_frame, text = "#: {}\nCR: {}\nTH: {}\nT: {}\nFr: {}".format(
#                                station_number, count_rate, station_time, threshold, frequency), font=('Times', '9'))
#            data_label.grid(row=0, column=1, sticky='nw')

#status_files_list = ["gro_1.txt", "gro_2.txt", "gro_3.txt"]
status_files_list = open_files()
for file_name in status_files_list:
    start_initialization(file_name)
max_portion = [1]*len(status_files_list)
while_cycle_bool = [1]*len(status_files_list)
main_infinity_loop()
        

#time_process = threading.Thread(target=time_update)
#info_process = threading.Thread(target=main_infinity_loop)
#time_process.start()
#info_process.start()
#main_form.mainloop()

