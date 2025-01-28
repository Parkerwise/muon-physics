import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def decay_power_law(x, total_muons, decay_rate):
    equation = total_muons*np.exp(-decay_rate*x)
    return equation


datafile = "25-01-23_sim.csv"
columns = ["decay", "time"]
imported_data = pd.read_csv(datafile, usecols=columns)
valid_times_ns = []
for decay_time in imported_data.decay:
    if decay_time < 40000:
        valid_times_ns.append(decay_time)

occurences = dict.fromkeys(valid_times_ns, 0)
for decay_time in valid_times_ns:
    occurences[decay_time] += 1
lists = sorted(occurences.items())
decay_time, muon_count = zip(*lists)

muon_count = len(valid_times_ns)
rate_guess = 4.54e-4
guess = [muon_count, rate_guess]
parameters, covariance = curve_fit(decay_power_law, decay_time,
                                   muon_count, p0=guess)

# plotting
plt.plot(decay_time, muon_count, "o")
plt.xlabel("Muon decay time")
plt.ylabel("Events")
plt.savefig("muon-histogram.pdf")
# print(len(foo))
# print(len(valid_times_ns))
# plt.hist(valid_times_ns, bins=1)
# plt.show()


# import data
# fit data
# plot fit
