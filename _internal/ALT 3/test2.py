import datetime
import json
import tkinter.messagebox

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


def savePlot(filename, N, exposed, asymptomatic, symptomatic, hospitalized, infected, recovered, deceased, beta, gamma,
             sigma, rho, delta, psi, theta, social_distancing, cityName):
    if ".png" in filename:
        format = "png"
    elif ".pdf" in filename:
        format = "pdf"
    elif ".ps" in filename:
        format = "ps"
        dic = {
            "N": N,
            "Exposed": exposed,
            "Asymptomatic": asymptomatic,
            "Symptomatic": symptomatic,
            "Hospitalized": hospitalized,
            "Infected": infected,
            "Recovered": recovered,
            "Deceased": deceased,
            "Date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "beta": beta,
            "gamma": gamma,
            "sigma": sigma,
            "rho": rho,
            "delta": delta,
            "psi": psi,
            "theta": theta,
            "social_distancing": social_distancing,
            "cityName": cityName
        }

        json_data = json.dumps(dic, indent=4)
        with open(filename, "w") as outfile:
            outfile.write(json_data)

    else:
        format = "jpg"
    if format != "ps":
        plt.savefig(filename, bbox_inches='tight', format=format), plt.close()

    tkinter.messagebox.showinfo("File Saved Succesfully", f"File saved as {filename}")


class PandemicModel:
    def __init__(self, N, initial_states, beta, gamma, sigma, rho, delta, psi, theta, social_distancing):
        self.N = N
        self.S, self.E, self.A, self.Sy, self.H, self.I, self.R, self.D = initial_states
        self.beta = beta
        self.gamma = gamma
        self.sigma = sigma
        self.rho = rho
        self.delta = delta
        self.psi = psi
        self.theta = theta
        self.social_distancing = social_distancing

    def deriv(self, y, t):
        S, E, A, Sy, H, I, R, D = y
        dSdt = -self.beta * self.social_distancing * S * (I + A + Sy) / self.N
        dEdt = self.beta * self.social_distancing * S * (I + A + Sy) / self.N - self.sigma * E
        dAdt = self.sigma * E * (1 - self.rho) - self.gamma * A
        dSydt = self.sigma * E * self.rho - self.theta * Sy - self.gamma * Sy
        dHdt = self.theta * Sy - self.psi * H - self.gamma * H
        dIdt = self.gamma * (A + Sy + H)
        dRdt = self.gamma * (A + Sy + H)
        dDdt = self.delta * Sy + self.psi * H
        return dSdt, dEdt, dAdt, dSydt, dHdt, dIdt, dRdt, dDdt

    def run_simulation(self, days):
        y0 = self.S, self.E, self.A, self.Sy, self.H, self.I, self.R, self.D
        t = np.linspace(0, days, days)
        ret = odeint(self.deriv, y0, t)
        return t, ret.T


class PandemicPlotter:
    def __init__(self, N):
        self.N = N

    def plot(self, t, data, labels, city_name):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        fig = plt.figure(facecolor='w')
        ax = fig.add_subplot(111, axisbelow=True)
        for dat, label in zip(data, labels):
            ax.plot(t, dat, alpha=1, lw=2, label=label)

        ax.set_xlabel('Time /days')
        ax.set_ylabel('Number of people')
        ax.set_ylim(0, np.max([np.max(dat) for dat in data]))
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(True, which='major', linestyle='-', linewidth=2, color='white')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        if city_name is None or city_name == "City Name:":
            city_name = "Example City"
        title_text = f"{city_name} Pandemic Spread as of {current_date}"
        ax.set_title(title_text)
        #plt.show()
        return fig, ax


if __name__ == '__main__':
    N = 1000000
    initial_states = (N - 10, 10, 0, 0, 0, 0, 0, 0)
    beta, gamma, sigma, rho, delta, psi, theta, social_distancing = 0.5, 1. / 20, 1. / 5, 0.2, 0.01, 0.01, 0.05, 1.0

    model = PandemicModel(N, initial_states, beta, gamma, sigma, rho, delta, psi, theta, social_distancing)
    t, results = model.run_simulation(days=160)

    plotter = PandemicPlotter(N)
    labels = ['Susceptible', 'Exposed', 'Asymptomatic', 'Symptomatic', 'Hospitalized', 'Infected', 'Recovered',
              'Deceased']
    plotter.plot(t, results, labels, "City")
