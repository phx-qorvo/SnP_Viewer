# Modules used
from Tkinter import *


class UserLimits(Frame):
    # called inside init so, it runs right away
    def createwidgets(self, filetype):
        # Buttons
        self.QUIT["text"] = "GO"
        self.QUIT["bg"] = "Green"
        self.QUIT["command"] = self.quit
        self.QUIT.grid(row=0, column=0)
        self.w.grid(row=1, column=3)
        self.x.grid(row=1, column=4)
        self.background.grid(row=0, column=3)

        # check buttons
        rows = 2
        counter = 0
        for j in range(0, filetype):
            for i in range(0, filetype):
                self.plot.append(BooleanVar())
                self.graph_type.append(BooleanVar())

                self.portbox = Checkbutton(self, variable=self.plot[counter],
                                           state=ACTIVE,
                                           text='S' + str(j + 1) + str(i + 1))
                self.portbox.grid(row=rows, column=3)

                self.dBbox = Radiobutton(self, text='dB Plot',
                                         variable=self.graph_type[counter],
                                         value=True)
                self.dBbox.grid(row=rows, column=4)
                self.smithbox = Radiobutton(self, text='Smith Plot',
                                            variable=self.graph_type[counter],
                                            value=False)
                self.smithbox.grid(row=rows, column=5)

                rows += 1
                counter += 1


    def __init__(self, filetype, master=None):
        Frame.__init__(self, master)
        master.title('Plot Selection')
        self.writing = Text(self)
        self.x = Label(self, text='Graph Type')
        self.w = Label(self, text='Ports')
        self.QUIT = Button(self)
        self.plot = []
        self.markers = [[] for i in range(filetype * filetype)]
        self.graph_type = []
        self.grid()
        self.white_background = BooleanVar()
        self.background = Checkbutton(self, variable=self.white_background,
                                      state=ACTIVE,
                                      text='White Backgound?')
        self.createwidgets(filetype)



