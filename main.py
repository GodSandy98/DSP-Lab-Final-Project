# keyboard_demo_06.py
# Play a note using a second-order difference equation
# when the user presses a key on the keyboard.

import pyaudio, struct
import numpy as np
from scipy import signal
from math import sin, cos, pi
import tkinter as Tk

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 2      # Decay time (seconds)
f0 = 220    # Frequency (Hz) (note A)
f1 = 440
C1 = f0 * 2 ** (3.0/12.0) #261
D1 = f0 * 2 ** (5.0/12.0) #293
E1 = f0 * 2 ** (7.0/12.0) #329
F1 = f0 * 2 ** (8.0/12.0) #349
G1 = f0 * 2 ** (10.0/12.0) #392
A1 = f0 * 2 ** (12.0/12.0) #440

B1 = f1 * 2 ** (2.0/12.0) #494
C2 = f1 * 2 ** (3.0/12.0) #523
D2 = f1 * 2 ** (5.0/12.0) #587
E2 = f1 * 2 ** (7.0/12.0) #659
F2 = f1 * 2 ** (8.0/12.0) #698
G2 = f1 * 2 ** (10.0/12.0) #784

print(G2)
# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
om0 = 2.0 * pi * float(C1)/RATE
om1 = 2.0 * pi * float(D1)/RATE
om2 = 2.0 * pi * float(E1)/RATE
om3 = 2.0 * pi * float(F1)/RATE
om4 = 2.0 * pi * float(G1)/RATE
om5 = 2.0 * pi * float(A1)/RATE
om6 = 2.0 * pi * float(B1)/RATE
om7 = 2.0 * pi * float(C2)/RATE
om8 = 2.0 * pi * float(D2)/RATE
om9 = 2.0 * pi * float(E2)/RATE
om10 = 2.0 * pi * float(F2)/RATE
om11 = 2.0 * pi * float(G2)/RATE




# Filter coefficients (second-order IIR)
a0 = [1, -2*r*cos(om0), r**2]
a1 = [1, -2*r*cos(om1), r**2]
a2 = [1, -2*r*cos(om2), r**2]
a3 = [1, -2*r*cos(om3), r**2]
a4 = [1, -2*r*cos(om4), r**2]
a5 = [1, -2*r*cos(om5), r**2]
a6 = [1, -2*r*cos(om6), r**2]
a7 = [1, -2*r*cos(om7), r**2]
a8 = [1, -2*r*cos(om8), r**2]
a9 = [1, -2*r*cos(om9), r**2]
a10 = [1, -2*r*cos(om10), r**2]
a11 = [1, -2*r*cos(om11), r**2]

b0 = [r*sin(om0)]
b1 = [r*sin(om1)]
b2 = [r*sin(om2)]
b3 = [r*sin(om3)]
b4 = [r*sin(om4)]
b5 = [r*sin(om5)]
b6 = [r*sin(om6)]
b7 = [r*sin(om7)]
b8 = [r*sin(om8)]
b9 = [r*sin(om9)]
b10 = [r*sin(om10)]
b11 = [r*sin(om11)]

ORDER = 2   # filter order

states0 = np.zeros(ORDER)
states1 = np.zeros(ORDER)
states2 = np.zeros(ORDER)
states3 = np.zeros(ORDER)
states4 = np.zeros(ORDER)
states5 = np.zeros(ORDER)
states6 = np.zeros(ORDER)
states7 = np.zeros(ORDER)
states8 = np.zeros(ORDER)
states9 = np.zeros(ORDER)
states10 = np.zeros(ORDER)
states11 = np.zeros(ORDER)

x0 = np.zeros(BLOCKLEN)
x1 = np.zeros(BLOCKLEN)
x2 = np.zeros(BLOCKLEN)
x3 = np.zeros(BLOCKLEN)
x4 = np.zeros(BLOCKLEN)
x5 = np.zeros(BLOCKLEN)
x6 = np.zeros(BLOCKLEN)
x7 = np.zeros(BLOCKLEN)
x8 = np.zeros(BLOCKLEN)
x9 = np.zeros(BLOCKLEN)
x10 = np.zeros(BLOCKLEN)
x11 = np.zeros(BLOCKLEN)


K = 0.93
G = 10000

p1 = int(RATE/C1)
p2 = int(RATE/D1)
p3 = int(RATE/E1)
p4 = int(RATE/F1)
p5 = int(RATE/G1)
p6 = int(RATE/A1)
p7 = int(RATE/B1)
p8 = int(RATE/C2)
p9 = int(RATE/D2)
p10 = int(RATE/E2)
p11 = int(RATE/F2)
p12 = int(RATE/G2)

BUFFER_LEN1 = p1              # length of buffer
buffer1 = BUFFER_LEN1 * [0]   # list of zeros
BUFFER_LEN2 = p2              # length of buffer
buffer2 = BUFFER_LEN2 * [0]   # list of zeros
BUFFER_LEN3 = p3              # length of buffer
buffer3 = BUFFER_LEN3 * [0]   # list of zeros
BUFFER_LEN4 = p4              # length of buffer
buffer4 = BUFFER_LEN4 * [0]   # list of zeros
BUFFER_LEN5 = p5              # length of buffer
buffer5 = BUFFER_LEN5 * [0]   # list of zeros
BUFFER_LEN6 = p6              # length of buffer
buffer6 = BUFFER_LEN6 * [0]   # list of zeros
BUFFER_LEN7 = p7              # length of buffer
buffer7 = BUFFER_LEN7 * [0]   # list of zeros
BUFFER_LEN8 = p8              # length of buffer
buffer8 = BUFFER_LEN8 * [0]   # list of zeros
BUFFER_LEN9 = p9              # length of buffer
buffer9 = BUFFER_LEN9 * [0]   # list of zeros
BUFFER_LEN10 = p10             # length of buffer
buffer10 = BUFFER_LEN10 * [0]   # list of zeros
BUFFER_LEN11 = p11              # length of buffer
buffer11 = BUFFER_LEN11 * [0]   # list of zeros
BUFFER_LEN12 = p12              # length of buffer
buffer12 = BUFFER_LEN12 * [0]   # list of zeros

kr1 = 0
kr2 = 0
kr3 = 0
kr4 = 0
kr5 = 0
kr6 = 0
kr7 = 0
kr8 = 0
kr9 = 0
kr10 = 0
kr11 = 0
kr12 = 0

kw1 = 0
kw2 = 0
kw3 = 0
kw4 = 0
kw5 = 0
kw6 = 0
kw7 = 0
kw8 = 0
kw9 = 0
kw10 = 0
kw11 = 0
kw12 = 0

g1 = 0
g2 = 0
g3 = 0
g4 = 0
g5 = 0
g6 = 0
g7 = 0
g8 = 0
g9 = 0
g10 = 0
g11 = 0
g12 = 0


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

KEYPRESS0 = False
KEYPRESS1 = False
KEYPRESS2 = False
KEYPRESS3 = False
KEYPRESS4 = False
KEYPRESS5 = False
KEYPRESS6 = False
KEYPRESS7 = False
KEYPRESS8 = False
KEYPRESS9 = False
KEYPRESS10 = False
KEYPRESS11 = False





def my_function(event):
    global CONTINUE
    global KEYPRESS0
    global KEYPRESS1
    global KEYPRESS2
    global KEYPRESS3
    global KEYPRESS4
    global KEYPRESS5
    global KEYPRESS6
    global KEYPRESS7
    global KEYPRESS8
    global KEYPRESS9
    global KEYPRESS10
    global KEYPRESS11

    print('You pressed ' + event.char)
    if event.char == 'q':
      print('Good Bye')
      CONTINUE = False

    if event.char == 'a':
      print('Frequency: %.2f' %C1)
      KEYPRESS0 = True

    if event.char == 's':
      print('Frequency: %.2f' %D1)
      KEYPRESS1 = True

    if event.char == 'd':
      print('Frequency: %.2f' %E1)
      KEYPRESS2 = True

    if event.char == 'f':
      print('Frequency: %.2f' %F1)
      KEYPRESS3 = True

    if event.char == 'j':
      print('Frequency: %.2f' %G1)
      KEYPRESS4 = True

    if event.char == 'k':
      print('Frequency: %.2f' %A1)
      KEYPRESS5 = True

    if event.char == 'l':
      print('Frequency: %.2f' %B1)
      KEYPRESS6 = True

    if event.char == ';':
      print('Frequency: %.2f' %C2)
      KEYPRESS7 = True

    if event.char == 'c':
      print('Frequency: %.2f' %D2)
      KEYPRESS8 = True

    if event.char == 'v':
      print('Frequency: %.2f' %E2)
      KEYPRESS9 = True

    if event.char == 'n':
      print('Frequency: %.2f' %F2)
      KEYPRESS10 = True

    if event.char == 'm':
      print('Frequency: %.2f' %G2)
      KEYPRESS11 = True


root = Tk.Tk()
root.bind("<Key>", my_function)

m = Tk.IntVar()


m1 = Tk.Radiobutton(root, text='piano',variable=m, value=0)
m2 = Tk.Radiobutton(root, text='guitar',variable=m, value=1)

m1.pack(side = Tk.LEFT)
m2.pack(side = Tk.TOP)

print('Press keys for sound.')
print('Press "q" to quit')

def noteClicked(event):
   a1 = 2
   print(a1)


frame = Tk.Frame(root, borderwidth=2, width=560, height=250)
frame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

btnDown = list()
btnUp = list()


for i in range(12):
    btnDown.append(Tk.Button(frame, bg='white', fg='black', bd=0))
    cur = btnDown[-1]
    cur.place(x=40+i*20, y=120, width=20, height=40)
    cur.bind('<Button>')

btnUp.append(Tk.Button(frame, bg='white', fg='black', bd=0))
cur = btnUp[-1]
cur.place(x=40, y=40, width=10, height=80)
cur.bind('<Button>', noteClicked)

for j in range(2):
    for i in range(2):
        btnUp.append(Tk.Button(frame, bg='white', fg='black', bd=0))
        cur = btnUp[-1]
        cur.place(x=50+j*137.5 + i * 20, y=40, width=2.5, height=80)
        cur.bind('<Button>', noteClicked)

        btnUp.append(Tk.Button(frame, bg='black', fg='white'))
        cur = btnUp[-1]
        cur.place(x=52.5+j*137.5 + i * 20, y=40, width=15, height=80)
        cur.bind('<Button>', noteClicked)

        btnUp.append(Tk.Button(frame, bg='white', fg='black', bd=0))
        cur = btnUp[-1]
        cur.place(x=67.5+j*137.5 + i * 20, y=40, width=2.5, height=80)
        cur.bind('<Button>', noteClicked)

        # for i in range(2):
        btnUp.append(Tk.Button(frame, bg='white', fg='black', bd=0))
        cur = btnUp[-1]
        cur.place(x=87.5+j*140+i*10, y=40, width=10, height=80)
        cur.bind('<Button>', noteClicked)

for i in range(3):
    btnUp.append(Tk.Button(frame, bg='white', fg='black', bd=0))
    cur = btnUp[-1]
    cur.place(x=107.5 + i*20, y=40, width=2.5, height=80)
    cur.bind('<Button>', noteClicked)

    btnUp.append(Tk.Button(frame, bg='black', fg='white'))
    cur = btnUp[-1]
    cur.place(x=110 + i*20, y=40, width=15, height=80)
    cur.bind('<Button>', noteClicked)

    btnUp.append(Tk.Button(frame, bg='white', fg='black', bd=0))
    cur = btnUp[-1]
    cur.place(x=125 + i*20, y=40, width=2.5, height=80)
    cur.bind('<Button>', noteClicked)

for i in range(2):
    btnUp.append(Tk.Button(frame, bg='white', fg='black', bd=0))
    cur = btnUp[-1]
    cur.place(x=167.5+i*10, y=40, width=10, height=80)
    cur.bind('<Button>', noteClicked)

for i in range(1):
    btnUp.append(Tk.Button(frame, bg='white', fg='black', bd=0))
    cur = btnUp[-1]
    cur.place(x=247.5+i*20, y=40, width=2.5, height=80)
    cur.bind('<Button>', noteClicked)

    btnUp.append(Tk.Button(frame, bg='black', fg='white'))
    cur = btnUp[-1]
    cur.place(x=250+i*20, y=40, width=15, height=80)
    cur.bind('<Button>', noteClicked)

    btnUp.append(Tk.Button(frame, bg='white', fg='black', bd=0))
    cur = btnUp[-1]
    cur.place(x=265+i*20, y=40, width=2.5, height=80)
    cur.bind('<Button>', noteClicked)

btnUp.append(Tk.Button(frame, bg='white', fg='black', bd=0))
cur = btnUp[-1]
cur.place(x=267.5, y=40, width=12, height=80)
cur.bind('<Button>', noteClicked)

while CONTINUE:
    root.update()
    mode = m.get()


    if mode == 0:

        if KEYPRESS0 and CONTINUE:
            # Some key (not 'q') was pressed
            x0[0] = 10000.0

        if KEYPRESS1 and CONTINUE:
            # Some key (not 'q') was pressed
            x1[0] = 10000.0

        if KEYPRESS2 and CONTINUE:
            # Some key (not 'q') was pressed
            x2[0] = 10000.0

        if KEYPRESS3 and CONTINUE:
            # Some key (not 'q') was pressed
            x3[0] = 10000.0

        if KEYPRESS4 and CONTINUE:
            # Some key (not 'q') was pressed
            x4[0] = 10000.0

        if KEYPRESS5 and CONTINUE:
            # Some key (not 'q') was pressed
            x5[0] = 10000.0

        if KEYPRESS6 and CONTINUE:
            # Some key (not 'q') was pressed
            x6[0] = 10000.0

        if KEYPRESS7 and CONTINUE:
            # Some key (not 'q') was pressed
            x7[0] = 10000.0

        if KEYPRESS8 and CONTINUE:
            # Some key (not 'q') was pressed
            x8[0] = 10000.0

        if KEYPRESS9 and CONTINUE:
            # Some key (not 'q') was pressed
            x9[0] = 10000.0

        if KEYPRESS10 and CONTINUE:
            # Some key (not 'q') was pressed
            x10[0] = 10000.0

        if KEYPRESS11 and CONTINUE:
            # Some key (not 'q') was pressed
            x11[0] = 10000.0

        [y0, states0] = signal.lfilter(b0, a0, x0, zi=states0)
        [y1, states1] = signal.lfilter(b1, a1, x1, zi=states1)
        [y2, states2] = signal.lfilter(b2, a2, x2, zi=states2)
        [y3, states3] = signal.lfilter(b3, a3, x3, zi=states3)
        [y4, states4] = signal.lfilter(b4, a4, x4, zi=states4)
        [y5, states5] = signal.lfilter(b5, a5, x5, zi=states5)
        [y6, states6] = signal.lfilter(b6, a6, x6, zi=states6)
        [y7, states7] = signal.lfilter(b7, a7, x7, zi=states7)
        [y8, states8] = signal.lfilter(b8, a8, x8, zi=states8)
        [y9, states9] = signal.lfilter(b9, a9, x9, zi=states9)
        [y10, states10] = signal.lfilter(b10, a10, x10, zi=states10)
        [y11, states11] = signal.lfilter(b11, a11, x11, zi=states11)

        x0[0] = 0.0
        x1[0] = 0.0
        x2[0] = 0.0
        x3[0] = 0.0
        x4[0] = 0.0
        x5[0] = 0.0
        x6[0] = 0.0
        x7[0] = 0.0
        x8[0] = 0.0
        x9[0] = 0.0
        x10[0] = 0.0
        x11[0] = 0.0

        KEYPRESS0 = False
        KEYPRESS1 = False
        KEYPRESS2 = False
        KEYPRESS3 = False
        KEYPRESS4 = False
        KEYPRESS5 = False
        KEYPRESS6 = False
        KEYPRESS7 = False
        KEYPRESS8 = False
        KEYPRESS9 = False
        KEYPRESS10 = False
        KEYPRESS11 = False

        y0 = np.clip(y0.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
        y1 = np.clip(y1.astype(int), -MAXVALUE, MAXVALUE)  # Clipping
        y2 = np.clip(y2.astype(int), -MAXVALUE, MAXVALUE)  # Clipping
        y3 = np.clip(y3.astype(int), -MAXVALUE, MAXVALUE)  # Clipping
        y4 = np.clip(y4.astype(int), -MAXVALUE, MAXVALUE)  # Clipping
        y5 = np.clip(y5.astype(int), -MAXVALUE, MAXVALUE)  # Clipping
        y6 = np.clip(y6.astype(int), -MAXVALUE, MAXVALUE)  # Clipping
        y7 = np.clip(y7.astype(int), -MAXVALUE, MAXVALUE)  # Clipping
        y8 = np.clip(y8.astype(int), -MAXVALUE, MAXVALUE)  # Clipping
        y9 = np.clip(y9.astype(int), -MAXVALUE, MAXVALUE)  # Clipping
        y10 = np.clip(y10.astype(int), -MAXVALUE, MAXVALUE)  # Clipping
        y11 = np.clip(y11.astype(int), -MAXVALUE, MAXVALUE)  # Clipping

        total = y0 + y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8 + y9 + y10 + y11


        binary_data = struct.pack('h' * BLOCKLEN, *total);    # Convert to binary binary data
        stream.write(binary_data, BLOCKLEN)               # Write binary binary data to audio output

    elif mode == 1:

        for i in range(0, BLOCKLEN):

            if KEYPRESS0 and CONTINUE:
                # Some key (not 'q') was pressed
                g1 = G

            if KEYPRESS1 and CONTINUE:
                # Some key (not 'q') was pressed
                g2 = G

            if KEYPRESS2 and CONTINUE:
                # Some key (not 'q') was pressed
                g3 = G

            if KEYPRESS3 and CONTINUE:
                # Some key (not 'q') was pressed
                g4 = G

            if KEYPRESS4 and CONTINUE:
                # Some key (not 'q') was pressed
                g5 = G

            if KEYPRESS5 and CONTINUE:
                # Some key (not 'q') was pressed
                g6 = G

            if KEYPRESS6 and CONTINUE:
                # Some key (not 'q') was pressed
                g7 = G

            if KEYPRESS7 and CONTINUE:
                # Some key (not 'q') was pressed
                g8 = G

            if KEYPRESS8 and CONTINUE:
                # Some key (not 'q') was pressed
                g9 = G

            if KEYPRESS9 and CONTINUE:
                # Some key (not 'q') was pressed
                g10 = G

            if KEYPRESS10 and CONTINUE:
                # Some key (not 'q') was pressed
                g11 = G

            if KEYPRESS11 and CONTINUE:
                # Some key (not 'q') was pressed
                g12 = G

            # y(n) = x(n) + K/2 y(n-N) + K/2 y(n-N-1)
            y1 = g1 + K/2 * buffer1[kr1] + K/2 * buffer1[kr1-1]
            y2 = g2 + K / 2 * buffer2[kr2] + K / 2 * buffer2[kr2 - 1]
            y3 = g3 + K / 2 * buffer3[kr3] + K / 2 * buffer3[kr3 - 1]
            y4 = g4 + K / 2 * buffer4[kr4] + K / 2 * buffer4[kr4 - 1]
            y5 = g5 + K / 2 * buffer5[kr5] + K / 2 * buffer5[kr5 - 1]
            y6 = g6 + K / 2 * buffer6[kr6] + K / 2 * buffer6[kr6 - 1]
            y7 = g7 + K / 2 * buffer7[kr7] + K / 2 * buffer7[kr7 - 1]
            y8 = g8 + K / 2 * buffer8[kr8] + K / 2 * buffer8[kr8 - 1]
            y9 = g9 + K / 2 * buffer9[kr9] + K / 2 * buffer9[kr9 - 1]
            y10 = g10 + K / 2 * buffer10[kr10] + K / 2 * buffer10[kr10 - 1]
            y11 = g11 + K / 2 * buffer11[kr11] + K / 2 * buffer11[kr11 - 1]
            y12 = g12 + K / 2 * buffer12[kr12] + K / 2 * buffer12[kr12 - 1]

            buffer1[kw1] = y1
            buffer2[kw2] = y2
            buffer3[kw3] = y3
            buffer4[kw4] = y4
            buffer5[kw5] = y5
            buffer6[kw6] = y6
            buffer7[kw7] = y7
            buffer8[kw8] = y8
            buffer9[kw9] = y9
            buffer10[kw10] = y10
            buffer11[kw11] = y11
            buffer12[kw12] = y12

            kr1 = kr1 + 1
            if kr1 >= BUFFER_LEN1:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kr1 = 0

            kr2 = kr2 + 1
            if kr2 >= BUFFER_LEN2:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kr2 = 0

            kr3 = kr3 + 1
            if kr3 >= BUFFER_LEN3:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kr3 = 0

            kr4 = kr4 + 1
            if kr4 >= BUFFER_LEN4:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kr4 = 0

            kr5 = kr5 + 1
            if kr5 >= BUFFER_LEN5:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kr5 = 0

            kr6 = kr6 + 1
            if kr6 >= BUFFER_LEN6:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kr6 = 0

            kr7 = kr7 + 1
            if kr7 >= BUFFER_LEN7:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kr7 = 0

            kr8 = kr8 + 1
            if kr8 >= BUFFER_LEN8:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kr8 = 0

            kr9 = kr9 + 1
            if kr9 >= BUFFER_LEN9:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kr9 = 0

            kr10 = kr10 + 1
            if kr10 >= BUFFER_LEN10:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kr10 = 0

            kr11 = kr11 + 1
            if kr11 >= BUFFER_LEN11:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kr11 = 0

            kr12 = kr12 + 1
            if kr12 >= BUFFER_LEN12:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kr12 = 0

            kw1 = kw1 + 1
            if kw1 >= BUFFER_LEN1:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kw1 = 0

            kw2 = kw2 + 1
            if kw2 >= BUFFER_LEN2:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kw2 = 0

            kw3 = kw3 + 1
            if kw3 >= BUFFER_LEN3:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kw3 = 0

            kw4 = kw4 + 1
            if kw4 >= BUFFER_LEN4:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kw4 = 0

            kw5 = kw5 + 1
            if kw5 >= BUFFER_LEN5:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kw5 = 0

            kw6 = kw6 + 1
            if kw6 >= BUFFER_LEN6:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kw6 = 0

            kw7 = kw7 + 1
            if kw7 >= BUFFER_LEN7:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kw7 = 0

            kw8 = kw8 + 1
            if kw8 >= BUFFER_LEN8:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kw8 = 0

            kw9 = kw9 + 1
            if kw9 >= BUFFER_LEN9:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kw9 = 0

            kw10 = kw10 + 1
            if kw10 >= BUFFER_LEN10:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kw10 = 0

            kw11 = kw11 + 1
            if kw11 >= BUFFER_LEN11:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kw11 = 0

            kw12 = kw12 + 1
            if kw12 >= BUFFER_LEN12:
                # The index has reached the end of the buffer. Circle the index back to the front.
                kw12 = 0

            KEYPRESS0 = False
            KEYPRESS1 = False
            KEYPRESS2 = False
            KEYPRESS3 = False
            KEYPRESS4 = False
            KEYPRESS5 = False
            KEYPRESS6 = False
            KEYPRESS7 = False
            KEYPRESS8 = False
            KEYPRESS9 = False
            KEYPRESS10 = False
            KEYPRESS11 = False


            y1 = np.clip(y1, -MAXVALUE, MAXVALUE)  # Clipping
            y2 = np.clip(y2, -MAXVALUE, MAXVALUE)  # Clipping
            y3 = np.clip(y3, -MAXVALUE, MAXVALUE)  # Clipping
            y4 = np.clip(y4, -MAXVALUE, MAXVALUE)  # Clipping
            y5 = np.clip(y5, -MAXVALUE, MAXVALUE)  # Clipping
            y6 = np.clip(y6, -MAXVALUE, MAXVALUE)  # Clipping
            y7 = np.clip(y7, -MAXVALUE, MAXVALUE)  # Clipping
            y8 = np.clip(y8, -MAXVALUE, MAXVALUE)  # Clipping
            y9 = np.clip(y9, -MAXVALUE, MAXVALUE)  # Clipping
            y10 = np.clip(y10, -MAXVALUE, MAXVALUE)  # Clipping
            y11 = np.clip(y11, -MAXVALUE, MAXVALUE)  # Clipping
            y12 = np.clip(y12, -MAXVALUE, MAXVALUE)  # Clipping

            total = y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8 + y9 + y10 + y11 + y12
            # print(type(total))


            binary_data = struct.pack('h', int(total))    # Convert to binary binary data
            stream.write(binary_data)               # Write binary binary data to audio output

            g1 = 0
            g2 = 0
            g3 = 0
            g4 = 0
            g5 = 0
            g6 = 0
            g7 = 0
            g8 = 0
            g9 = 0
            g10 = 0
            g11 = 0
            g12 = 0


print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()




# # ### demo 20
# #
# #
# import pyaudio
# import wave
# import struct
# from random import normalvariate
# import numpy as np
#
#
# RATE     = 8000
# WIDTH    = 2
# CHANNELS = 1
# duration = 2
#
# MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)
#
# output_wavfile = 'demo20.wav'
# output_wf = wave.open(output_wavfile, 'w')
# output_wf.setframerate(RATE)
# output_wf.setsampwidth(WIDTH)
# output_wf.setnchannels(CHANNELS)
#
# K = 0.93
# N = 60
#
# a = list(np.zeros(N-1))
# a.insert(0,1)
# a.append(-K/2)
# a.append(-K/2)
# b = 1
#
# G = 10000
#
# x = [G*normalvariate(0,1) for i in range(N)]
# xzeros = list(np.zeros(int(duration*RATE)))
# x.extend(xzeros)
#
# # num_samples = duration*RATE
# num_samples = len(x)
#
#
# BUFFER_LEN = N+1   # N+1 is kept because we want max delay of N+1 samples
# buffer = BUFFER_LEN * [0]
#
#
# p = pyaudio.PyAudio()
# stream = p.open(
#     format      = pyaudio.paInt16,
#     channels    = CHANNELS,
#     rate        = RATE,
#     input       = False,
#     output      = True )
#
# k = 0
#
#
# print("Started...")
#
# for i in range(num_samples):
#
#     # Convert string to number
#     x0 = x[i]
#
#     if(k == N):
#         y0 = b * x0 - a[N] * buffer[k] - a[N+1] * buffer[0]
#     else:
#         y0 = b * x0 - a[N] * buffer[k] - a[N+1] * buffer[k+1]
#
#     # Update buffer
#     buffer[k] = y0
#
#     # Increment buffer index
#     k = k + 1
#     if k >= BUFFER_LEN:
#         # The index has reached the end of the buffer. Circle the index back to the front.
#         k = 0
#
#     y0 = np.clip(y0, -MAXVALUE, MAXVALUE)     # Clipping
#     output_string = struct.pack('h', int(y0))
#
#     stream.write(output_string)
#
#     output_wf.writeframes(output_string)
#
# print("...Finished")
#
# stream.stop_stream()
# stream.close()
# output_wf.close()
# p.terminate()