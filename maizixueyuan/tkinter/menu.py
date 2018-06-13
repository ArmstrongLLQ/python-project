__author__ = 'Armstrong'


from tkinter import *

def callback():
    print('call the menu')

root = Tk()

# 创建一个menu实例，然后将menu贴到root上
menu = Menu(root)
root.config(menu = menu)

# 创建一个子菜单filemenu实例
filemenu = Menu(menu)

# 将filemenu贴到menu上
menu.add_cascade(label = 'file', menu = filemenu)

# 在filemenu中添加命令
filemenu.add_command(label = 'new file', command = callback)
filemenu.add_command(label = 'open file', command = callback)

# 在filemenu中添加分割线
filemenu.add_separator()

filemenu.add_command(label = 'exit', command = callback)

root.mainloop()