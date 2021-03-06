# A very simple and basic model for local CO2 concentration

import numpy as np
import matplotlib.pyplot as plt
import solar as sol


# Photosynthesis rate at intensity, Michaelis-Menden-like
def pi_curve(intensity, p_max=10, ki=1/2):
    # p_max     maximal photosynthesis rate
    # ki        half-saturation intensity
    return p_max * intensity / (ki + intensity)


# Computes solar intensity
def solar_intensity(Day=20, Month=5, Year=2018, hour=0, TZ=2, lat=47, long=10, elev=3000):
    incident_angle = sol.SPA(Day, Month, Year, hour, TZ, lat, long, elev)
    if incident_angle <= 90:
        return abs(incident_angle - 90) / 90
    else:
        return 0


# The model

def evolve(init_concentration, init_time=0, init_date=(6,6,2018), duration=24, stepsize=0.1, Absorption=0, Emission=0):
    # EVOLVE : evolves an initial concentration in time.
    # init_concentration: initial concentration at init_time at the measurement site
    # init_time: Time in hours on the clock when evolving starts (0 means 0:00 in the morning)
    # init_date: Initial date in format (Day,month,year)
    # duration: Denotes the time in hours how long the system will be evolved
    # stepsize: Stepsize for the integration method
    # Absorption: Absorption model ID
    # Emission: Emission model ID

    C = [init_concentration]
    time = np.arange(init_time, init_time + duration, stepsize) % 24
    for t in time[1:]:
        cur_hour = round(t)
        absorp = absorption(0, cur_hour)
        emiss = emission(0)
        net_change = absorp + emiss
        new_value = C[-1] + net_change * stepsize  # eulerian method
        C.append(new_value)
    return [time,C]


def absorption(ID, cur_hour):
    if ID == 0:  # PI-Curve / Michaelis-Menten-Model
        p_max = 1
        ki = 1 / 16
        return -pi_curve(solar_intensity(hour=cur_hour), p_max, ki)
    elif ID == 1:  # Tomato
        return
    elif ID == 2:  # Nelke
        return


def emission(ID, temperature=25):
    if ID == 0:  # Constant model
        constant = 0.5
        return constant
    if ID == 1:  # Gent & Enoch model
        c1 = 1
        c2 = 1
        return c1*np.exp(c2 * (temperature - 25))


# Apply
stepsize = 0.01
#Day1 = model_day(stepsize)
#Day2 = model_day(stepsize, init_val=Day1[-1])
res = evolve(406, 0, (6, 6, 2018), 23, stepsize, 0, 0)

# Plot
#plt.plot(np.arange(0, 24, stepsize), Day1)
#plt.plot(np.arange(0, 24, stepsize), Day2)
plt.plot(res[0], res[1])
plt.show()


