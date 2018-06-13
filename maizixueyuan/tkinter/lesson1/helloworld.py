from tkinter import *

root = Tk() # 根窗体

label = Label(root, text='hello world')
label.config(cursor='gumby', width=80, height=10, fg='green', bg='yellow')
label.pack()

root.mainloop()