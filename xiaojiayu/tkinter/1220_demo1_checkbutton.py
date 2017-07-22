from tkinter import *

root = Tk()

v = IntVar()

check_button = Checkbutton(root, text = 'check', variable = v)
check_button.pack()

label = Label(root, textvariable = v)
label.pack()

mainloop()
