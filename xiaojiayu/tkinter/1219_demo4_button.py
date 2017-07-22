from tkinter import *

def CallBack():
    var.set('fdsfdfdsafdsafdsafdsafadsfdsfs')

root = Tk()

frame1 = Frame(root)
frame2 = Frame(root)

var = StringVar()
var.set('dfsafdafdasf')

text_label = Label(frame1, textvariable = var, justify = LEFT)
text_label.pack()

photo = PhotoImage(file = '3.gif')
img_label = Label(frame1, image = photo)
img_label.pack()

button1 = Button(frame2, text = 'wowowo', command = CallBack)
button1.pack()

frame1.pack()
frame2.pack()

mainloop()
