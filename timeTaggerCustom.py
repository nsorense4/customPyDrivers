# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys
import numpy
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


# for plotting real time
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from datetime import datetime
import os

import tkinter as tk

try:
    import TimeTagger
except:
    print ("Time Tagger lib is not in the search path.")
    pyversion = sys.version_info
    from winreg import ConnectRegistry, OpenKey, HKEY_LOCAL_MACHINE, QueryValueEx
    registry_path = "SOFTWARE\\Python\\PythonCore\\" + str(pyversion.major) + "." + str(pyversion.minor) + "\\PythonPath\\Time Tagger"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    key = OpenKey(reg, registry_path) 
    module_path = QueryValueEx(key,'')[0]
    print ("adding " + module_path)
    sys.path.append(module_path)
    
from TimeTagger import (createTimeTagger, Combiner, Coincidence, Counter, 
                        Countrate, Correlation, TimeDifferences, TimeTagStream, 
                        Scope, Event, CHANNEL_UNUSED, UNKNOWN, LOW, HIGH)

import time
from time import sleep

        
class timeTaggerCustom(tk.Frame):
    def __init__(self, parent):
        global LARGE_FONT
        
        tk.Frame.__init__(self)
        tk.Frame.__init__(self)
        label = tk.Label(self, text="TimeTagging", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def initTimeTagger(channels, trig=0.1, deadtime=6000):
        # create a timetagger instance
        lenChannels = int(len(channels))
        tagger = createTimeTagger()
        tagger.reset()
        
        #Set the trigger level and deadtime for each channel
        for i in range(lenChannels):
            tagger.setTriggerLevel(i, trig)
            tagger.setDeadtime(i, deadtime)
            tagger.setInputDelay(channel=channels[i],delay=0)
        tagger.sync()
        
        #set the channels to count
        cr = Countrate( tagger, channels=channels )
        tagger.sync()
        
        return tagger, cr

    def animateCountrate(channels, crData, timeList, startTime, timeInt, cr):
        global a, f
        timeList = np.roll(timeList, -1, axis = 0)
        timeList[-1] = time.time()-startTime
        crData = np.roll(crData, -1, axis = 0)
        crData[-1, :] = cr.getData()
        
        a.clear()
        for i in range(len(channels)):
            a.plot(timeList, crData[:,i])
        
        a.set_xlabel('Time (s)')
        a.set_ylabel('Power (mW)')
        f.tight_layout()
        time.sleep(timeInt)
        
    # def animateCountrateHistogram(i):
    #     global data
    
    #     timeList = shift(timeList, -1, cval = time.time()-startTime)
    #     a.clear()
    #     if config == configPM100D:
    #         a.plot(timeList, powerList)
    #     elif config == configDAQ:
    #         a.plot(timeList, powerList)
    #         a.plot(timeList, powerList0)
    #         a.plot(timeList, powerList5320)
        
    #     a.set_xlabel('Time (s)')
    #     a.set_ylabel('Power (mW)')
    #     f.tight_layout()
    #     time.sleep(timeInt)
    
    # def crossCorrelation():

    #     # create a timetagger instance
    #     tagger = createTimeTagger()
    #     tagger.reset()
        
        
    #     # Set the trigger level and deadtime for each channel
    #     [tagger.setTriggerLevel(i, trig) for i in range(8)]
    #     [tagger.setDeadtime(i, deadtime) for i in range(8)]
        
    #     #delay the two beamsplit channels to coincide with zero time difference at the idler (correlation)
    #     tagger.setInputDelay(channel=chan1,delay=0)#-3900)
    #     tagger.setInputDelay(channel=chan2,delay=0)#-0, 2900)
    #     tagger.sync()
        
    #     # cross correlation between channels 6 and 7, and 5 and 7
    #     corr = Correlation(tagger, channel_1=chan1, channel_2=chan2, binwidth=binwidth, n_bins=binnumber)
    #     tstart = time.time()    # for profiling
        
    #     sleep(1)
    #     fig, ax = plt.subplots(1, 1)
    #     corr_plot, = fig.plot(corr.getIndex()/1e3, corr.getData(), label= str(chan1)+'/'+str(chan2))
    #     ax.set_xlabel('Time [ns]')
    #     ax.set_ylabel('Correlations/sec')
    #     ax.set_title('Cross correlation between channel 5 and 7')

class application(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Timetagging")
        tk.Button(self, text="stop", command=self.stopAndSave).pack()
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame1 = timeTaggerCustom(self)
        self.frames[timeTaggerCustom] = frame1
        frame1.grid(row=0, column=0, sticky="nsew")
        self.show_frame(timeTaggerCustom)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        
    def stopAndSave():
        global data
        
        dateTimeObj = datetime.now()
        preamble = (str(dateTimeObj.year) + str(dateTimeObj.month) + str(dateTimeObj.day) + '-'
                    + str(dateTimeObj.hour) + '_' + str(dateTimeObj.minute) + '_' +
                    str(dateTimeObj.second))
        
        fileName = ("C:/Users/srv_plank/Documents/computerGeneratedHolography/data/" 
                    + preamble + 'Exposure.csv')
        if not os.path.exists(fileName): np.savetxt(fileName, data, delimiter=",")
        
        raise Exception('Saving data.')    

       

def startCountrate(channels = [1,2], N = 100,  binwidth = 1000, binnumber = 200, timeInt = 0.2):
    global LARGE_FONT, f, a
    LARGE_FONT = ("Verdana", 12)
    style.use("ggplot")
    
    f = Figure(figsize=(5,5), dpi=100)
    a = f.add_subplot(111)
    
    # initialize time tagger
    tagger, cr = timeTaggerCustom.initTimeTagger(channels = channels)
    lenChannels = int(len(channels))
    
    #wait and then start taking data
    sleep(0.1)
    
    startTime = time.time()
    crData = np.zeros([N, lenChannels])
    timeList = np.zeros(N)
    
    app = application()
    ani = animation.FuncAnimation(f, 
                                  timeTaggerCustom.animateCountrate(channels, crData, 
                                                        timeList, startTime, 
                                                        timeInt, cr),
                                  interval=100)
    app.mainloop()

if __name__ == "__main__":
    startCountrate()
