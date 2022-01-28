#student name: Joshua Wu
#student number: 18468603

#covid simple dashboard app

#imports
from covid import Covid

from tkinter import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def getMasterCovidData() -> list:
    """ this function is called once to get the master data for 
        this application; 
        all data used in this application is derived from data 
        returned by this function
    """
    covid = Covid() #instantiate
    data = covid.get_data() # returns a list of dictionaries
    return data

def getConfirmed(data1: list) -> list:
    """ this function uses the masterdata data1 and returns a 
        list of (country, confirmed) data
    """
    confirmed = []
    for i in data1:
        confirmed.append((i["country"], i["confirmed"])) #returns a list of tuples
    #print("DEBUG: confirmed is ", confirmed)
    return confirmed

def plotConfirmed():
    """ a callback function for the button;
        plots a histogram of the top 10 confirmed cases 
    """
    global plotted, canvas
    if plotted:
        return
    fig = Figure(figsize = (8, 5))
    plot1= fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master = window) 

    top10 = [confirmed[i] for i in range(10)]
    #print("DEBUG: top10", top10)
    x = [top10[i][0] for i in range(10)]
    y = [top10[i][1] for i in range(10)]
    plot1.bar(x, y)

    for tick in plot1.get_xticklabels(): #rotate the text slightly
        tick.set_rotation(15) 
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    plotted = True

def clear():
    """ a callback for the Clear button """ 
    global plotted, canvas
    if plotted:
        canvas.get_tk_widget().destroy()
        plotted = False

#### program starts here
#get masterData
masterData = getMasterCovidData()
print("DEBUG: type(masterData) is", type(masterData))
confirmed = getConfirmed(masterData)
print("DEBUG: type(confirmed) is", type(confirmed))

#instantiate the main window
window = Tk()
window.geometry("800x500")

window.title("Covid Data Visualization")

plotted = False

plot_button = Button(master = window,
                command = lambda: plotConfirmed(),
                height = 2,
                width = 20,
                text = "Plot: top 10 confirmed").pack()

clear_button = Button(master = window,
                command = lambda: clear(),
                height = 2,
                width = 10,
                text = "Clear").pack()

window.mainloop()