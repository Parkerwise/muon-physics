import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy import signal
fig, (ax1, ax2)=plt.subplots(2,1)
fig.set_figwidth(6)
fig.set_figheight(6)
plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.size': 11})

#plots data
columns=["time","pos"]
df=pd.read_csv("TEK0004.CSV",usecols=[3,4],names=["time","amp"])
time=np.array(df.time)
amp=np.array(df.amp)
start_index=np.where(time==0)[0][0]
end_index=np.where(time==0.4)[0][0]

time=time[start_index:end_index]
amp=amp[start_index:end_index]
peak_indices = signal.find_peaks(amp,width=20)
peak_indices=peak_indices[0]
peak_count = len(peak_indices) # the number of peaks in the array

peaks_time=[time[peak_indices[i]] for i in range(len(peak_indices))]
peaks_amp=[amp[[peak_indices[i]]] for i in range(len(peak_indices))]

def TimeToFreq(t,f0,dt,df):
    conversion_rate=df/dt
    return t*conversion_rate+f0

#we want freq and index number
peaks_freq=[TimeToFreq(peaks_time[i],800,0.4,9200) for i in range(len(peaks_time))]
peaks_index=[i for i in range(len(peaks_time))]
print(peaks_index)
L=0.375

def LinearFit(x,c):
    return (c*(x)/(2*L))+peaks_freq[0]
guess=[343]
parameters, covariance= curve_fit(LinearFit, peaks_index, peaks_freq ,sigma=[0.1]*len(peaks_index))
c=parameters[0]
print(c)
print(peaks_index[1],peaks_freq[1])
fit_freq=[(c*(i))/(2*L)+peaks_freq[0] for i in range(len(peaks_time))]
ax1.plot(peaks_index,fit_freq,label="Fit")
ax1.plot(peaks_index,peaks_freq,"o",label="Data")
residual=[peaks_freq[i]-fit_freq[i] for i in range(len(peaks_time))]
ax2.axhline(0,0,20,color="black",linestyle="dashed")
ax2.plot(peaks_index,residual,"o",color="red",label="Residual")
fig.supxlabel("Resonance Number")
fig.supylabel("Frequency (Hz)",)
ax1.yaxis.tick_right()
ax2.yaxis.tick_right()
ax1.legend()
ax2.legend()
plt.savefig("fitting.pdf")
print(np.sqrt(np.diag(covariance)))
plt.tight_layout()
#plt.show()
