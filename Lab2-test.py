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

class App:

    def __init__(self):
        self.window = Tk()
        self.window.geometry("800x500")
        self.covid_data = self.CovidData(self.window)
        self.menu = self.MenuBttn(self.window)
        #self.infoBttns = self.InfoBttns(self.window)

        #need to implement some frames, pass it into the object's window


    class CovidData:

        def __init__(self, window):
            self.window = window
            self.masterData = self.getMasterCovidData()
            print("DEBUG: type(masterData) is", type(self.masterData))

            #initialize info buttons
            self.infoBttns = self.InfoBttns(self.window)

            #List of tuples (country, number of cases)
            self.info_list = [
                self.getConfirmed(self.masterData),
                self.getActive(self.masterData),
                self.getDeaths(self.masterData),
                self.getRecovered(self.masterData)
            ]
            '''
            self.confirmed = self.getConfirmed(self.masterData)
            print("DEBUG: type(confirmed) is", type(self.confirmed))
            self.active = self.getActive(self.masterData)
            self.death = self.getDeaths(self.masterData)
            self.recovered = self.getRecovered(self.masterData)
            '''

            self.plotted = False

            #default settings (these statements are only called once, we want to call self.infoBttns.getInfoBttns() every time button get pressed)
            #self.requested_country = self.countries["Top_10_Countries"] ////note: we are using zero for top 10 country
            self.requested_country = 0 
            #self.requested_info = self.info["Confirmed_Cases"] ////note: we are using zero for confirmed cases by default
            self.requested_info = 0

            #dictionary for country
            self.countries = {
                "Top_10_Countries" : 0,      
                "Canada" : 1,
                "United_States" : 2,
                "Russia" : 3,
                "England" : 4,
                "Brazil" : 5,
                "Australia" : 6,
                "India" : 7,
                "Iran" : 8,
                "Italy" : 9,
                "New_Zealand" : 10
            }

            #dictionary for info
            self.info = {
                "Confirmed_Cases" : 0,
                "Active_Cases" : 1,
                "Death" : 2,
                "Recoverd_Cases" : 3
            }
        
        # To be set after a new button or menu is pressed (called by app)
        def setRequestedCountry(self, requested_country: int):
            self.requested_country = requested_country
        
        def setRequestedInfo(self, requested_info: int):
            self.requested_info = requested_info

        def getMasterCovidData(self) -> list:
            """ this function is called once to get the master data for 
                this application; 
                all data used in this application is derived from data 
                returned by this function
            """
            covid = Covid() #instantiate
            data = covid.get_data() # returns a list of dictionaries
            return data

        def getConfirmed(self, data1: list) -> list:
            """ this function uses the masterdata data1 and returns a 
                list of (country, confirmed) data
            """
            confirmed = []
            for i in data1:
                confirmed.append((i["country"], i["confirmed"])) #returns a list of tuples
            #print("DEBUG: confirmed is ", confirmed)
            return confirmed
        

        def getActive(self, master_data: list) -> list:
            active = []
            for i in master_data:
                active.append((i["country"], i["active"]))
            return active

        def getDeaths(self, master_data: list) -> list:
            deaths = []
            for i in master_data:
                deaths.append((i["country"], i["deaths"]))
            return deaths

        def getRecovered(self, master_data: list) -> list:
            recovered = []
            for i in master_data:
                recovered.append((i["country"], i["recovered"]))
            return recovered
                

        def plotConfirmed(self):
            """ a callback function for the button;
                plots a histogram of the top 10 confirmed cases 
            """
            global canvas
            if self.plotted:
                return
            fig = Figure(figsize = (8, 5))
            plot1= fig.add_subplot(111)
            canvas = FigureCanvasTkAgg(fig, master = self.window) 

            #WIP area
            top10 = [self.info_list[self.requested_info][i] for i in range(10)]
            print("DEBUG: top10", top10)
            print("Self.requested_info: ", self.requested_info)
            x = [top10[i][0] for i in range(10)]
            y = [top10[i][1] for i in range(10)]
            plot1.bar(x, y)

            for tick in plot1.get_xticklabels(): #rotate the text slightly
                tick.set_rotation(15) 
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True)
            self.plotted = True

        def clear(self):
            """ a callback for the Clear button """ 
            global canvas
            if self.plotted:
                canvas.get_tk_widget().destroy()
                self.plotted = False
        
        class InfoBttns:

            def __init__(self, window):
                self.title = Label(window, text = "Information")
                
                self.info = IntVar()
                
                self.confirmed_cases = Radiobutton(window, text = "Confirmed Cases", variable= self.info, value = 0, command= lambda: print(self.info.get()))
                self.active_cases = Radiobutton(window, text = "Active Cases", variable= self.info, value = 1, command= lambda: print(self.info.get()))
                self.death_cases = Radiobutton(window, text = "Death", variable= self.info, value = 2, command= lambda: print(self.info.get()))
                self.recovered_cases = Radiobutton(window, text = "Recovered Cases", variable= self.info, value = 3, command= lambda: print(self.info.get()))
            
            # this function accesses self.info
            def getInfoItem(self) -> int:
                print("DEBUG getInfoItem(): ", self.info.get())
                return self.info.get()

            #need to make drawing more prettier
            def drawInfoBttns(self):
                self.title.pack()
                self.confirmed_cases.pack()
                self.active_cases.pack()
                self.death_cases.pack()
                self.recovered_cases.pack()

    class MenuBttn:
        def __init__(self, window):
            self.menu_button = Menubutton(window, text = "Country")
            self.menu = Menu(self.menu_button, tearoff = 0)
            self.menu_button["menu"] = self.menu

            self.menu_item = IntVar()

            self.menu.add_radiobutton(label = "Top 10 Countries", variable= self.menu_item, value = 0, command= lambda: print(self.menu_item.get()))
            self.menu.add_radiobutton(label = "Canada", variable= self.menu_item, value = 1, command= lambda: print(self.menu_item.get()))
            self.menu.add_radiobutton(label = "United States", variable= self.menu_item, value = 2, command= lambda: print(self.menu_item.get()))
            self.menu.add_radiobutton(label = "Russia", variable= self.menu_item, value = 3, command= lambda: print(self.menu_item.get()))
            self.menu.add_radiobutton(label = "England", variable= self.menu_item, value = 4, command= lambda: print(self.menu_item.get()))
            self.menu.add_radiobutton(label = "Brazil", variable= self.menu_item, value = 5, command= lambda: print(self.menu_item.get()))
            self.menu.add_radiobutton(label = "Australia", variable= self.menu_item, value = 6, command= lambda: print(self.menu_item.get()))
            self.menu.add_radiobutton(label = "India", variable= self.menu_item, value = 7, command= lambda: print(self.menu_item.get()))
            self.menu.add_radiobutton(label = "Iran", variable= self.menu_item, value = 8, command= lambda: print(self.menu_item.get()))
            self.menu.add_radiobutton(label = "Italy", variable= self.menu_item, value = 9, command= lambda: print(self.menu_item.get()))
            self.menu.add_radiobutton(label = "New Zealand", variable= self.menu_item, value = 10, command= lambda: print(self.menu_item.get()))
        
        def getMenuItem(self) -> int:
            return self.menu_item.get()

        def drawMenuBttn(self):
            self.menu_button.pack()
        
        
    class PlotButton:

        def __init__(self, window):
            self.window = window
            self.menu_item = 0
            self.info_item = 0
            self.plot_button = Button(master = self.window, height = 2, width = 20, text = "Plot")


        #the app will call gettors for menu item and info item then pass as parameters
        def update(self, menu_item, info_item):
            self.menu_item = menu_item
            self.info_item = info_item

            

        def drawPlotButton(self, window):
            pass

    class ClearButton:
        pass
    
    
    
    def run(self):

        self.window.title("Covid Data Visualization")

        self.covid_data.plotted = False

        self.plot_button = Button(master = self.window,
                        command = lambda: self.covid_data.plotConfirmed(),
                        height = 2,
                        width = 20,
                        text = "Plot: top 10").pack()

        self.clear_button = Button(master = self.window,
                        command = lambda: self.covid_data.clear(),
                        height = 2,
                        width = 10,
                        text = "Clear").pack()

        self.menu.drawMenuBttn()

        #WIP area
        self.covid_data.infoBttns.drawInfoBttns()

        #communicates the update results to the covid data
        #print(self.menu.getMenuItem())


        #WIP area: info buttons now part of covid data
        #print("DEBUG Info Item", self.infoBttns.getInfoItem())
        self.covid_data.setRequestedCountry(self.menu.getMenuItem())
        #self.covid_data.setRequestedInfo(self.infoBttns.getInfoItem())

        self.window.mainloop()
    
    
if __name__ == "__main__":
    app = App()
    app.run()
