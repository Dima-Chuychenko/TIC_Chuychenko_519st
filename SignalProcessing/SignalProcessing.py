import numpy
import scipy
import matplotlib.pyplot as plt
from scipy import signal, fft

# 16-th variant input data
n = 500
F_s = 1000
F_max = 33
# Signal generation
random = numpy.random.normal(0, 10, n)
# Determination of time counts that will be displayed on the OX axis of the graph
time_line_ox = numpy.arange(n) / F_s
# Calculation of filter parameters
w = F_max / (F_s / 2)
parameters_filter = scipy.signal.butter(3, w, 'low', output='sos')
# Signal filtering
filtered_signal = scipy.signal.sosfiltfilt(parameters_filter, random)
# 1-st chart
fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(time_line_ox, filtered_signal, linewidth=1)
ax.set_xlabel("Час (секунди) ", fontsize=14)
ax.set_ylabel("Амплітуда сигналу ", fontsize=14)
plt.title("Сигнал із максимальною частотою Fmax = 33", fontsize=14)
ax.grid()
fig.savefig('./figures/' + 'графік_1' + '.png', dpi=600)
dpi = 600
# Calculation of the signal spectrum
spectrum = scipy.fft.fft(filtered_signal)
spectrum = numpy.abs(scipy.fft.fftshift(spectrum))
length_signal = n
freq_countdown = scipy.fft.fftfreq(length_signal, 1 / length_signal)
freq_countdown = scipy.fft.fftshift(freq_countdown)
# 2-nd chart
fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(freq_countdown, spectrum, linewidth=1)
ax.set_xlabel("Час (секунди) ", fontsize=14)
ax.set_ylabel("Амплітуда спектра ", fontsize=14)
plt.title("Спектр сигнала із максимальною частотой Fmax = 21", fontsize=14)
ax.grid()
fig.savefig('./figures/' + 'графік_2' + '.png', dpi=600)
