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
# datafile = "data.csv"
datafile = "long-data.csv"
columns = ["decay", "time"]
imported_data = pd.read_csv(datafile, usecols=columns)
valid_times_ns = []
for decay_time in imported_data.decay:
    if decay_time < 40000:
        valid_times_ns.append(decay_time)

# muon_count, edges = np.histogram(valid_times_ns, bins=300)
# decay_time = 0.5 * (edges[:-1] + edges[1:])

occurences = dict.fromkeys(valid_times_ns, 0)
for decay_time in valid_times_ns:
    occurences[decay_time] += 1
lists = sorted(occurences.items())
decay_time, muon_count = zip(*lists)
decay_time = list(decay_time)
muon_count = list(muon_count)
print(f"length {len(valid_times_ns)}")
removed_index = 0
decay_time.pop(removed_index)
muon_count.pop(removed_index)
yerr = [np.sqrt(count) for count in muon_count]
delta_t = decay_time[1] - decay_time[0]
print(f"delta t {delta_t}")
TOTAL_MUONS = len(valid_times_ns)


def decay_power_law(x, decay_rate, B):
    equation = TOTAL_MUONS*delta_t*decay_rate*np.exp(-decay_rate*x)+B
    return equation


rate_guess = 4.54e-4
background_guess = 1
guess = [rate_guess, background_guess]
parameters, covariance = curve_fit(f=decay_power_law, xdata=decay_time,
                                   ydata=muon_count, p0=guess, sigma=yerr, absolute_sigma=True)
model_decay_rate = parameters[0]
model_background = parameters[1]
model_muon_count = []
for time in decay_time:
    entry = decay_power_law(time, model_decay_rate, model_background)
    model_muon_count.append(entry)

# plotting


def straight_line(x, b):
    return b


def find_background(data, tau, iterations, coeff, parameters):
    bg_guess = model_background
    counts = data
    tar = tau
    times = decay_time
    params = parameters
    total_bg = 0
    for i in range(iterations):
        background = [count for count, time in zip(counts, times) if time > coeff*tar]
        bg_times = [time for count, time in zip(counts, times) if time > coeff*tar]
        bg_yerr = [np.sqrt(count) for count in background]
        bg_parameters, bg_covariance = curve_fit(f=straight_line, xdata=bg_times,
                                                 ydata=background, p0=bg_guess, sigma=bg_yerr, absolute_sigma=True)
        new_muon_count = [count - bg_parameters[0] for count in counts if (count - bg_parameters[0]) > 0]
        new_muon_time = [time for count, time in zip(counts, times) if (count - bg_parameters[0]) > 0]
        new_yerr = [np.sqrt(count) for count in new_muon_count]
        new_parameters, new_covariance = curve_fit(f=decay_power_law, xdata=new_muon_time,
                                                   ydata=new_muon_count, p0=params, sigma=new_yerr, absolute_sigma=True)
        new_model_muon_count = []
        for time in new_muon_time:
            entry = decay_power_law(time, new_parameters[0], new_parameters[1])
            new_model_muon_count.append(entry)
        print("decay time", 1/new_parameters[0])
        tar = 1/new_parameters[0]
        # print("tau", tar)
        counts = new_muon_count
        times = new_muon_time
        params = new_parameters
        total_bg += bg_parameters[0]
    return bg_parameters[0], tar, new_parameters, new_muon_time, new_muon_count, total_bg, new_covariance


bg_level, tau, new_parameters, new_time, new_count, total_bg, new_covariance = find_background(muon_count, 1/parameters[0], 10, 2, parameters)
fit_error = np.sqrt(np.diag(new_covariance))
error = np.sqrt((tau)**4*(fit_error[0])**2)
print(f"error {error}")
# bg_level, tau, new_parameters, new_time, new_count, total_bg = find_background(muon_count, 1/parameters[0], 1, 6, parameters)
final_model = []
# print(new_parameters[1])
for time in decay_time:
    entry = decay_power_law(time, new_parameters[0], bg_level)
    final_model.append(entry)
# ax[0].axhline(bg_level, 0, 21000, color="green")
ax[0].errorbar(decay_time, muon_count, yerr=yerr, xerr=20, fmt="o", markersize=1, zorder=1, lw=0.5)
# ax[0].errorbar(new_time, new_count+total_bg, 0, xerr=20, fmt="o", color="black", markersize=3)
ax[0].plot(decay_time, final_model, color="red", label="Model")
# ax[0].plot(decay_time, model_muon_count+bg_level, color="red", label="Model")
# plt.plot(decay_time, real_model_muon_count, color="green")
ax[0].legend()
# ax[0].set_xscale("log")
# ax[0].set_yscale("log")
# ax[0].set_ylim(-1, 40)
ax[0].set_ylabel("Events")
residuals = []
for model_point, real_point in zip(final_model, muon_count):
    residual_point = real_point - model_point
    residuals.append(residual_point)
ax[1].plot(decay_time, residuals, "o", label="Residuals", markersize=1)
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
