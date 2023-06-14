# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 10:25:33 2023

@author: Nicholas Sorensen - nicholasjsorensen@gmail.com
referenced https://pythonprogramming.net/embedding-live-matplotlib-graph-tkinter-gui/
"""


import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

import tkinter as tk
import time as time
import sys

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

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

N = 100
timeInt = 0.1
startTime = time.time()
yy = np.zeros(N)
timeArr = np.linspace(-N*timeInt, 0, N)

class timeTaggerCustom():
        
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

def animateTest(i):
    global yy, timeArr

    
    timeArr = np.roll(timeArr, -1, axis = 0)
    timeArr[-1] = time.time()-startTime
    a.clear()
    yy = np.sin(timeArr)

    a.plot(timeArr, yy)
    
    a.set_xlabel('x')
    a.set_ylabel('y')
    f.tight_layout()
    time.sleep(timeInt)
    
def animateCounts(i, cr, crData, channels):
    global timeArr

    
    timeArr = np.roll(timeArr, -1, axis = 0)
    timeArr[-1] = time.time()-startTime
    a.clear()
   
    crData = np.roll(crData, -1, axis = 0)
    crData[-1, :] = cr.getData()

    for i in range(len(channels)):
        a.plot(timeArr, crData[:,i])
    
    a.set_xlabel('x')
    a.set_ylabel('y')
    f.tight_layout()
    time.sleep(timeInt)

    
class application(tk.Tk):

    def __init__(self, title, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, title)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame1 = powerMonitor(container, self, frameTitle = title)
        self.frames[powerMonitor] = frame1
        frame1.grid(row=0, column=0, sticky="nsew")
        self.show_frame(powerMonitor)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class powerMonitor(tk.Frame):

    def __init__(self, parent, controller, frameTitle):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=frameTitle, font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
class runApp():
    def test():
        app = application(title = "Test")
        ani = animation.FuncAnimation(f, animateTest, interval=100)
        app.mainloop()
        
    def countrate(channels):
        tagger, cr = timeTaggerCustom.initTimeTagger(channels = channels)
        crData = np.zeros(N, len(channels))
        
        app = application(title = "Test")
        ani = animation.FuncAnimation(f, animateCounts(cr, crData, channels), interval=100)
        app.mainloop()
        
if __name__ == "__main__":
    runApp.test()
        
