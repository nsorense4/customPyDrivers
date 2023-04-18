# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 12:20:50 2023

@author: Nicholas Sorensen - nicholasjsorensen@gmail.com
referenced https://pythonprogramming.net/embedding-live-matplotlib-graph-tkinter-gui/
"""


import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import nidaqmx
from datetime import datetime
import os

import tkinter as tk
import sys
from tkinter import ttk
import time as time
from scipy.ndimage.interpolation import shift

sys.path.append('/Users/srv_plank/Documents/Python/Core/Drivers')

from PM100D import PM100D as PM100D

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)


N = 100
timeInt = 0.1
startTime = time.time()
powerList = np.zeros(N)
powerList0 = np.zeros(N)
powerList1 = np.zeros(1)
powerList2 = np.zeros(1)
timeListAppend = np.zeros(1)
timeList = np.linspace(-N*timeInt, 0, N)

configPM100D = 0
configDAQ = 1
config = configDAQ
appendBool = False

initDAQ = False

def initDAQPD(avg = 10):
    DAQ = nidaqmx.Task("task")
    DAQ.ai_channels.add_ai_voltage_chan("Dev1/ai0", min_val=0, max_val=10)
    DAQ.ai_channels.add_ai_voltage_chan("Dev1/ai1", min_val=0, max_val=10)
    
    return DAQ

if config == configPM100D:
    PD = PM100D()
elif config == configDAQ:
    if initDAQ == True:
        DAQ = initDAQPD()
    
def convV2Int(volt):
    # scatters for first order: 2.505 V, 1.345 mW, 2.82900037e-06 V, 0 mW
    # zero order: 2.27825 V, 1.236 mW,  6.47855904e-06 V, 0 mW
    slope = np.array([1.345/(2.505-0.01197444), 1.236/(2.27825-0.00533462)])
    intercept = slope*np.array([0.01197444, (0.00533462)])
    return slope*volt - intercept
    
def readPD(DAQ, PD = '0th', avgNum = 10):
    # scale = np.array([1.236/2.27825, 1.345/2.505]) # mW/V
    volt = np.mean(np.asarray(DAQ.read(number_of_samples_per_channel=avgNum)), axis = 1)
    intensity = convV2Int(volt) #/ 1000

    return intensity


def animate(i):
    global powerList, timeList, powerList0
    if config == configPM100D:
        powerList = shift(powerList, -1, cval = PD.readPower()*1000)
    elif config == configDAQ:
        power = readPD(DAQ)
        powerList = shift(powerList, -1, cval = power[0])
        powerList0 = shift(powerList0, -1, cval = power[1])
    
    timeList = shift(timeList, -1, cval = time.time()-startTime)
    a.clear()
    if config == configPM100D:
        a.plot(timeList, powerList)
    elif config == configDAQ:
        a.plot(timeList, powerList)
        a.plot(timeList, powerList0)
    
    a.set_xlabel('Time (s)')
    a.set_ylabel('Power (mW)')
    f.tight_layout()
    time.sleep(timeInt)
    
def animateAppend(i):
    global powerList1, timeListAppend, powerList2
    power = readPD(DAQ)
    powerList1 = np.append(powerList1,power[0])
    powerList2 = np.append(powerList2,power[1])
    timeListAppend = np.append(timeListAppend,time.time()-startTime)
    a.clear()
    a.plot(timeListAppend, powerList1)
    a.plot(timeListAppend, powerList2)
    
    a.set_xlabel('Time (s)')
    a.set_ylabel('Power (mW)')
    f.tight_layout()
    time.sleep(timeInt)
    
def stopAndSave():
    global powerList1, timeListAppend, powerList2
    
    data = np.vstack([timeListAppend, powerList1, powerList2])
    
    dateTimeObj = datetime.now()
    preamble = (str(dateTimeObj.year) + str(dateTimeObj.month) + str(dateTimeObj.day) + '-'
                + str(dateTimeObj.hour) + '_' + str(dateTimeObj.minute) + '_' +
                str(dateTimeObj.second))
    
    fileName = ("C:/Users/srv_plank/Documents/computerGeneratedHolography/data/" 
                + preamble + 'Exposure.csv')
    if not os.path.exists(fileName): np.savetxt(fileName, data, delimiter=",")
    
    raise Exception('Ending the exposure recording.')

    
class application(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "PM100D Power Monitoring")
        tk.Button(self, text="stop", command=stopAndSave).pack()
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame1 = powerMonitor(container, self)
        self.frames[powerMonitor] = frame1
        frame1.grid(row=0, column=0, sticky="nsew")
        self.show_frame(powerMonitor)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class powerMonitor(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="PM100D Power Monitoring", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        # button = ttk.Button(self, text="Visit Page 1",
        #                     command=lambda: controller.show_frame(PageOne))
        # button.pack()      

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        


app = application()
if appendBool == True:
    ani = animation.FuncAnimation(f, animateAppend, interval=100)
else:
    ani = animation.FuncAnimation(f, animate, interval=100)
app.mainloop()