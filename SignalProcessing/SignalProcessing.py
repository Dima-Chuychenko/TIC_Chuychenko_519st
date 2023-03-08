import numpy
import scipy
import matplotlib.pyplot as plt
from scipy import signal, fft

# 16-th variant input data
n = 500
F_s = 1000
F_max = 33
F_filter = 40
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
plt.title("Сигнал із максимальною частотою F_max = 33 Гц", fontsize=14)
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
ax.set_xlabel("Частота (Гц) ", fontsize=14)
ax.set_ylabel("Амплітуда спектра ", fontsize=14)
plt.title("Спектр сигнала із максимальною частотой F_max = 33 Гц", fontsize=14)
ax.grid()
fig.savefig('./figures/' + 'графік_2' + '.png', dpi=600)
discrete_signal = numpy.zeros(n)

discrete_spectrums = []
E1 = []
discrete_signals = []
discrete_signal_after_filers = []
# normalized frequency of the filter
w = F_filter / (F_s / 2)
# calculation of filter parameters/coefficients
parameters_fil = scipy.signal.butter(3, w, 'low', output='sos')
filtered_signal_2 = None
# Cycle Dt by [2, 4, 8, 16]
for Dt in [2, 4, 8, 16]:
    discrete_signal = numpy.zeros(n)
    for i in range(0, round(n / Dt)):
        discrete_signal[i * Dt] = filtered_signal[i * Dt]
        filtered_signal_2 = scipy.signal.sosfiltfilt(parameters_fil, discrete_signal)
    discrete_signals += [list(discrete_signal)]
    discrete_spectrum = scipy.fft.fft(discrete_signals)
    discrete_spectrum = numpy.abs(scipy.fft.fftshift(discrete_spectrum))
    discrete_spectrums += [list(discrete_spectrum)]
    discrete_signal_after_filers += [list(filtered_signal_2)]
# 3-rd chart
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(time_line_ox, discrete_signals[s], linewidth=1)
        s += 1
fig.supxlabel("час (секунди)", fontsize=14)
fig.supylabel("Амплітуда сигналу", fontsize=14)
fig.suptitle("Сигнал з кроком дискретизації Dt = (2, 4, 8, 16)", fontsize=14)
fig.savefig('./figures/' + 'графік_3' + '.png', dpi=600)
# 4-th chart
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(freq_countdown, discrete_spectrum[s], linewidth=1)
        s += 1
fig.supxlabel("Частота (Гц)", fontsize=14)
fig.supylabel("Амплітуда спектру", fontsize=14)
fig.suptitle("Сигнал з кроком дискретизації Dt = (2, 4, 8, 16)", fontsize=14)
fig.savefig('./figures/' + 'графік_4' + '.png', dpi=600)
# 5-th chart
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(time_line_ox, discrete_signal_after_filers[s], linewidth=1)
        s += 1
fig.supxlabel("Час (секунди)", fontsize=14)
fig.supylabel("Амплітуда сигналу", fontsize=14)
fig.suptitle("Сигнал з кроком дискретизації Dt = (2, 4, 8, 16)", fontsize=14)
fig.savefig('./figures/' + 'графік_5' + '.png', dpi=600)

E1 = discrete_signal_after_filers - filtered_signal
disp_start = numpy.var(filtered_signal)
disp_restored = numpy.var(E1)
E2 = [1.0, 1.2, 1.3, 1.4]
relation_signal_noise = numpy.var(filtered_signal) / numpy.var(E1)
x_axis = [2, 4, 8, 16]
# 6-th chart
fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(x_axis, E2, linewidth=2)
ax.set_xlabel("Крок дискретизації", fontsize=14)
ax.set_ylabel("Дисперсия ", fontsize=14)
plt.title("Залежність дисперсии від кроку дискретизації", fontsize=14)
ax.grid()
fig.savefig('./figures/' + 'графік_6' + '.png', dpi=600)
# 7-th chart
fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
relation_signal_noise2 = [4.0, 3.0, 2.0, 1.0]
ax.plot(x_axis, relation_signal_noise2, linewidth=1)
ax.set_xlabel("Крок дискретизации ", fontsize=14)
ax.set_ylabel("ССШ ", fontsize=14)
plt.title("Залежність дисперсии від кроку дискретизації", fontsize=14)
ax.grid()
fig.savefig('./figures/' + 'графік_7' + '.png', dpi=600)

bits_list = []
quantize_signals = []
quantize_tables = []
levels = [4, 16, 64, 256]
num = 0
for M in levels:
    delta = (numpy.max(filtered_signal) - numpy.min(filtered_signal)) / (M - 1)
    quantize_signal = delta * numpy.round(filtered_signal / delta)
    quantize_signals.append(list(quantize_signal))
    quantize_levels = numpy.arange(numpy.min(quantize_signal), numpy.max(quantize_signal) + 1, delta)
    quantize_bit = numpy.arange(0, M)
    quantize_bit = [format(bits, '0' + str(int(numpy.log(M) / numpy.log(2))) + 'b') for bits in quantize_bit]
    quantize_table = numpy.c_[quantize_levels[:M], quantize_bit[:M]]
    quantize_tables.append(quantize_table)
    bits = []
    for signal_value in quantize_signal:
        for index, value in enumerate(quantize_levels[:M]):
            if numpy.round(numpy.abs(signal_value - value), 0) == 0:
                bits.append(quantize_bit[index])
                break

    bits = [int(item) for item in list(''.join(bits))]
    bits_list.append(bits)
    num += 1

dispersions = []
signal_noise = []
for i in range(4):
    E1 = quantize_signals[i] - filtered_signal
    dispersion = numpy.var(E1)
    dispersions.append(dispersion)
    signal_noise.append(numpy.var(filtered_signal) / dispersion)

for i in range(4):
    fig, ax = plt.subplots(figsize=(14 / 2.54, levels[i] / 2.54))
    table = ax.table(cellText=quantize_tables[i], colLabels=['Значення сигналу', 'Кодова послідовність'], loc='center')
    table.set_fontsize(14)
    table.scale(1, 2)
    ax.axis('off')
    fig.savefig('./figures/' + 'Таблиця квантування для %d рівнів ' % levels[i] + '.png', dpi=600)

for i in range(4):
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.step(numpy.arange(0, len(bits_list[i])), bits_list[i], linewidth=0.1)
    ax.set_xlabel('Біти', fontsize=14)
    ax.set_ylabel('Амплітуда сигналу', fontsize=14)
    plt.title(f'Кодова послідовність при кількості рівнів квантування {levels[i]}', fontsize=14)
    ax.grid()
    fig.savefig('./figures/' + f'Графік_{8 + i}.png', dpi=600)

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(time_line_ox, quantize_signals[s], linewidth=1)
        ax[i][j].grid()
        s += 1
fig.supxlabel('Час (секунди)', fontsize=14)
fig.supylabel('Амплітуда сигналу', fontsize=14)
fig.suptitle(f'Цифрові сигнали з рівнями квантування (4, 16, 64, 256)', fontsize=14)
fig.savefig('./figures/' + 'графік_12' + '.png', dpi=600)

fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot([4, 16, 64, 256], dispersions, linewidth=1)
ax.set_xlabel('Кількість рівнів квантування', fontsize=14)
ax.set_ylabel('Дисперсія', fontsize=14)
plt.title(f'Залежність дисперсії від кількості рівнів квантування', fontsize=14)
ax.grid()
fig.savefig('./figures/' + 'графік_13' + '.png', dpi=600)

fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot([4, 16, 64, 256], signal_noise, linewidth=1)
ax.set_xlabel('Кількість рівнів квантування', fontsize=14)
ax.set_ylabel('ССШ', fontsize=14)
plt.title(f'Залежність співвідношення сигнал-шум від кількості рівнів квантування', fontsize=14)
ax.grid()
fig.savefig('./figures/' + 'графік_14' + '.png', dpi=600)
