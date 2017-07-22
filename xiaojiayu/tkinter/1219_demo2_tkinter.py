from tkinter import *

root = Tk()

text_label = Label(root, text = 'wuwuwuwu', justify = LEFT, padx = 10, font = ('', 20))
text_label.pack(side = LEFT)

photo = PhotoImage(file = '3.gif')
img_label = Label(root, image = photo)
img_label.pack(side = RIGHT)

mainloop()
