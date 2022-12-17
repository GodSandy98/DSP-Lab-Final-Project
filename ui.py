import tkinter as Tk
from tkinter import ttk
import tkinter.font as font
from threading import Thread
import scipy.io.wavfile as wavfile
import numpy as np
# from tkmacosx import Button



class Interface():

    def __init__(self):
        self.KEYPRESS = [False for i in range(20)]
        self.CONTINUE = True
        self.RECORDING = False
        self.IR_PATH = "./IRs/"
        self.IR_NAME = "Church"
        self.IR_FULLPATH = "./IRs/Church.wav"

    def buttonFlash(self, button):
        button.flash()

     # KeyPressed function
    def my_function(self, event):
        print('You pressed ' + event.char)

        if event.char == 'x':
            print('Good Bye')
            self.CONTINUE = False

        keys = ['q', '2', 'w', '3', 'e', 'r', '5', 't', '6', 'y', '7', 'u', 'i', '9', 'o', '0', 'p', '[', '=', ']']

        for i in range(20):
            if event.char == keys[i]:
                self.KEYPRESS[i] = True


     # ButtonPressed function
    def buttonPressed(self, event):
        # print(event.widget["text"])
        buttons = [
            'C1', 'c1', 'D1', 'd1', 'E1', 'F1', 'f1', 'G1', 'g1', 'A1', 'a1',
            'B1', 'C2', 'c2', 'D2', 'd2', 'E2', 'F2', 'f2', 'G2'
                   ]
        for i in range(20):
            if event.widget['text'] == buttons[i]:
                self.KEYPRESS[i] = True
     
     # Recording Btn clicked
        
     
     # Add record and mix features
    def addRecording(self, root):
        # function for changing the state of recording button
        def recordBtnPressed():
            if self.RECORDING:
                self.RECORDING = False
                recordBtn['bg']='green'
                recordBtn['text']='Start'
            else:
                self.RECORDING = True
                recordBtn['bg']='red'
                recordBtn['text']='Stop'
                
        def mixBtnPressed():
            fs1, IR = wavfile.read(self.IR_FULLPATH)
            IR_sig = IR.astype(np.float32) / 2 ** 15

            fs2, mySound = wavfile.read("./output_original.wav")
            mySound_sig = mySound.astype(np.float32) / 2 ** 15

            output = np.convolve(IR_sig, mySound_sig)
            
            wavfile.write("output_mixed.wav", fs1, output)
            
        def changeSelectedEffect(event):
            self.IR_NAME = effectName.get()
            self.IR_FULLPATH = self.IR_PATH + self.IR_NAME + ".wav"
            print(self.IR_FULLPATH)
        
        frame = Tk.Frame(root, borderwidth=2, width=560, height=80)
        frame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        recordBtn = Tk.Button(frame, bg='green',fg='white', text='Start', command=recordBtnPressed)
        recordBtn.pack(side=Tk.LEFT, fill=Tk.Y, expand=1)
        effectName = Tk.StringVar()
        effectComb = ttk.Combobox(frame, width=20, textvariable=effectName)
        effectComb['values'] = ('Church',
                                'Studio',
                                'University')
        effectComb.pack(side=Tk.LEFT, fill=Tk.Y, expand=1)
        effectComb.current(0)
        effectComb.bind('<<ComboboxSelected>>', changeSelectedEffect)
        mixBtn = Tk.Button(frame, bg='white',fg='black', text='Mix', command=mixBtnPressed)
        mixBtn.pack(side=Tk.LEFT, fill=Tk.Y, expand=1)
        
     # Build UI
    def updateUI(self, root):

        frame = Tk.Frame(root, borderwidth=2, width=320, height=200)
        # frame = Tk.Frame(outFrame, borderwidth=2, width=560, height=250)
        frame.pack(side=Tk.TOP)

        for i in range(12):
            match i:
                case 0:
                    cur = Tk.Button(frame, bg='white', fg='black', text='C1', bd=0)
                case 1:
                    cur = Tk.Button(frame, bg='white', fg='black', text='D1', bd=0)
                case 2:
                    cur = Tk.Button(frame, bg='white', fg='black', text='E1', bd=0)
                case 3:
                    cur = Tk.Button(frame, bg='white', fg='black', text='F1', bd=0)
                case 4:
                    cur = Tk.Button(frame, bg='white', fg='black', text='G1', bd=0)
                case 5:
                    cur = Tk.Button(frame, bg='white', fg='black', text='A1', bd=0)
                case 6:
                    cur = Tk.Button(frame, bg='white', fg='black', text='B1', bd=0)
                case 7:
                    cur = Tk.Button(frame, bg='white', fg='black', text='C2', bd=0)
                case 8:
                    cur = Tk.Button(frame, bg='white', fg='black', text='D2', bd=0)
                case 9:
                    cur = Tk.Button(frame, bg='white', fg='black', text='E2', bd=0)
                case 10:
                    cur = Tk.Button(frame, bg='white', fg='black', text='F2', bd=0)
                case 11:
                    cur = Tk.Button(frame, bg='white', fg='black', text='G2', bd=0)

            cur.place(x=40+i*20, y=120, width=20, height=40)
            cur.bind('<Button>', self.buttonPressed)

        btn = Tk.Button(frame, bg='white', bd=0)
        btn.place(x=40, y=40, width=10, height=80)

        for j in range(2):
            for i in range(2):
                btn = Tk.Button(frame, bg='white', fg='black', bd=0)
                btn.place(x=50+j*137.5 + i * 20, y=40, width=2.5, height=80)

                if j == 0:
                    if i == 0:
                        cur = Tk.Button(frame, bg='black', fg='white', text='c1')
                    elif i == 1:
                        cur = Tk.Button(frame, bg='black', fg='white', text='d1')
                elif j == 1:
                    if i == 0:
                        cur = Tk.Button(frame, bg='black', fg='white', text='c2')
                    elif i == 1:
                        cur = Tk.Button(frame, bg='black', fg='white', text='d2')

                cur.place(x=52.5 + j * 137.5 + i * 20, y=40, width=15, height=80)
                cur.bind('<Button>', self.buttonPressed)

                btn = Tk.Button(frame, bg='white', fg='black', bd=0)
                btn.place(x=67.5+j*137.5 + i * 20, y=40, width=2.5, height=80)


                # for i in range(2):
                btn = Tk.Button(frame, bg='white', fg='black', bd=0)
                btn.place(x=87.5+j*140+i*10, y=40, width=10, height=80)

        for i in range(3):
            btn = Tk.Button(frame, bg='white', fg='black', bd=0)
            btn.place(x=107.5 + i*20, y=40, width=2.5, height=80)


            if i == 0:
                cur = Tk.Button(frame, bg='black', fg='white', text='f1')
            elif i == 1:
                cur = Tk.Button(frame, bg='black', fg='white', text='g1')
            elif i == 2:
                cur = Tk.Button(frame, bg='black', fg='white', text='a1')

            cur.place(x=110 + i * 20, y=40, width=15, height=80)
            cur.bind('<Button>', self.buttonPressed)
            btn = Tk.Button(frame, bg='white', fg='black', bd=0)

            btn.place(x=125 + i*20, y=40, width=2.5, height=80)

        for i in range(2):
            btn = Tk.Button(frame, bg='white', fg='black', bd=0)
            btn.place(x=167.5+i*10, y=40, width=10, height=80)

        for i in range(1):
            btn = Tk.Button(frame, bg='white', fg='black', bd=0)
            btn.place(x=247.5+i*20, y=40, width=2.5, height=80)

            cur = Tk.Button(frame, bg='black', fg='white', text='f2')
            cur.place(x=250+i*20, y=40, width=15, height=80)
            cur.bind('<Button>', self.buttonPressed)

            btn = Tk.Button(frame, bg='white', fg='black', bd=0)
            btn.place(x=265+i*20, y=40, width=2.5, height=80)

        btn = Tk.Button(frame, bg='white', fg='black', bd=0)
        btn.place(x=267.5, y=40, width=12, height=80)