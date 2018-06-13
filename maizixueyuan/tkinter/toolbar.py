__author__ = 'Armstrong'

from tkinter import *

root = Tk()

def callback():
    print("clicked tool bar button ")

# 使用Frame来实现toolbar
toolbar = Frame(root)

# 增加一个按钮new
b = Button(toolbar,text='new',width=6,command=callback)
# 设置Button显示的位置
b.pack(side=LEFT,padx=2,pady=2)

c = Button(toolbar,text='open',width=6,command=callback)
c.pack(side=LEFT,padx=2,pady=2)

toolbar.pack(side=TOP,fill=X)
root.mainloop()

