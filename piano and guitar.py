# keyboard_demo_06.py
# Play a note using a second-order difference equation
# when the user presses a key on the keyboard.

import pyaudio, struct
import numpy as np
from scipy import signal
from math import sin, cos, pi
import tkinter as Tk
import tkinter.font as tkFont
import ui
import wave

BLOCKLEN = 64  # Number of frames per block
WIDTH = 2  # Bytes per sample
CHANNELS = 1  # Mono
RATE = 8000  # Frames per second

MAXVALUE = 2 ** 15 - 1  # Maximum allowed output signal value (because WIDTH = 2)

output_wavfile = './wav/output_original.wav'
output_wf = wave.open(output_wavfile, 'w')  # wave file
output_wf.setframerate(RATE)
output_wf.setsampwidth(WIDTH)
output_wf.setnchannels(CHANNELS)

# Parameters

majors = {
    'A': 0,
    'bB': 1,
    'C': 3,
    'D': 5,
    'bE': 6,
    'F': 8,
    'G': 10
}


def updateMajorParameters(major):
    Ta = 2

    i = majors[major]
    f0 = 220 * 2 ** (i / 12.0)
    R = [2 ** (1.0 / 12.0 * i) for i in range(20)]  # 1.05946309^i
    f = [f0 * i for i in R]  # 220 * 1.05946309^i

    r = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
    omega = [2.0 * pi * float(i) / RATE for i in f]

    a = [[1, -2 * r * cos(om), r ** 2] for om in omega]
    b = [[r * sin(om)] for om in omega]

    pitches = [int(RATE / i) for i in f]
    BUFFER_LEN = 40
    buffers = [BUFFER_LEN * [0] for _ in range(20)]
    x_guitar = []
    for pitch in pitches:
        x_temp = np.concatenate((np.random.random(pitch) * 10, np.zeros(2000, dtype=int)))
        x_guitar.append(x_temp)
    kr_guitar = [40 - pitch for pitch in pitches]
    kw_guitar = [0] * 20

    return a, b, buffers, x_guitar, kr_guitar, kw_guitar


root = Tk.Tk()
ui = ui.Interface()

title = Tk.Label(root, text="Piano & Guitar Keyboard", font=tkFont.Font(family='times', size=16, weight='bold'))
title.pack(side=Tk.TOP)

root.bind("<Key>", ui.my_function)

majorFrame = Tk.Frame(root, borderwidth=2, width=40, height=60)
majorFrame.pack(side=Tk.BOTTOM)
majorTitle = Tk.Label(majorFrame, text="Major Selection", font=tkFont.Font(family='times', weight='bold'))
majorTitle.pack(side=Tk.TOP)

major = Tk.StringVar()
major1 = Tk.Radiobutton(majorFrame, text='A', variable=major, value='A')
major2 = Tk.Radiobutton(majorFrame, text='bB', variable=major, value='bB')
major3 = Tk.Radiobutton(majorFrame, text='C', variable=major, value='C')
major4 = Tk.Radiobutton(majorFrame, text='D', variable=major, value='D')
major5 = Tk.Radiobutton(majorFrame, text='bE', variable=major, value='bE')
major6 = Tk.Radiobutton(majorFrame, text='F', variable=major, value='F')
major7 = Tk.Radiobutton(majorFrame, text='G', variable=major, value='G')
major.set('C')

major1.pack(side=Tk.LEFT)
major2.pack(side=Tk.LEFT)
major3.pack(side=Tk.LEFT)
major4.pack(side=Tk.LEFT)
major5.pack(side=Tk.LEFT)
major6.pack(side=Tk.LEFT)
major7.pack(side=Tk.LEFT)

m = Tk.IntVar()

modeFrame = Tk.Frame(root, borderwidth=2, width=40, height=60)
modeFrame.pack(side=Tk.BOTTOM)
modeTitle = Tk.Label(modeFrame, text="Mode Selection", font=tkFont.Font(family='times', weight='bold'))
modeTitle.pack(side=Tk.TOP)

m1 = Tk.Radiobutton(modeFrame, text='piano', variable=m, value=0)
m2 = Tk.Radiobutton(modeFrame, text='guitar', variable=m, value=1)

m1.pack(side=Tk.LEFT)
m2.pack(side=Tk.LEFT)

Ta = 2  # Decay time (seconds)
f0 = 220 * 2 ** (3.0 / 12.0)  # Frequency (Hz) (note A)
R = [2 ** (1.0 / 12.0 * i) for i in range(20)]  # 1.05946309^i
f = [f0 * i for i in R]  # 220 * 1.05946309^i

# Pole radius and angle
r = 0.01 ** (1.0 / (Ta * RATE))  # 0.01 for 1 percent amplitude
omega = [2.0 * pi * float(i) / RATE for i in f]

# Filter coefficients (second-order IIR)
a = [[1, -2 * r * cos(om), r ** 2] for om in omega]
b = [[r * sin(om)] for om in omega]

ORDER = 2  # filter order

states = [np.zeros(ORDER) for i in range(20)]
x = [np.zeros(BLOCKLEN) for i in range(20)]
total = np.zeros(BLOCKLEN)

# parameters for guitar
K = 0.93
G = 20000

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
    format=PA_FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=False,
    output=True,
    frames_per_buffer=128)
# specify low frames_per_buffer to reduce latency

CONTINUE = True

root.bind("<Key>", ui.my_function)

ui.addRecording(root)
ui.updateUI(root)

print('Press "q" - "]" & "2,3,5,6,7,9,0,=" for sound.')
print('Press "x" to quit')

while CONTINUE:
    root.update()
    mode = m.get()

    maj = major.get()

    a, b, buffers, x_guitar, kr_guitar, kw_guitar = updateMajorParameters(maj)

    KEYPRESS = ui.KEYPRESS

    CONTINUE = ui.CONTINUE
    recording = list()

    if mode == 0:
        total = np.zeros(BLOCKLEN)
        for i in range(20):
            if KEYPRESS[i] and CONTINUE:
                x[i][0] = 10000.0
            [y, states[i]] = signal.lfilter(b[i], a[i], x[i], zi=states[i])
            x[i][0] = 0.0
            KEYPRESS[i] = False
            y = np.clip(y.astype(int), -MAXVALUE, MAXVALUE)  # Clipping
            total = total + y
        total = np.clip(total.astype(int), -MAXVALUE, MAXVALUE)
        binary_data = struct.pack('h' * BLOCKLEN, *total)  # Convert to binary binary data
        if ui.RECORDING:
            output_wf.writeframes(binary_data)
        stream.write(binary_data, BLOCKLEN)  # Write binary binary data to audio output

    elif mode == 1:
        gain_guitar = [0] * 20
        total = [[0] * 2036 for i in range(20)]
        subtotal = [[0] * 2036 for i in range(20)]

        for i in range(20):
            # y = 0
            if KEYPRESS[i] and CONTINUE:
                # Some key (not 'q') was pressed
                gain_guitar[i] = G
                for j in range(len(x_guitar[i])):
                    y = gain_guitar[i] * x_guitar[i][j] + K / 2 * buffers[i][kr_guitar[i]] + K / 2 * buffers[i][kr_guitar[i] - 1]
                    buffers[i][kw_guitar[i]] = y
                    subtotal[i][j] = y

                    kr_guitar[i] = kr_guitar[i] + 1
                    if kr_guitar[i] >= 40:
                        # The index has reached the end of the buffer. Circle the index back to the front.
                        kr_guitar[i] = 0
                    kw_guitar[i] = kw_guitar[i] + 1
                    if kw_guitar[i] >= 40:
                        # The index has reached the end of the buffer. Circle the index back to the front.
                        kw_guitar[i] = 0

                gain_guitar[i] = 0.0
                KEYPRESS[i] = False

                for j in range(2036):
                    total[i][j] = total[i][j] + subtotal[i][j]
                    total[i][j] = int(np.clip(total[i][j], -MAXVALUE, MAXVALUE))  # Clipping
                binary_data = struct.pack('h'*2036, *total[i])  # Convert to binary binary data
                if ui.RECORDING:
                    output_wf.writeframes(binary_data)
                stream.write(binary_data)  # Write binary binary data to audio output

print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()
output_wf.close()