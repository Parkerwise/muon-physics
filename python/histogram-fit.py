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

total_muon_count = len(valid_times_ns)
rate_guess = 4.54e-4
guess = [total_muon_count, rate_guess]
parameters, covariance = curve_fit(f=decay_power_law, xdata=decay_time,
                                   ydata=muon_count, p0=guess)

model_total = parameters[0]
model_decay_rate = parameters[1]
model_muon_count = []
for time in decay_time:
    entry = decay_power_law(time, model_total, model_decay_rate)
    model_muon_count.append(entry)

# real_model_muon_count = []
# for time in decay_time:
#     entry = decay_power_law(time, total_muon_count, rate_guess)
#     real_model_muon_count.append(entry)

# plotting
plt.plot(decay_time, muon_count, "o")
plt.plot(decay_time, model_muon_count, color="red")
# plt.plot(decay_time, real_model_muon_count, color="green")
plt.xlabel("Muon decay time")
plt.ylabel("Events")
plt.show()
# plt.savefig("muon-histogram.pdf")
# plt.hist(valid_times_ns, bins=1)
# plt.show()
