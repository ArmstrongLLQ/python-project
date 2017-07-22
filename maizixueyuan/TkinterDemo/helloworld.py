__author__ = 'Armstrong'

from tkinter import *

# 创建根窗体实例
root = Tk()

# 在根窗体上添加一个Label
label = Label(root, text = 'hello world')
label.config(width = 80, height = 10, fg = 'yellow', bg = 'white')
label.config(cursor = 'gumby')
label.pack()

root.mainloop()