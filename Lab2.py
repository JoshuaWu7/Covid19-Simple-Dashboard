#student name: Joshua Wu
#student number: 18468603

#covid simple dashboard app

#imports
from cProfile import label
from covid import Covid
from tkinter import *
import matplotlib
from tkinter import ttk

matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App:
    """ 
        The App is responsible for creating the window and updating the CovidData object with menu and info button selections.
        It also is responsible for running the application interface in the main loop

        Features:
        1. allow user to select among confirmed, active, deaths and recovered, 
           then the app displays the bar graph plot of the top 10 country cases for that metric
        
        2. allow user to select a specific country from a list, 
           then the app displays the numbers of confirmed, active, deaths and recovered cases as tabulated data
    """

    def __init__(self):
        """ 
            App constructor initializes the window, CovidData, Menu Buttons, and Information Buttons
        """
        self.window = Tk()
        self.window.geometry("800x500")
        self.covid_data = self.CovidData(self.window)
        self.menu = self.MenuBttn(self.window)
        self.infoBttns = self.InfoBttns(self.window)

        # Future: implement some frames, pass it into the object's window peram

    # Updates the Covid Data and Plots:
    def update(self):
        """ 
            A call back function for the plot button. Updates the requested country and information item for the covid data object.
            Depending on the requested country and info, plots bar graph or table
        """
        self.covid_data.setRequestedCountry(self.menu.getMenuItem())
        self.covid_data.setRequestedInfo(self.infoBttns.getInfoItem())
        print("DEBUG Update: sent new response")
        print("DEBUG Updated Requested Country: ", self.covid_data.requested_country)
        print("DEBUG Updated Information Item: ", self.covid_data.requested_info)

        #Verify if requested country is: Top Ten
        if self.covid_data.requested_country == 0:
            self.covid_data.plotTopTen()
        else:
            # if requested country is other, update and plot covid table
            self.covid_data.update_covid_table()
            self.covid_data.covid_table.draw_table(self.covid_data.plotted)

    def clear(self):
        """ 
            A call back function for the clear button. Clears both graph and table, whichever is already plotted.
        """
        self.covid_data.clear()
        self.covid_data.covid_table.clear_table()
        

    class CovidData:
        """ 
            CovidData holds all the covid data metrics collected from WorldoMeter.
            It is responsible for plotting covid data, and wraps a Covid Table class.
        """

        def __init__(self, window):
            """ 
                Intializes the CovidData with metrics, confirmed cases, active cases, death cases, and recovered cases.
                Each CovidData object have a plotted boolean that signifies whether it has been plotted or not.
            """
            self.window = window
            self.covid_table = self.CovidTable(self.window)

            self.master_data = self.getMasterCovidData()
            #print("DEBUG: type(masterData) is", type(self.master_data))
            
            self.countries = self.getListOfCountries()
            #print("DEBUG: type(countries) is", type(self.countries))

            self.filtered_out_names = [
                "world",
                "europe",
                "north america",
                "south america",
                "asia",
                "africa",
            ]

            #List of a list of tuples (country/world/continenet, number of cases)
            self.info_list = [
                self.getConfirmed(),
                self.getActive(),
                self.getDeaths(),
                self.getRecovered()
            ]

            #print("DEBUG: ", self.info_list)

            self.sorted_info_list = [
                self.sortByTuple(self.info_list[0]),
                self.sortByTuple(self.info_list[1]),
                self.sortByTuple(self.info_list[2]),
                self.sortByTuple(self.info_list[3])
            ]

            #print("DEBUG: "self.sorted_info_list[0])

            self.filtered_by_country_sorted_info_list = [
                self.filterByCountry(self.sorted_info_list[0], self.filtered_out_names),
                self.filterByCountry(self.sorted_info_list[1], self.filtered_out_names),
                self.filterByCountry(self.sorted_info_list[2], self.filtered_out_names),
                self.filterByCountry(self.sorted_info_list[3], self.filtered_out_names)
            ]
            
            
            #print("DEBUG: "self.filtered_by_country_sorted_info_list[0])

            self.plotted = False

            #default settings: requested_country - Top 10 Countries, requested_info - Confirmed Cases
            self.requested_country = 0 
            self.requested_info = 0

            #dictionary integer to country conversion
            self.countries = {
                0 : "Top 10 Countries" ,      
                1 : "Canada",
                2 : "USA",
                3 : "Russia",
                4 : "UK",
                5 : "Brazil",
                6 : "Australia",
                7 : "India",
                8 : "Iran",
                9 : "Italy",
                10 : "China"
            }

            #dictionary integer to info conversion
            self.info = {
                0 : "Confirmed Cases",      
                1 : "Active Cases",
                2 : "Death Cases",
                3 : "Recovered Cases"
            }
        
        #Called by the app
        def update_covid_table(self):
            """ 
                this function updates confirmed, active, death, and recovered case values on covid table 
                with the given requested country. Requested country cannot be "Top 10 Countries".
            """
            #refer to the country dictionary to convert integer to string
            called_country = self.countries[self.requested_country]

            #represents a singleton list, containing one tuple which has the called country's case value
            country_confirmed = [tup for tup in self.info_list[0] if tup[0] == called_country]
            country_active = [tup for tup in self.info_list[1] if tup[0] == called_country]
            country_death = [tup for tup in self.info_list[2] if tup[0] == called_country]
            country_recovered = [tup for tup in self.info_list[3] if tup[0] == called_country]

            #set info method signature - country: str, confirmed: int, active: int, death: int, recovered: int
            self.covid_table.set_info(called_country, country_confirmed[0][1], country_active[0][1], country_death[0][1], country_recovered[0][1])

        # Called by App during update
        def setRequestedCountry(self, requested_country: int):
            """ 
                This function sets the CovidData object with a requested country mapped by an integer
            """
            print("DEBUG setRequestedCountry: ")
            self.requested_country = requested_country
        
        def setRequestedInfo(self, requested_info: int):
            """ 
                This function sets the CovidData object with a requested info mapped by an integer
            """
            print("DEBUG setRequestedInfo: ", requested_info)
            self.requested_info = requested_info
            print("DEBUG self.requested_info: ", self.requested_info)

        def getMasterCovidData(self) -> list:
            """ this function is called once to get the master data for 
                this application; 
                all data used in this application is derived from data 
                returned by this function
            """
            covid = Covid(source = "worldometers") #instantiate
            data = covid.get_data() # returns a list of dictionaries
            #print(data)
            return data
        
        def getListOfCountries(self) -> list:
            """ 
                this function gets a list of countries from the worldometers source
            """
            covid = Covid(source = "worldometers") #instantiate
            countries = covid.list_countries()
            #print("DEBUG: list of countries: ", countries)
            return countries

        def getConfirmed(self) -> list:
            """ 
                this function uses the this object's masterdata and returns a 
                list of (country, confirmed cases) data
            """
            confirmed = []
            for i in self.master_data:
                confirmed.append((i["country"], i["confirmed"])) #returns a list of tuples
            #print("DEBUG: confirmed is ", confirmed)
            return confirmed
        

        def getActive(self) -> list:
            """ 
                This function uses the masterdata and returns a 
                list of (country, active cases) data
            """
            active = []
            for i in self.master_data:
                active.append((i["country"], i["active"]))
            return active

        def getDeaths(self) -> list:
            """ 
                This function uses the masterdata and returns a 
                list of (country, death cases) data
            """
            deaths = []
            for i in self.master_data:
                deaths.append((i["country"], i["deaths"]))
            return deaths

        def getRecovered(self) -> list:
            """ 
                this function uses the masterdata and returns a 
                list of (country, recovered cases) data
            """
            recovered = []
            for i in self.master_data:
                recovered.append((i["country"], i["recovered"]))
            return recovered
        
        def sortByTuple(self, list_item: list) -> list:
            """ 
                This function sorts a list of items by index one of a list of tuples, in descending order
            """
            new_list = sorted(list_item, key = lambda tup: tup[1], reverse = True)
            return new_list
        
        def filterByCountry(self, list_item: list, filtered_set: list) -> list:
            """ 
                This function filters a list of tuples by index zero, representing a country.
                Countries that are not in the filtered set are filtered in
            """
            filtered_list = [tup for tup in list_item if tup[0].lower() not in filtered_set]
            return filtered_list


        def plotTopTen(self):
            """ 
                A callback function for the button;
                plots a histogram of the top 10 requested info cases 
            """
            global canvas
            if self.plotted or self.covid_table.plotted:
                return
            fig = Figure(figsize = (8, 5))
            plot1= fig.add_subplot(111)
            canvas = FigureCanvasTkAgg(fig, master = self.window) 

            top10 = [self.filtered_by_country_sorted_info_list[self.requested_info][i] for i in range(10)]
            print("DEBUG: top10", top10)
            print("Self.requested_info: ", self.requested_info)
            x = [top10[i][0] for i in range(10)]
            y = [top10[i][1] for i in range(10)]
            plot1.bar(x, y)

            plot1.set_title(label=self.info[self.requested_info], loc = 'center')

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

        class CovidTable:
            """ 
                CovidTable is a table class that wraps a tkk.Treeview() object. 
                It is reponsible for displaying a requested country's case information in a tabulated format
            """
            def __init__(self, window):
                """ 
                    Constructor function for the CovidData class. 
                    Initalizes the country info with empty string and case counts with -1.
                    Creates the general layout for a Treeview object
                """
                self.window = window
                
                #check whether it is plotted or not
                self.plotted = False

                #main info with initialized values
                self.country = ""
                self.confirmed = -1
                self.active = -1
                self.death = -1
                self.recovered = -1

                self.table = ttk.Treeview(self.window)
                
                self.table['columns'] = ('Info', 'Country')

                self.table.column("#0", width=0,  stretch=NO)
                self.table.column("Info",anchor=CENTER, width=80)
                self.table.column("Country",anchor=CENTER,width=80)
                
                self.table.heading("0",text="",anchor=CENTER)
                self.table.heading("Info",text="Info",anchor=CENTER)
                
            
            #called by CovidData
            def set_info(self, country: str, confirmed: int, active: int, death: int, recovered: int):
                """ 
                    A function for setting the updated requested country info and case metrics to be tabulated
                """
                self.country = country
                self.confirmed = confirmed
                self.active = active
                self.death = death
                self.recovered = recovered

            def draw_table(self, graphIsPlotted: bool):
                """ 
                    A drawing function responsible for drawing the Treeview table.
                    It updates the table heading with country and inserts rows with confirmed, active, death and recovered metrics
                """

                if self.plotted or graphIsPlotted is True:
                    return 

                self.table.heading("Country",text= self.country, anchor=CENTER)
                self.table.insert(parent='',index='end',iid=0,text='',
                values=('Confirmed', self.confirmed))
                self.table.insert(parent='',index='end',iid=1,text='',
                values=('Active', self.active))
                self.table.insert(parent='',index='end',iid=2,text='',
                values=('Death', self.death))
                self.table.insert(parent='',index='end',iid=3,text='',
                values=('Recovered', self.recovered))
                
                self.table.pack()
                self.plotted = True

            def clear_table(self):
                """ 
                    A clearing function responsible for clearing the rows of a table.
                """
                if self.plotted is True:

                    r = self.table.get_children()
                    for item in r:
                        self.table.delete(item)

                    self.table.pack_forget()
                    print("DEBUG Clear: You cleared the table!")
                    self.plotted = False


    class InfoBttns():
        """ 
            A information button class that wraps radio button metrics
        """
        def __init__(self, window):
            """ 
                Initializes the radio buttons for confirmed cases, active cases, death cases, and recovered cases
            """
            self.title = Label(window, text = "Information")
            
            # integer variable for radio button value pressed
            self.info = IntVar()
            
            self.confirmed_cases = Radiobutton(window, text = "Confirmed Cases", variable= self.info, value = 0, command= lambda: print("Selected Confirmed Cases: 0"))
            self.active_cases = Radiobutton(window, text = "Active Cases", variable= self.info, value = 1, command= lambda: print("Selected Active Cases: 1"))
            self.death_cases = Radiobutton(window, text = "Death Cases", variable= self.info, value = 2, command= lambda: print("Selected Death Cases: 2"))
            self.recovered_cases = Radiobutton(window, text = "Recovered Cases", variable= self.info, value = 3, command= lambda: print("Selected Recovered Cases: 3"))
        
        
        def getInfoItem(self) -> int:
            """ 
                A gettor function for accessing which radio button was pressed
            """
            print("DEBUG InfoBttns::getInfoItem(): ", self.info.get())
            return self.info.get()

        #Future: draw more prettier
        def drawInfoBttns(self):
            """ 
                Plotting function for drawing the radio buttons onto the screen
            """
            self.title.pack()
            self.confirmed_cases.pack()
            self.active_cases.pack()
            self.death_cases.pack()
            self.recovered_cases.pack()

    class MenuBttn():
        """ 
            Menu Button class represents a menu that lists ten countries and the top 10 countries label
        """
        def __init__(self, window):
            """ 
                Initializes the menu button with the label and menu pull down
            """
            self.menu_button = Menubutton(window, text = "~Country Menu~")
            self.menu = Menu(self.menu_button, tearoff = 0)
            self.menu_button["menu"] = self.menu

            # integer variabel for storing which menu button was pressed
            self.menu_item = IntVar()

            self.menu.add_radiobutton(label = "Top 10 Countries", variable= self.menu_item, value = 0, command= lambda: print("Selected Top 10 Countries: ", self.menu_item.get()))
            self.menu.add_radiobutton(label = "Canada", variable= self.menu_item, value = 1, command= lambda: print("Selected Canada: ", self.menu_item.get()))
            self.menu.add_radiobutton(label = "United States", variable= self.menu_item, value = 2, command= lambda: print("Selected USA: ", self.menu_item.get()))
            self.menu.add_radiobutton(label = "Russia", variable= self.menu_item, value = 3, command= lambda: print("Selected Russia: ", self.menu_item.get()))
            self.menu.add_radiobutton(label = "England", variable= self.menu_item, value = 4, command= lambda: print("Selected England: ", self.menu_item.get()))
            self.menu.add_radiobutton(label = "Brazil", variable= self.menu_item, value = 5, command= lambda: print("Selected Brazil: ", self.menu_item.get()))
            self.menu.add_radiobutton(label = "Australia", variable= self.menu_item, value = 6, command= lambda: print("Selected Australia: ", self.menu_item.get()))
            self.menu.add_radiobutton(label = "India", variable= self.menu_item, value = 7, command= lambda: print("Selected India: ", self.menu_item.get()))
            self.menu.add_radiobutton(label = "Iran", variable= self.menu_item, value = 8, command= lambda: print("Selected Iran: ", self.menu_item.get()))
            self.menu.add_radiobutton(label = "Italy", variable= self.menu_item, value = 9, command= lambda: print("Selected Italy: ", self.menu_item.get()))
            self.menu.add_radiobutton(label = "China", variable= self.menu_item, value = 10, command= lambda: print("Selected China: ", self.menu_item.get()))
        
        def getMenuItem(self) -> int:
            """ 
                A gettor function for retrieving which which menu button was pressed.
                Returns and integer mapped to a name.
            """
            return self.menu_item.get()

        #Future: draw prettier
        def drawMenuBttn(self):
            """ 
                A plotting function for drawing the menu
            """
            self.menu_button.pack()
    
    
    def run(self):
        """ 
            An app class function responsible for running the main super loop of the app.
            Reponsible for drawing out the menu button, info buttons, plotting button, and clear button.
            Also reponsible for updating and clearing the screen when called back.
        """

        self.window.title("Covid Data Visualization")

        self.covid_data.plotted = False

        self.menu.drawMenuBttn()
        self.infoBttns.drawInfoBttns()

        # When pressed, calls back app's update function
        self.plot_button = Button(master = self.window,
                        command = lambda: self.update(),
                        height = 2,
                        width = 20,
                        text = "Plot").pack()

        # When pressed, calls back the app's clear function
        self.clear_button = Button(master = self.window,
                        command = lambda: self.clear(),
                        height = 2,
                        width = 20,
                        text = "Clear").pack()

        #print("DEBUG Info Item", self.infoBttns.getInfoItem())
        #print("DEBUG reached after update")

        self.window.mainloop()
    
    
if __name__ == "__main__":
    # The main function for creating the app and running it
    app = App()
    app.run()
