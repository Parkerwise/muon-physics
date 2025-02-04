import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from my_plot import set_size
tex_fonts = {
    # Use LaTeX to write all text
    "text.usetex": True,
    "font.family": "serif",
    # Use 10pt font in plots, to match 10pt font in document
    "axes.labelsize": 10,
    "font.size": 10,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
}

plt.rcParams.update(tex_fonts)

width = 452.0
fig, ax = plt.subplots(2, 1, figsize=set_size(width))

# # plt.rcParams('text.latex', preamble=r'\usepackage{lmodern}')
# plt.rcParams['text.latex.preamble'] = r"\usepackage{lmodern}"
# params = {'text.usetex': True,
#           'font.size': 11,
#           # 'font.family': 'lmodern',
#           # 'text.latex.unicode': True,
#           }
# plt.rcParams.update(params)


def decay_power_law(x, total_muons, decay_rate, B):
    equation = total_muons*np.exp(-decay_rate*x)+B
    return equation


datafile = "data.csv"
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
background_guess = 0
guess = [total_muon_count, rate_guess, background_guess]
parameters, covariance = curve_fit(f=decay_power_law, xdata=decay_time,
                                   ydata=muon_count, p0=guess)

model_total = parameters[0]
model_decay_rate = parameters[1]
model_background = parameters[2]
fit_error = np.sqrt(np.diag(covariance))
error = np.sqrt((model_decay_rate)**-4*(fit_error[1])**2)
model_muon_count = []
for time in decay_time:
    entry = decay_power_law(time, model_total, model_decay_rate,
                            model_background)
    model_muon_count.append(entry)

# real_model_muon_count = []
# for time in decay_time:
#     entry = decay_power_law(time, total_muon_count, rate_guess)
#     real_model_muon_count.append(entry)

# plotting
# ax.errorbar(decay_time, muon_count, 0, 1, fmt=".")
ax[0].plot(decay_time, muon_count, ".", label="Decay Events", markersize=3)
ax[0].plot(decay_time, model_muon_count, color="red", label="Model")
# plt.plot(decay_time, real_model_muon_count, color="green")
ax[0].legend()
# ax[0].set_xscale("log")
# ax[0].set_yscale("log")
ax[0].set_ylim(-1, 40)
# ax[0].set_xlabel("Muon decay time (ns)")
ax[0].set_ylabel("Events")

residuals = []
for model_point, real_point in zip(model_muon_count, muon_count):
    residual_point = real_point - model_point
    residuals.append(residual_point)
ax[1].plot(decay_time, residuals, ".", markersize=3, label="Residuals")
ax[1].legend()
ax[1].axhline(0, -100, 21000, color="red", ls="dashed")
ax[1].set_xlabel("Muon decay time (ns)")
ax[1].set_ylabel("Residuals")
ax[0].set_xticklabels([])
plt.subplots_adjust(hspace=0.1)
ax[0].tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    labelbottom=False)
fig.align_ylabels()
fig.savefig("muon-histogram.pdf", bbox_inches='tight')
TAU = 1/model_decay_rate
ax[0].axvline(5*TAU, 0, 40, color="red", ls="dashed")
print(1/parameters[1])
plt.show()


# def straight_line(x, b):
#     return b
#
#
# def find_background(data, tau, iterations, coeff, parameters):
# #     bg_guess = 0
#     counts = data
#     tar = tau
#     times = decay_time
#     params = parameters
    # for i in range(iterations):
    #     background = [count for count, time in zip(counts, times) if time > coeff*tar]
    #     bg_times = [time for count, time in zip(counts, times) if time > coeff*tar]
    #     bg_parameters, bg_covariance = curve_fit(f=straight_line, xdata=bg_times,
    #                                              ydata=background, p0=bg_guess)
    #     # plt.plot(bg_times, background, ".", "green", markersize=3)
    #     # plt.plot(times, counts, ".", markersize=3)
    #     # new_muon_count = [count - bg_parameters[0] for count in counts if count - bg_parameters[0] > 0]
    #     new_muon_count = [count - bg_parameters[0] for count in counts if (count - bg_parameters[0]) > 0]
    #     new_muon_time = [time for count, time in zip(counts, times) if (count - bg_parameters[0]) > 0]
    #     new_parameters, new_covariance = curve_fit(f=decay_power_law, xdata=new_muon_time,
    #                                                ydata=new_muon_count, p0=params)
    #     new_model_muon_count = []
    #     for time in new_muon_time:
    #         entry = decay_power_law(time, new_parameters[0], new_parameters[1], new_parameters[2])
    #         new_model_muon_count.append(entry)
    #     plt.hlines(bg_parameters[0], 0, 21000, "black")
    #     plt.plot(new_muon_time, new_muon_count, ".", markersize=3)
    #     plt.plot(new_muon_time, new_model_muon_count, ".", markersize=3)
    #     plt.show()
    #     print("decay time", 1/new_parameters[1])
    #     print("bg", bg_parameters[0])
    #     tar = 1/new_parameters[1]
    #     print("tau", tar)
    #     counts = new_muon_count
    #     times = new_muon_time
    #     params = new_parameters
    # return bg_parameters


# find_background(muon_count, TAU, 3, 5, parameters)
