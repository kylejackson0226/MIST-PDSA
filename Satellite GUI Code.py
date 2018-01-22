'''
#https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
Although this webpage uses classes to define pages. Instead, we use ttk notebooks to define pages

Dual y-axis graph from https://matplotlib.org/examples/api/two_scales.html
'''

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

import urllib
import json

import pandas as pd
import numpy as np
from random import randint

from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

import re

from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

#import turtle
import time
import datetime

from array import array
import binascii
from binascii import hexlify
import os
from tkinter import filedialog

import urllib
from urllib.request import urlopen

main = Tk()
main.title('NEUDOSE')
main.geometry('1000x1000')

real_data_array = []                # This is the BIG MULTIDIMENSIONAL ARRAY; Define as a global; Note that channel numbers are shifted by 2 (i.e. channel 0 is in element 2)

'''
rows = 0
while rows < 10:
    main.rowconfigure(rows, weight=1)
    main.columnconfigure(rows, weight=1)
    rows += 1
'''

nb = ttk.Notebook(main)
nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')

'''******************************
Page 1 - House Keeping
******************************'''

page1 = ttk.Frame(nb)
nb.add(page1, text='Housekeeping')


pressureTemperatureGraph = Figure() #figsize=(2,5), dpi=100

def threshold_plot(ax, x, y, threshv, color, overcolor):
    """
    Helper function to plot points above a threshold in a different color

    Parameters
    ----------
    ax : Axes
        Axes to plot to
    x, y : array
        The x and y values

    threshv : float
        Plot using overcolor above this value

    color : color
        The color to use for the lower values

    overcolor: color
        The color to use for values over threshv

    """
    # Create a colormap for red, green and blue and a norm to color
    # f' < -0.5 red, f' > 0.5 blue, and the rest green
    cmap = ListedColormap([color, overcolor])
    norm = BoundaryNorm([np.min(y), threshv, np.max(y)], cmap.N)

    # Create a set of line segments so that we can color them individually
    # This creates the points as a N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be numlines x points per line x 2 (x and y)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:], points[:]], axis=1)

    # Create the line collection object, setting the colormapping parameters.
    # Have to set the actual values used for colormapping separately.
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(y)

    ax.add_collection(lc)
    ax.set_xlim(np.min(x), np.max(x))
    ax.set_ylim(np.min(y)*1.1, np.max(y)*1.1)
    return lc

pressureTemperatureGraph, ax = plt.subplots()

x = np.linspace(0, 3 * np.pi, 500)
y = np.sin(x)

lc = threshold_plot(ax, x, y, .50, 'k', 'r')
#ax.axhline(.75, color='k', ls='--')
lc.set_linewidth(3)


'''pressureTemperatureGraph, ax1 = plt.subplots()
t = np.arange(0.01, 10.0, 0.01)
s1 = np.exp(t)
ax1.plot(t, s1, 'b-')
ax1.set_xlabel('time (s)')
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('Temperature', color='b')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()
s2 = np.sin(2 * np.pi * t)
ax2.plot(t, s2, 'r.')
ax2.set_ylabel('Pressure', color='r')
ax2.tick_params('y', colors='r')'''

'''def PTGraphColourGradient():
    a=np.outer(np.arange(0,1,0.01),np.ones(10))
    fact = 1.0/255.0
    cdict2 = {'red':  [(0.0,  222*fact, 222*fact),
                       (0.25, 133*fact, 133*fact),
                       (0.5,  191*fact, 191*fact),
                       (0.75, 151*fact, 151*fact),
                       (1.0,   25*fact,  25*fact)],
             'green': [(0.0,   0*fact,  0*fact),
                       (0.25, 182*fact, 182*fact),
                       (0.5,  217*fact, 217*fact),
                       (0.75, 203*fact, 203*fact),
                       (1.0,   88*fact,  88*fact)],
             'blue':  [(0.0,    0*fact, 0*fact),
                       (0.25, 222*fact, 222*fact),
                       (0.5,  214*fact, 214*fact),
                       (0.75, 143*fact, 143*fact),
                       (1.0,   40*fact,  40*fact)]} 
    my_cmap2 = matplotlib.colors.LinearSegmentedColormap('my_colormap2',cdict2,256)
    plt.imshow(a,aspect='auto', cmap =my_cmap2) 

def bluegreen(y):
    red = [(0.0, 0.0, 0.0), (0.5, y, y), (1.0, 0.0, 0.0)]
    green = [(0.0, 0.0, 0.0), (0.5, y, y), (1.0, y, y)]
    blue = [(0.0, y, y), (0.5, y, y),(1.0,0.0,0.0)]
    colordict = dict(red=red, green=green, blue=blue)
    bluegreenmap = LinearSegmentedColormap('bluegreen', colordict, 256)
    return bluegreenmap'''

pressureTemperatureGraph_a = pressureTemperatureGraph.add_subplot(111)


#plt.show()


def PT_Data_Import(i):
    #pullData = open("sampleDataPressure.txt","r").read()
    #dataList = pullData.split('\n')
    xList = []
    yList = []
    
    x = 0
    for data_packet_array in real_data_array:
        #if len(eachLine) > 1:
            x +=1
            y = data_packet_array[2]
            #x, y = eachLine.split(',')
            
            xList.append(int(x))
            yList.append(int(y))

    pressureTemperatureGraph_a.clear()
    pressureTemperatureGraph_a.plot(xList, yList)
    pressureTemperatureGraph_a.set_xlabel('time')
    pressureTemperatureGraph_a.set_ylabel('temperature')
    pressureTemperatureGraph_a.set_title('NEUDOSE Temperature-Pressure Graph')
    
'''def PT_Data_Import_From_DummySampleFile(i):
    pullData = open("sampleDataPressure.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    pressureTemperatureGraph_a.clear()
    pressureTemperatureGraph_a.plot(xList, yList)'''
    
canvasPT = FigureCanvasTkAgg(pressureTemperatureGraph, page1)
canvasPT.show()
canvasPT.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

#pressureTemperatureGraph.display(page1)

'''fig, ax1 = plt.subplots()
t = np.arange(0.01, 10.0, 0.01)
s1 = np.exp(t)
ax1.plot(t, s1, 'b-')
ax1.set_xlabel('time (s)')
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('exp', color='b')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()
s2 = np.sin(2 * np.pi * t)
ax2.plot(t, s2, 'r.')
ax2.set_ylabel('sin', color='r')
ax2.tick_params('y', colors='r')

fig.tight_layout()
#plt.show()
#plt.draw()'''

def import_NEUDOSE_Data():

    '''
    Describe Data Format and reference with URL (confluence page)

    Channel 0: Pressure
    Channel 1: Pressure
    Channel 2: Temperature
    Channel 3: Temperature
    Channel 4: Voltage
    Channel 5: Voltage
    Channel 6: Voltage
    Channel 7: Voltage

    Current as of June 26th 2017
    
    '''

    #Open the data file using a dialog box
    #give link to URL of the example from the web
    root = tk.Tk()
    root.withdraw()
    root.update()
    root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                           filetypes=[("Text Files", "*.txt")])
    print(root.filename)
    root.filenamecsv = re.sub('.txt', '.csv', root.filename)        #need a better regex to make sure you're getting the rightmost replacement (just in case)
    print(root.filenamecsv)

    #Open a file for exporting the data as formatted csv; allows easier access to the data if needed further analysis
    # *** NEED TO NAME FILE SOMETHING APPROPRIATE BASED ON THE ORIGINAL FILE NAME ***
    test_dump = open(root.filenamecsv, "a+")



    data_string = open(root.filename,"r").read()
    #string ="FFFF07E155165516110D04F62836400060008000A036C000E000FFFF07E155165516110D05062835400060008000A036C000E000FFFF07E15516110D05062835400060008000A036C000E000FFFF07E15516110D04F32835400060008000A036C000E000FFFF07E15516110D04F62835400060008000A036C000E000FFFF07E15516110D04D42836400060008000A036C000E000FFFF07E15516110D04F62836400060008000A036C000E000FFFF07E15516110D04F42836400060008000A036C000E000FFFF07E15516110D04C62834400060008000A036C000E000" 
    #string = string.replace('FFFF',',')
    string = data_string.split('FFFF')      # split data stream at FFFF; timestamp and corresponding data end up in an array element
    #string.pop(0)
    if len(string[0]) > 0:                      # check that no weird characters preceeded the initial FFFF
        print("Unexpected Data", string[0])
        print('')
        string.pop(0)
        print(string[0])
    else:
        if len(string[0]) == 0:                 # removed first empty data; this is an artifact of the python split function; empty first element will give error later the routine
            string.pop(0)


    packet_index = 0
    date_placeholder = 0
    for packet in string:                    # loop through all the data to further extract dates and channel signal into 
        packet_data_array = []              # this will contain the parsed packet data; channels shift by 2 (i.e. channel 0 is in element 2)
        if len(packet) > 0:

            packet_data_array.append(packet_index)
            print(packet)
            print(len(packet))
            test_dump.write(packet)          # write the whole string to the csv file
            test_dump.write(",")

            Date_of_transmission_to_Binary = bin(int(packet[0:11],16))[2:].zfill(16)
            Date_of_transmission = str(int(Date_of_transmission_to_Binary,2))

            print("date is",Date_of_transmission)   #packet[0:12]
            test_dump.write(Date_of_transmission)    # write the date to the csv file
            test_dump.write(",")
            packet_data_array.append(packet[0:12])
            

            channel_number_counter = 0
            while channel_number_counter < 8:          # loop through each of the channels; write them to csv file; put them into appropriate array for plotting
                channel_data = packet[(12+4*channel_number_counter):(16+4*channel_number_counter)]

                print("date:",date_placeholder,"; channel:",channel_number_counter,"; signal:",channel_data)

                #binary_data = binascii.unhexlify(i[12:16])
                #print(binary_data)

 

                #data = bin(int(str(channel_data), 16))[2:].zfill(16)
                #print(data)
                #data = serial.readline()

                data = bin(int(channel_data,16))[2:].zfill(16)
                print(data)

                print ("Channel Number is",int(data[0:3],2),'  ',data[0:3])
                print ("ADC Signal is", int(data[4:],2),'  ',data[4:])
                test_dump.write(str(int(data[0:3],2)))      # this is the channel ID/number
                test_dump.write(",")
                test_dump.write(str(int(data[4:],2)))
                test_dump.write(",")
                #if channel_number_counter == 1:
                packet_data_array.append(int(data[4:],2))
                channel_number_counter += 1
                
            print (packet_data_array)
            real_data_array.append(packet_data_array)

            if packet_index ==4:
                print(real_data_array)
                #time.sleep(60)

            

            test_dump.write("\n")
            print('')
        else:
            print("Error")
            print('')
        packet_index += 1
        date_placeholder += 1
        
    test_dump.close()

    
    
import_button_temperaturepressure = Button(page1, text = "Import Temperature/Pressure Data", command=import_NEUDOSE_Data)
import_button_temperaturepressure.pack()

'''url = 'http://laspace.lsu.edu/hasp/groups/2017/data/data.php?pname=Payload_03&py=2017'

file_name = url.split('/')[-1]
u = urllib.urlopen(url)
f = open(file_name, 'wb')
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print("Downloading: %s Bytes: %s") % (file_name, file_size)

file_size_dl = 0
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break

    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print(status),

f.close()'''

'''
urllib.urlretrieve (url)

response = urlopen(url)
CHUNK = 16 * 1024
with open(file, 'wb') as f:
    while True:
        chunk = response.read(CHUNK)
        if not chunk:
            break
        f.write(chunk)

f = urllib.urlopen(url)    
fh = open('data.php', 'wb')
fh.write(f.read())
fh.close()'''

'''******************************
Page 2 - Energy/Dose
******************************'''

page2 = ttk.Frame(nb)
nb.add(page2, text='TEPC')

energyGraph = Figure() #figsize=(2,5), dpi=100
energyGraph_a = energyGraph.add_subplot(111)

def Energy_Data_Import(i):
    '''#pullData = open("sampleDataEnergy.txt","r").read()
    #dataList = pullData.split('\n')

    xList = []
    yList = []

    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    energyGraph_a.clear()
    energyGraph_a.plot(xList, yList)'''

    #pullData = open("sampleDataPressure.txt","r").read()
    #dataList = pullData.split('\n')
    xList = []
    yList = []
    
    x = 0
    for data_packet_array in real_data_array:
        #if len(eachLine) > 1:
            x +=1
            y = data_packet_array[3]
            #x, y = eachLine.split(',')
            
            xList.append(int(x))
            yList.append(int(y))

    energyGraph_a.clear()
    energyGraph_a.plot(xList, yList)
    energyGraph_a.set_xlabel('Time')
    energyGraph_a.set_ylabel('Energy')
    energyGraph_a.set_title('NEUDOSE Energy Graph')

canvasE = FigureCanvasTkAgg(energyGraph, page2)
canvasE.show()
canvasE.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

button_Import_TEPC = Button(page2, text = "Import TEPC Data", command=import_NEUDOSE_Data)
button_Import_TEPC.pack()
    


#pressureTemperatureGraph.display(page2)

'''
toolbar = NavigationToolbar2TkAgg(canvas, self)
toolbar.update()
canvas._tkcanvas.pack(page2, side=tk.TOP, fill=tk.BOTH, expand=True)
'''

'''******************************
Page 3 - Sensor Ring
******************************'''

page3 = ttk.Frame(nb)
nb.add(page3, text='ACD Sensor Ring')

sensorRingGraph = Figure(figsize=(5,5)) #, dpi=100
#sensorRingGraphAxis = sensorRingGraph.add_axes([0,0,1,1],frameon=False)
#sensorRingGraphAxis.set_xlim(0,1),sensorRingGraphAxis.set_xticks([])
#sensorRingGraphAxis.set_ylim(0,1),sensorRingGraphAxis.set_yticks([])
sensorRingGraph_a = sensorRingGraph.add_subplot(111)

def sensorRing_Data_Import(i):

    #For the moment, this function generates data for the sensor rings
    #It first creates the x,y co-ordinates for each sensor to be displayed on an x-y graph
    #Then it randomly picks a sensor to be 'hot' and sets a new colour/size for that sensor
    
    numberOfSensors = 30
    plottingSensorRadius = 1

    sensorIndex = 0
    xListRing = []
    yListRing = []
    hotListRing = []
    hotSensor = randint(0,(3*numberOfSensors))
    #print(hotSensor)
    
    sensorRingGraph_a.clear()
    sensorRingGraph_a.set_title('ACD SiPM Sensors')
    
    while (sensorIndex < numberOfSensors):
       #print('The sensor index is:', sensorIndex,'  ',sensorIndex * (2 * np.pi / numberOfSensors))
       angle = sensorIndex * (2 * np.pi / numberOfSensors)
       xRing = plottingSensorRadius * np.cos(angle)
       yRing = plottingSensorRadius * np.sin(angle)
       xListRing.append(float(xRing))
       yListRing.append(float(yRing))

       '''
       if(sensorIndex == hotSensor):
           hotListRing.append('r')
       else:
           hotListRing.append('b')
           
       #sensor[sensorIndex] = (x,y)
       #print('The sensor index is:', sensorIndex,'  ',sensorIndex * (2 * np.pi / numberOfSensors),'  x:',x,'  y:',y)
       '''
       if(sensorIndex == hotSensor):
           #print('*',sensorIndex,hotSensor,xRing,yRing)
           sensorRingGraph_a.plot(xRing, yRing, marker='o', color='r', markersize='20') #, marker='o', color='b', markersize='25'
       else:
           #print(sensorIndex,hotSensor,xRing,yRing)
           sensorRingGraph_a.plot(xRing, yRing, marker='o', color='b', markersize='5') #y, marker='o', color='r', markersize='10'
       
       sensorIndex += 1
    #sensorRingGraph_a.clear()
    #sensorRingGraph_a.plot(xListRing, yListRing, linewidth='0', marker='o', color='b', markersize='10')

canvasSensorRing = FigureCanvasTkAgg(sensorRingGraph,page3)
canvasSensorRing.show()
canvasSensorRing.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


'''
matplotlib incline

T = [1, 10, 20, 30, 40, 50, 60]
R = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

def rtpairs(r, n):

    for i in range(len(r)):
       for j in range(n[i]):    
        yield r[i], j*(2 * np.pi / n[i])

for r, t in rtpairs(R, T):
    plt.plot(r * np.cos(t), r * np.sin(t), 'bo')
plt.show(page3)'''

'''canvas_width = 500
canvas_height =500

w = Canvas(page3, 
           width=canvas_width, 
           height=canvas_height)
w.pack()

w.create_oval(10,10,490,490)
w.create_oval(30,30,470,470)

radius = 100'''
#turtle.speed(0)

'''for rings in range(2):
    turtle.penup()
    turtle.goto(0, -radius)
    turtle.pendown()
    turtle.circle(radius)
    radius += 30'''

'''******************************
Page 4 - Form/Log for Comments
******************************'''
page4 = ttk.Frame(nb)
nb.add(page4, text='SiPM Analysis')

sensorRingGraph2 = Figure(figsize=(5,5))
sensorRingGraph2_a = sensorRingGraph2.add_subplot(111)

def sensorRing_Data_Analysis(i):

    #For the moment, this function generates data for the sensor rings
    #It first creates the x,y co-ordinates for each sensor to be displayed on an x-y graph
    #Then it randomly picks a sensor to be 'hot' and sets a new colour/size for that sensor
    
    numberOfSensors2 = 30
    plottingSensorRadius2 = 1

    sensorIndex2 = 0
    xListRing2 = []
    yListRing2 = []
    hotListRing2 = []
    hotSensor = randint(0,(3*numberOfSensors))
    #print(hotSensor)
    
    sensorRingGraph2_a.clear()
    sensorRingGraph2_a.set_title('ACD SiPM Sensors Analysis')
    
    while (sensorIndex2 < numberOfSensors2):
       #print('The sensor index is:', sensorIndex,'  ',sensorIndex * (2 * np.pi / numberOfSensors))
       angle = sensorIndex2 * (2 * np.pi / numberOfSensors2)
       xRing2 = plottingSensorRadius * np.cos(angle)
       yRing2 = plottingSensorRadius * np.sin(angle)
       xListRing2.append(float(xRing2))
       yListRing2.append(float(yRing2))

       '''
       if(sensorIndex == hotSensor):
           hotListRing.append('r')
       else:
           hotListRing.append('b')
           
       #sensor[sensorIndex] = (x,y)
       #print('The sensor index is:', sensorIndex,'  ',sensorIndex * (2 * np.pi / numberOfSensors),'  x:',x,'  y:',y)
       '''
       if(sensorIndex == hotSensor):
           #print('*',sensorIndex,hotSensor,xRing,yRing)
           sensorRingGraph2_a.plot(xRing2, yRing2, marker='o', color='r', markersize='20') #, marker='o', color='b', markersize='25'
       else:
           #print(sensorIndex,hotSensor,xRing,yRing)
           sensorRingGraph2_a.plot(xRing2, yRing2, marker='o', color='b', markersize='5') #y, marker='o', color='r', markersize='10'
       
       sensorIndex2 += 1
    #sensorRingGraph_a.clear()
    #sensorRingGraph_a.plot(xListRing, yListRing, linewidth='0', marker='o', color='b', markersize='10')


canvasSensorRing2 = FigureCanvasTkAgg(sensorRingGraph2,page4)
canvasSensorRing2.show()
canvasSensorRing2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
'''******************************
Page 5 - Form/Log for Comments
******************************'''

page5 = ttk.Frame(nb)
nb.add(page5, text='LOG')

#Name entry section

name = Label(page5, text='Operator')
name_entry = Entry(page5)

name.grid(row=0, column=0)
name_entry.grid(row=0, column=1)

#checkboxes section

c = Checkbutton(page5, text = 'All Systems Fine')
c.grid(row=2, column=0, columnspan=1, sticky='W')
c = Checkbutton(page5, text = 'Systems could need improving')
c.grid(row=3, column=0, columnspan=1, sticky='W')
c = Checkbutton(page5, text = 'Systems really need to be improved')
c.grid(row=4, column=0, columnspan=1, sticky='W')

#textbox comment section

comment_section = Text(page5)
comment_section.grid(row=5)

#Submit Button section
def submit():
    tkinter.messagebox.showinfo('Operator\'s Response - ' + name_entry.get(), comment_section.get("1.0",'end-1c'))
    human_readable_time=(datetime.date.today().strftime("%A"), #day of the week
            datetime.date.today().strftime("%B"), #the month
            datetime.date.today().strftime("%d"), #day of the month
            datetime.date.today().strftime("%Y"), #current year
                         )
    f= open("guru99.txt","a+")
     #f=open("guru99.txt","a+")
    for i in range(1):
        #time stamp of comment                                       
        f.write(str(human_readable_time) + "\n")
        #transfering the comment section content to the flat file
        f.write(comment_section.get("1.0",'end-1c')+"\n")
        #+"Kyle This is line %d\r\n" % (i+1)
    f.close()
    print('done writing to file')
    
button1 = Button(page5, text = 'Submit', fg='blue', command=submit)
button1.grid(row= 6, column=0)

'''
def feedback():
    f= open("guru99.txt","w+")
    #f=open("guru99.txt","a+")
    for i in range(11):
#        f.write(comment_section+"Kyle This is line %d\r\n" % (i+1))
    f.close()   
   #Open the file back and read the contents
    f=open("guru99.txt", "r")
    if f.mode == 'r': 
        contents =f.read()
        print (contents)
   #or, readlines reads the individual line into a list
    fl =f.readlines()
    for x in fl:
        print (x)
#if __name__== "__main__":
#  feedback()
'''

'''******************************
Main Code Area
******************************'''

#print(human_readable_time)

ring = animation.FuncAnimation(sensorRingGraph, sensorRing_Data_Import, interval=20)
energy_graph = animation.FuncAnimation(energyGraph, Energy_Data_Import, interval=1000)
TP_graph = animation.FuncAnimation(pressureTemperatureGraph, PT_Data_Import, interval=1000)
plt.show()
main.mainloop()
