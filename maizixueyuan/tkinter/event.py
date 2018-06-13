from tkinter import *

root = Tk()

def buttonClick():
    print('button click')

button = Button(text = 'hello', command = buttonClick)

button.pack()

def callback(event):
    frame.focus_set()
    print('click at:', event.x, event.y)

def key(event):
    print('pressed:', repr(event.char))

frame = Frame(root, width = 100, height = 100)
frame.bind('<Button-1>', callback)
frame.bind('<Key>', key)
frame.pack()

root.mainloop()