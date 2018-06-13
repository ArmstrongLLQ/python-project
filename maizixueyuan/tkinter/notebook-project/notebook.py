__author__ = 'Armstrong'

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import os

filename = ''

def new():
    global filename
    root.title('未命名文件')
    filename = None
    textPad.delete(1.0, END)    #1.0代表的时第一行第零列，文本的初始位置

#要用到filedialog模块
def openfile():
    global filename
    filename = askopenfilename(defaultextension = '.txt')
    if filename == '':
        filename = None
    else:
        root.title('FileName:' + os.path.basename(filename))
        textPad.delete(1.0, END)
        f = open(filename, 'r')
        textPad.insert(1.0, f.read())
        f.close()

def save():
    global filename
    try:
        f = open(filename,'w')
        msg = textPad.get(1.0,END)
        f.write(msg)
        f.close()
    except:
        saveas()


def saveas():
    f = asksaveasfilename(initialfile= '未命名.txt', defaultextension='.txt')
    global filename
    filename = f
    fh = open(f,'w')
    msg = textPad.get(1.0,END)
    fh.write(msg)
    fh.close()
    root.title('FileName:'+os.path.basename(f))

def cut():
    textPad.event_generate('<<Cut>>')

def copy():
    textPad.event_generate('<<Copy>>')

def paste():
    textPad.event_generate('<<Paste>>')

def redo():
    textPad.event_generate('<<Redo>>')

def undo():
    textPad.event_generate('<<Undo>>')

def selectAll():
    textPad.tag_add('sel','1.0',END)

def search():
    topsearch = Toplevel(root)
    topsearch.geometry('300x30+200+250')
    label1 = Label(topsearch,text='Find')
    label1.grid(row=0, column=0,padx=5)
    entry1 = Entry(topsearch,width=20)
    entry1.grid(row=0, column=1,padx=5)
    button1 = Button(topsearch,text='查找')
    button1.grid(row=0, column=2)

#点击时弹出新的对话框，要用到messagebox模块，然后使用showinfo方法
def author():
    showinfo('作者信息', 'Armstrong!')

def about():
    showinfo('版权信息', '无')


root = Tk()
root.title('Armstrong Note')
#设置窗口的大小500*500和位置（100，100）
#注意，这个里面的参数500*500的乘号不能使用*，
root.geometry("500x500+100+100")

#create menu
menubar = Menu(root)
root.config(menu = menubar)

#filemenu
filemenu = Menu(menubar)
filemenu.add_command(label='新建', accelerator='Ctrl + N', command= new)
filemenu.add_command(label='打开', accelerator='Ctrl + O',command = openfile)
filemenu.add_command(label='保存', accelerator='Ctrl + S', command=save)
filemenu.add_command(label='另存为', accelerator='Ctrl + Shift + S',command=saveas)
menubar.add_cascade(label='文件',menu=filemenu)

#editmenu
editmenu = Menu(menubar)
editmenu.add_command(label='撤销', accelerator='Ctrl + Z', command=undo)
editmenu.add_command(label='重做', accelerator='Ctrl + y', command=redo)
editmenu.add_separator()
editmenu.add_command(label = "剪切",accelerator = "Ctrl + X",command=cut)
editmenu.add_command(label = "复制",accelerator = "Ctrl + C", command=copy)
editmenu.add_command(label = "粘贴",accelerator = "Ctrl + V", command= paste)
editmenu.add_separator()
editmenu.add_command(label = "查找",accelerator = "Ctrl + F", command=search)
editmenu.add_command(label = "全选",accelerator = "Ctrl + A", command= selectAll)
menubar.add_cascade(label = "编辑",menu = editmenu)

#aboutmenu
aboutmenu = Menu(menubar)
aboutmenu.add_command(label = "作者", command=author)
aboutmenu.add_command(label = "版权", command = about)
menubar.add_cascade(label = "关于",menu=aboutmenu)

#toolbar--root的一个Frame，Frame里面有两个Button
toolbar = Frame(root, height = 25, bg = 'light sea green')
shortButton = Button(toolbar, text = '打开', command = openfile)
shortButton.pack(side = LEFT, padx = 5, pady = 5)

shortButton = Button(toolbar, text = '保存', command = save)
shortButton.pack(side = LEFT)
toolbar.pack(expand = NO, fill = X)

#status bar
#relief浮雕效果，anchor对齐，W左对齐
status = Label(root, text = 'Ln20', bd = 1, relief = SUNKEN, anchor = W)
status.pack(side = BOTTOM, fill = X)

#linenumber&text
lnlabel = Label(root, width = 2, bg = 'antique white')
lnlabel.pack(side = LEFT, fill = Y)

textPad = Text(root, undo = True)
textPad.pack(expand = YES, fill = BOTH)

#滚动条，嵌入textPad里面
scroll = Scrollbar(textPad)
textPad.config(yscrollcommand = scroll.set)
scroll.config(command = textPad.yview)
scroll.pack(side = RIGHT, fill = Y)

root.mainloop()