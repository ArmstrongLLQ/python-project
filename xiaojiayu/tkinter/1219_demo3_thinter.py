from tkinter import *

root = Tk()

photo = PhotoImage(file = '3.gif')
label = Label(root,
              text = 'weisha buneng shuru zhong wen a ',
              justify = LEFT,
              image = photo,
              compound = CENTER,
              font = ('', 40),
              fg = 'blue')

label.pack()

mainloop()
