# keyboard_demo_06.py
# Play a note using a second-order difference equation
# when the user presses a key on the keyboard.

import pyaudio, struct
import numpy as np
from scipy import signal
from math import sin, cos, pi
import tkinter as Tk
import ui
from threading import Thread

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 2      # Decay time (seconds)
f0 = 220 * 2 ** (3.0/12.0)    # Frequency (Hz) (note A)
R = [2 ** (1.0/12.0 * i) for i in range(20)]    # 1.05946309^i
f = [f0 * i for i in R]     # 220 * 1.05946309^i

# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
omega = [2.0 * pi * float(i)/RATE for i in f]


# Filter coefficients (second-order IIR)
a = [[1, -2*r*cos(om), r**2] for om in omega]
b = [[r*sin(om)] for om in omega]

ORDER = 2   # filter order

states = [np.zeros(ORDER) for i in range(20)]
x = [np.zeros(BLOCKLEN) for i in range(20)]
total = np.zeros(BLOCKLEN)

# parameters for guitar
K = 0.93
G = 20000

pitches = [int(RATE/i) for i in f]
BUFFER_LEN = [i for i in pitches]
buffers = [i * [0] for i in BUFFER_LEN]

kr_guitar = [0] * 20
kw_guitar = [0] * 20
gain_guitar = [0] * 20

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
        format      = PA_FORMAT,
        channels    = CHANNELS,
        rate        = RATE,
        input       = False,
        output      = True,
        frames_per_buffer = 128)
# specify low frames_per_buffer to reduce latency

CONTINUE = True
# KEYPRESS = [False for i in range(20)]
#
# def my_function(event):
#     global CONTINUE
#     global KEYPRESS
#     global f
#
#     print('You pressed ' + event.char)
#
#     if event.char == 'x':
#       print('Good Bye')
#       CONTINUE = False
#
#     keys = ['q', '2', 'w', '3', 'e', 'r', '5', 't', '6', 'y', '7', 'u', 'i', '9', 'o', '0', 'p', '[', '=', ']']
#
#     for i in range(20):
#         if event.char == keys[i]:
#             print('Frequency: %.2f' %f[i])
#             KEYPRESS[i] = True

root = Tk.Tk()
ui = ui.Interface()
# my_function = ui.my_function()

root.bind("<Key>", ui.my_function)

ui.updateUI(root)

m = Tk.IntVar()


m1 = Tk.Radiobutton(root, text='piano',variable=m, value=0)
m2 = Tk.Radiobutton(root, text='guitar',variable=m, value=1)

m1.pack(side = Tk.LEFT)
m2.pack(side = Tk.TOP)

print('Press keys for sound.')
print('Press "x" to quit')



while CONTINUE:
    root.update()
    mode = m.get()
    KEYPRESS = ui.KEYPRESS

    # print(KEYPRESS)
    CONTINUE = ui.CONTINUE
    # thread1 = Thread(target=)

    if mode == 0:
        total = np.zeros(BLOCKLEN)
        for i in range(20):
            if KEYPRESS[i] and CONTINUE:
                x[i][0] = 10000.0
            [y, states[i]] = signal.lfilter(b[i], a[i], x[i], zi = states[i])
            x[i][0] = 0.0        
            KEYPRESS[i] = False
            y = np.clip(y.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
            total = total + y
        total = np.clip(total.astype(int), -MAXVALUE, MAXVALUE)
        binary_data = struct.pack('h' * BLOCKLEN, *total);    # Convert to binary binary data
        stream.write(binary_data, BLOCKLEN)               # Write binary binary data to audio output

    elif mode == 1:

        for i in range(0, BLOCKLEN):
            total = 0
            for i in range(20):
                if KEYPRESS[i] and CONTINUE:
                    # Some key (not 'q') was pressed
                    gain_guitar[i] = G
                y = gain_guitar[i] + K/2 * buffers[i][kr_guitar[i]] + K/2 * buffers[i][kr_guitar[i]-1]
                buffers[i][kw_guitar[i]] = y
                kr_guitar[i] = kr_guitar[i] + 1
                if kr_guitar[i] >= BUFFER_LEN[i]:
                    # The index has reached the end of the buffer. Circle the index back to the front.
                    kr_guitar[i] = 0
                kw_guitar[i] = kw_guitar[i] + 1
                if kw_guitar[i] >= BUFFER_LEN[i]:
                    # The index has reached the end of the buffer. Circle the index back to the front.
                    kw_guitar[i] = 0
                KEYPRESS[i] = False
                y = np.clip(y, -MAXVALUE, MAXVALUE)     # Clipping
                total = total + y
            total = np.clip(total, -MAXVALUE, MAXVALUE)
            binary_data = struct.pack('h', int(total))    # Convert to binary binary data
            stream.write(binary_data)               # Write binary binary data to audio output
            for i in range(20):
                gain_guitar[i] = 0


print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()