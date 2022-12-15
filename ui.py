import tkinter as Tk

global a1

def updateUI(root):

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


    # flag = True
    #
    # while flag:
    #     root.update()


