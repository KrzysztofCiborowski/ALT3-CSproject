import json
import sys
import tkinter.messagebox
import customtkinter
from tkinter import Menu
import tkinter
import initialRates
import initialSates
import newSimDialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import filedialog
import sliderDialog
import test2

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class CustomToolbar(NavigationToolbar2Tk):
    toolitems = [t for t in NavigationToolbar2Tk.toolitems if t[0] != 'Save']

    def __init__(self, canvas, window):
        NavigationToolbar2Tk.__init__(self, canvas, window)

    def _init_toolbar(self):
        self.wanttoolbar = True
        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.add_separator()
            else:
                self.add_toolitem(text, tooltip_text, image_file, callback, orientation="horizontal")


def viewDocumentation():
    import webbrowser
    webbrowser.open("README.md")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.toolbar = None
        self.toolbarFrame = None
        self.canvas = None
        self.ax = None
        self.fig = None
        self.labels = None
        self.social_distancing = None
        self.theta = None
        self.fileDir_Graph = None
        self.fileDir = None
        self.results = None
        self.t = None
        self.psi = None
        self.delta = None
        self.rho = None
        self.sigma = None
        self.gamma = None
        self.beta = None
        self.initial_states = None
        self.cityName = None
        self.pltAvail = None
        self.N = None
        self.Infected = None
        self.Recovered = None
        self.Exposed = None
        self.Asymptomatic = None
        self.Symptomatic = None
        self.Deceased = None
        self.Hospitalized = None
        self.saved = False

        self.title("Pandemic Outbreak Simulator")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._create_widgets()
        self.config(menu=self.menubar)

    def _on_closing(self):
        choice = tkinter.messagebox.askyesno("Are you sure", "Are you sure you want to quit")
        if choice:
            self.quit()

    def _create_widgets(self):
        """Menu Bar"""
        self.menubar = Menu(self, bg="black", fg="white", font=("Helvetica", 12))
        file = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file)
        file.add_command(label="New Simulation", command=self.newSimulation)
        file.add_separator()
        file.add_command(label="Open", command=self.open)
        file.add_command(label="Save As", command=self.saveAs)
        file.add_separator()
        file.add_command(label='Exit', command=self._on_closing)
        edit = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=edit)
        init_state = Menu(edit, tearoff=0)
        edit.add_cascade(label="Initial State", menu=init_state)
        edit.add_separator()
        init_rate = Menu(edit, tearoff=0)
        edit.add_cascade(label="Initial Rates", menu=init_rate)

        """Dialog 2"""
        attributesState = [
            ("Population", self.changeAttributeState, ("N", 10000, 25000000)),
            ("Initial Infected", self.changeAttributeState, ("Infected", 1, 1000)),
            ("Initial Recovered", self.changeAttributeState, ("Recovered", 1, 1000)),
            ("Initial Exposed", self.changeAttributeState, ("Exposed", 1, 1000)),
            ("Initial Asymptomatic", self.changeAttributeState, ("Asymptomatic", 1, 1000)),
            ("Initial Symptomatic", self.changeAttributeState, ("Symptomatic", 1, 1000)),
            ("Initial Hospitalized", self.changeAttributeState, ("Hospitalized", 1, 1000)),
            ("Initial Deceased", self.changeAttributeState, ("Deceased", 1, 1000))
        ]

        attributesRate = [
            ("Transmission Rate", self.changeAttributeState, ("beta", 0, 100)),
            ("Recovery Rate", self.changeAttributeState, ("gamma", 0, 100)),
            ("Progression Rate", self.changeAttributeState, ("sigma", 0, 100)),
            ("Hospitalization Rate", self.changeAttributeState, ("rho", 0, 100)),
            ("Death Rate", self.changeAttributeState, ("delta", 0, 100)),
            ("External Infection Rate", self.changeAttributeState, ("psi", 0, 100)),
            ("Intervention Rate", self.changeAttributeState, ("theta", 0, 100))
        ]

        for label, command, args in attributesState:
            init_state.add_command(
                label=f"Change {label}",
                command=lambda a=args: self.changeAttributeState(a[0], a[1], a[2]) if getattr(self, a[
                    0]) is not None else tkinter.messagebox.showerror("Error 3",
                                                                      "Current value is None or no simulation is "
                                                                      "running")
            )

        for label, command, args in attributesRate:
            init_rate.add_command(
                label=f"Change {label}",
                command=lambda a=args: self.changeAttributeRate(a[0], a[1], a[2]) if getattr(self, a[
                    0]) is not None else tkinter.messagebox.showerror("Error 3",
                                                                      "Current value is None or no simulation is "
                                                                      "running")
            )
        """Rest of Menu Bar"""
        window = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Window", menu=window)
        window.add_command(label="Change Appearance", command=self.changeAppearence)

        helpMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Help', menu=helpMenu)
        helpMenu.add_command(label="View Documentation", command=viewDocumentation)

    def changeAttributeState(self, attr, slider_min, slider_max):
        """Change of attributes of the simulation (initial state)"""
        value = sliderDialog.CTkSliderDialog(title=f"Change {attr}", text=f"Initial {attr}",
                                             sliderMin=slider_min, sliderMax=slider_max,
                                             curr_val=getattr(self, attr)).get_input()
        setattr(self, attr, value)
        self.saved = False
        self.run()

    def changeAttributeRate(self, attr, slider_min, slider_max):
        """Change of attributes of the simulation (initial rates)"""
        value = sliderDialog.CTkSliderDialog(title=f"Change {attr}", text=f"Initial {attr}",
                                             sliderMin=slider_min, sliderMax=slider_max,
                                             curr_val=getattr(self, attr), multiplier=100).get_input()
        setattr(self, attr, value)
        if attr == "delta":
            self.delta /= 1000
            print("yes")
        self.saved = False
        self.run()

    def changeAppearence(self):
        a = customtkinter.get_appearance_mode()
        print(a)
        if customtkinter.get_appearance_mode() == "Dark":
            customtkinter.set_appearance_mode("Light")
            self.update_menu_bar_appearance("Light")
        else:
            customtkinter.set_appearance_mode("Dark")
            self.update_menu_bar_appearance("Dark")

    def update_menu_bar_appearance(self, mode: str):
        if mode == "Dark":
            self.menubar.configure(bg="gray25", fg="white", activeforeground="white", activebackground="gray30")
        elif mode == "Light":
            self.menubar.configure(bg="gray95", fg="black", activeforeground="black", activebackground="gray85")

    def open(self):
        self.fileDir = filedialog.askopenfilename(defaultextension=".ps",
                                                  filetypes=[
                                                      ("PandemicSimulator File", ".ps")
                                                  ])

        with open(self.fileDir, "r") as f:
            json_data = json.load(f)

        for key, value in json_data.items():
            setattr(self, key, value)
        self.saved = True
        self.run()

    def saveAs(self):
        if self.pltAvail is None:
            tkinter.messagebox.showerror(title="Error 1", message="Error, no simulation created")
        else:
            self.fileDir_Graph = filedialog.asksaveasfilename(defaultextension=".ps",
                                                              filetypes=[
                                                                  ("PandemicSimulator File", ".ps"),
                                                                  ("PNG Image", ".png"),
                                                                  ("PDF File", ".pdf"),
                                                                  ("JPG Image", ".jpg"),
                                                                  ("All Files", "*.*")
                                                              ])

            if self.fileDir_Graph:
                self.saved = True
                test2.savePlot(filename=self.fileDir_Graph, N=self.N, exposed=self.Exposed,
                               asymptomatic=self.Asymptomatic, symptomatic=self.Symptomatic,
                               hospitalized=self.Hospitalized, infected=self.Infected, recovered=self.Recovered,
                               deceased=self.Deceased, beta=self.beta, gamma=self.gamma, sigma=self.sigma, rho=self.rho,
                               delta=self.delta, psi=self.psi, theta=self.theta,
                               social_distancing=self.social_distancing, cityName=self.cityName)
            else:
                tkinter.messagebox.showerror(title="Error", message="No file selected to save as")

    def newSimulation(self):
        self.cityName, self.N = newSimDialog.NewSimulation(title="New Simulation").get_input()

        states_dialog = initialSates.R0I0()
        states_values = states_dialog.get_input()

        self.Infected = float(states_values["Initial Infected"])
        self.Exposed = float(states_values["Initial Exposed"])
        self.Recovered = float(states_values["Initial Recovered"])
        self.Asymptomatic = float(states_values["Initial Asymptomatic"])
        self.Symptomatic = float(states_values["Initial Symptomatic"])
        self.Hospitalized = float(states_values["Initial Hospitalized"])
        self.Deceased = float(states_values["Initial Deceased"])

        rates_dialog = initialRates.Rates()
        rate_values = rates_dialog.get_input()

        self.beta = float(rate_values["Transmission Rate"])
        self.gamma = float(rate_values["Recovery Rate"])
        self.sigma = float(rate_values["Progression Rate"])
        self.rho = float(rate_values["Hospitalization Rate"])
        self.delta = float(rate_values["Mortality Rate"])
        self.psi = float(rate_values["External Introduction Rate"])
        self.theta = float(rate_values["Intervention Rate"])
        self.social_distancing = 1.0

        print(self.gamma, self.sigma, self.rho, self.delta, self.psi, self.theta, self.social_distancing)
        self.run()

    def run(self):
        self.initial_states = (self.N - (
                self.Exposed + self.Asymptomatic + self.Symptomatic + self.Hospitalized + self.Infected +
                self.Recovered + self.Deceased),
                               self.Exposed, self.Asymptomatic, self.Symptomatic, self.Hospitalized,
                               self.Infected, self.Recovered, self.Deceased)

        model = test2.PandemicModel(self.N, self.initial_states, self.beta, self.gamma, self.sigma, self.rho,
                                    self.delta, self.psi, self.theta, self.social_distancing)
        self.t, self.results = model.run_simulation(days=160)

        self.saved = False
        self.plot()


    def plot(self):
        self.labels = ['Susceptible', 'Exposed', 'Asymptomatic', 'Symptomatic', 'Hospitalized', 'Infected', 'Recovered',
                       'Deceased']
        self.fig, self.ax = test2.PandemicPlotter(self.N).plot(self.t, self.results, self.labels, self.cityName)

        self.frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.toolbarFrame = customtkinter.CTkFrame(self)
        self.toolbarFrame.grid(row=1, column=0, sticky="ew")
        self.toolbar = CustomToolbar(self.canvas, self.toolbarFrame)
        self.toolbar.update()
        self.toolbar.pack(side=tkinter.TOP, fill=tkinter.X)

        self.pltAvail = self.fig


if __name__ == "__main__":
    app = App()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        tkinter.messagebox.showerror(title="Error", message="Program terminated forcefully")
    finally:
        sys.exit(0)

