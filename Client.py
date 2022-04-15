# import necessary library for project
from tkinter import messagebox
import tkinter as tk
from functools import partial
from Server import Threading_socket

#  create class with name CaroGame
class CaroGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Caro Tkinter - codelearn.io")
        self.Buts = {}
        self.memory = []
        self.Threading_socket = Threading_socket(self)
        # print(self.Threading_socket.name)



    def showFrame(self):
        frame1 = tk.Frame(self)
        frame1.pack()
        frame2 = tk.Frame(self)
        frame2.pack()
        # undo button
        Undo = tk.Button(frame1, text="Undo", width=10, 
                         command=partial(self.Undo, synchronized=True))
        Undo.grid(row=0, column=0, padx=30)

        tk.Label(frame1, text="IP", pady=4).grid(row=0, column=1)
        inputIp = tk.Entry(frame1, width=20)  # ip address receiving frame
        inputIp.grid(row=0, column=2, padx=5)
        connectBT = tk.Button(frame1, text="Connect", width=10,
                              command=lambda: self.Threading_socket.clientAction(inputIp.get()))
        connectBT.grid(row=0, column=3, padx=3)

        makeHostBT = tk.Button(frame1, text="MakeHost", width=10,  # button create host
                               command=lambda: self.Threading_socket.serverAction())
        makeHostBT.grid(row=0, column=4, padx=30)
        # Taoj bangr Ox, Oy
        for x in range(Ox):   
            for y in range(Oy):
                self.Buts[x, y] = tk.Button(frame2, font=('arial', 15, 'bold'), height=1, width=2,
                                            borderwidth=2, command=partial(self.ButtonHandle, x=x, y=y))
                self.Buts[x, y].grid(row=x, column=y)

    # mange button function 
    def ButtonHandle(self, x, y):
        if self.Buts[x, y]['text'] == "":
            if self.memory.count([x, y]) == 0:
                self.memory.append([x, y])
            if len(self.memory) % 2 == 1:
                self.Buts[x, y]['text'] = 'O'
                self.Threading_socket.sendData("{}|{}|{}|".format("hit", x, y))
                if(self.checkWin(x, y, "O")):
                    self.notification("Winner", "O")
                    self.newGame()
            else:
                print(self.Threading_socket.name)
                self.Buts[x, y]['text'] = 'X'
                self.Threading_socket.sendData("{}|{}|{}|".format("hit", x, y))
                if(self.checkWin(x, y, "X")):
                    self.notification("Winner", "X")
                    self.newGame()

    def notification(self, title, msg):
        messagebox.showinfo(str(title), str(msg))

    def checkWin(self, x, y, XO):
        count = 0
        i, j = x, y
        while(j < Ox and self.Buts[i, j]["text"] == XO):
            count += 1
            j += 1
        j = y
        while(j >= 0 and self.Buts[i, j]["text"] == XO):
            count += 1
            j -= 1
        if count >= 6:
            return True
        # check cột
        count = 0
        i, j = x, y
        while(i < Oy and self.Buts[i, j]["text"] == XO):
            count += 1
            i += 1
        i = x
        while(i >= 0 and self.Buts[i, j]["text"] == XO):
            count += 1
            i -= 1
        if count >= 6:
            return True
        # check cheo phai
        count = 0
        i, j = x, y
        while(i >= 0 and j < Ox and self.Buts[i, j]["text"] == XO):
            count += 1
            i -= 1
            j += 1
        i, j = x, y
        while(i <= Oy and j >= 0 and self.Buts[i, j]["text"] == XO):
            count += 1
            i += 1
            j -= 1
        if count >= 6:
            return True
        # check cheo trai
        count = 0
        i, j = x, y
        while(i < Ox and j < Oy and self.Buts[i, j]["text"] == XO):
            count += 1
            i += 1
            j += 1
        i, j = x, y
        while(i >= 0 and j >= 0 and self.Buts[i, j]["text"] == XO):
            count += 1
            i -= 1
            j -= 1
        if count >= 6:
            return True
        return False

    def Undo(self, synchronized):
        if(len(self.memory) > 0):
            x = self.memory[len(self.memory) - 1][0]
            y = self.memory[len(self.memory) - 1][1]
            # print(x,y)
            self.Buts[x, y]['text'] = ""
            self.memory.pop()
            if synchronized == True:
                self.Threading_socket.sendData("{}|".format("Undo"))
            print(self.memory)
        else:
            print("No character")
    # restare game 
    def newGame(self):
        for x in range(Ox):
            for y in range(Oy):
                self.Buts[x, y]["text"] = ""

if __name__ == "__main__":
    Ox = 20  # number of axes  X
    Oy = 20 # number of axes Y
    window = CaroGame()
    window.showFrame()
    window.mainloop()