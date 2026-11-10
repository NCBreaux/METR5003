#Import stuff
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

#Define functions from the lab instructions
def Skew(temp, pres):
    skew = -30
    return (temp) + skew * np.log(pres/1000)

#For below functions: temp must be in Kelvin
def dry_lapse(temp, pres):
    return (Rd*temp)/(pres*cp)

def sat_vap_pres(temp):
    c = 6.112 #hPa
    return c*np.exp(17.67*(temp-273.15)/(temp-29.65))

def rs(temp, pres):
    e_s = sat_vap_pres(temp)
    return epsilon*(e_s/(pres-e_s))

def moist_lapse(temp, pres):
    r_s = rs(temp, pres)
    numer = 1 + ((Lv*r_s)/(Rd*temp))
    denom = 1 + (((Lv**2) * r_s)/(cp*Rv*(temp**2)))
    dT_dz = -(g/cp)*numer/denom
    dT_dp = dT_dz * (Rd*temp)/(-pres*g)
    return dT_dp

#Set constants and limits from lab instructions
plines = np.arange(100, 1000, 100)
Tlines = np.arange(-100, 100, 10)
pmin, pmax = 100, 1000
Tmin, Tmax = -40, 100
epsilon = 0.622
g = 9.8 #m/s^2
cp = 1004 #J/kgK
Rd = 287 #J/kgK
Rv = 461 #J/kgK
Lv = 2.5e6 #J/kg

#Get temps in K and flip the order of pressure for adiabat calculations
K_T = Tlines + 273.15
moist_extra = np.arange(5,55,10) + 273.15
pres = np.arange(100,1001,1)
hPa_p = np.flip(pres)

def plot_skewt(sounding_t, sounding_td, sounding_p, lines):

    #Plot the skew T
    fig, ax = plt.subplots()
    label = 1

    #Plot pressure and temperature lines, formatting to lab specifications
    #The label thing is so only one line gets the label for the legend, or else the legend wouldn't work as I have it
    for p in plines:
        if label == 1:
            ax.hlines(p, xmin=Tmin, xmax=Tmax, color='gray', linewidths=.5, label = 'Isobars')
            label = 0
        else:
            ax.hlines(p, xmin=Tmin, xmax=Tmax, color='gray', linewidths=.5)
    for T in Tlines:
        if label == 0:
            ax.plot(Skew(T, pres), np.arange(100, 1001,1), color='orange', linestyle='--', linewidth=.5, label = 'Isotherms')
            label = 1
        else:
            ax.plot(Skew(T, pres), np.arange(100, 1001,1), color='orange', linestyle='--', linewidth=.5)
    ax.set_yscale('log') #This makes the y-axis (pressure) logarithmic
    ax.set_ylim(pmax, pmin) #This sets the limits of the pressure axis provided in the lab
    ax.set_xlim(Tmin, Tmax)  #This sets the limits of the temperature axis provided in the lab

    #Plot the dry adiabats 
    #Same thing with the label thing, only one line gets the label for the legend
    for temp in K_T:
        temps = [temp-273.15]
        t = temp
        for p in hPa_p[1:]:
            t = t - dry_lapse(t, p)
            temps.append(t-273.15)
        if label == 1:
            ax.plot(Skew(temps, hPa_p), hPa_p, color='brown', linewidth=.5, label = 'Dry adiabat')
            label = 0
        else:
            ax.plot(Skew(temps, hPa_p), hPa_p, color='brown', linewidth=.5)

    #Plot the moist adiabats 
    for temp in np.concatenate((K_T, moist_extra)):
        temps = [temp-273.15]
        t = temp
        for p in hPa_p[1:]:
            t = t - moist_lapse(t, p)
            temps.append(t-273.15)
        if label == 0:
            ax.plot(Skew(temps, hPa_p), hPa_p, color='blue', linewidth=.5, label = 'Moist adiabat')
            label = 1
        else:
            ax.plot(Skew(temps, hPa_p), hPa_p, color='blue', linewidth=.5)

    #Plot observed sounding lines
    for i in range(lines):
        t_in = sounding_t[i]
        td_in = sounding_td[i]
        p_in = sounding_p[i]
        ax.plot(Skew(t_in, p_in), p_in, color='red', label = 'Temperature Profile')
        #ax.plot(Skew(td_in, p_in), p_in, color='green', label = 'Dew Point Profile')

    #Add a title, labels, and a legend
    #ax.set_title('Norman, OK May 13, 2026 00z Sounding')
    ax.set_xlabel('Temperature (C)')
    ax.set_ylabel('Pressure (hPa)')
    ax.legend(loc='upper right')

    #Make the y-axis not show scientific notation (Thank you ChatGPT)
    ax.yaxis.set_major_locator(ticker.LogLocator(base=10, subs=(1, 2, 3, 4, 5, 6, 7, 8, 9)))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x:.0f}"))