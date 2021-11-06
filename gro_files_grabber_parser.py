#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 06:43:26 2021

@author: yaroslav
"""

import os
#import subprocess
#import sys
import re
#from hiscore_monitor_gui import Station

SCRIPT_DIR = os.getcwd()
PORTION_REGULAR_PATTERN = r'Portion=(\d*)' 
FREQUENCE_REGULAR_PATTERN = r'Frequence=(\d*\w*)' 
COUNT_RATE_REGULAR_PATTERN = r'(\d*\.\d*) Hz' 
THRESHOLD_REGULAR_PATTERN = r'Threshold = (\d*)' 
STATION_NUMBER_REGULAR_PATTERN = r'# (\d*)' 
TIME_REGULAR_PATTERN = r'Time::  (.*)$'

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

