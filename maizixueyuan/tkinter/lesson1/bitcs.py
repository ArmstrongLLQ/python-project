__author__ = 'Armstrong'
from tkinter import *
from tkinter import ttk
import pymysql

class DataClass:
	def __init__(self):
		self.conn = pymysql.connect("172.16.155.11", "doaj", "Doa123!@#j", "doaj", charset="utf8")
		# 使用cursor()方法获取操作游标
		self.cursor = self.conn.cursor()

	def getData(self, offset, limit):
		sql = "select id, title, abstract, year, term_l1 from doaj_data limit %d, %d" % (offset, limit)
		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			return results
		except Exception as e:
			print(e)
			self.conn.rollback()
		self.cursor.close()
		self.conn.close()

class MainWindow:
	def __init__(self):
		self.root = Tk()
		self.root.title('信息采集系统')

		# 总体布局
		self.frame_title = Frame(width=800, height=100)
		self.frame_content = Frame(width=400, height=500)
		self.frame_bottom = Frame(width=800, height=200)

		# 菜单栏
		# create menu
		self.menubar = Menu(self.root)
		self.root.config(menu=self.menubar)

		# filemenu
		self.filemenu = Menu(self.menubar)
		self.filemenu.add_command(label='新建', accelerator='Ctrl + N', command=self.new)
		self.filemenu.add_command(label='打开', accelerator='Ctrl + O', command=self.openfile)
		self.filemenu.add_command(label='保存', accelerator='Ctrl + S', command=self.save)
		self.filemenu.add_command(label='另存为', accelerator='Ctrl + Shift + S', command=self.saveas)
		self.menubar.add_cascade(label='文件', menu=self.filemenu)

		# 标题显示部分
		self.title_label = Label(self.frame_title, text='信息采集系统', font='Arial 16 bold')
		self.title_label.pack()

		# 数据表格显示部分
		self.tree = ttk.Treeview(self.frame_content, show='headings', height=18, columns=('id', 'title', 'abstract', 'year', 'term_l1'))
		self.vbar = ttk.Scrollbar(self.frame_content, orient=VERTICAL, command=self.tree.yview)
		self.tree.configure(yscrollcommand=self.vbar.set)

		self.tree.column('id', width=100)
		self.tree.column('title', width=200)
		self.tree.column('abstract', width=300)
		self.tree.column('year', width=100)
		self.tree.column('term_l1', width=100)

		self.tree.heading('id', text='id')
		self.tree.heading('title', text='title')
		self.tree.heading('abstract', text='abstract')
		self.tree.heading('year', text='year')
		self.tree.heading('term_l1', text='term_l1')

		self.page = 1
		self.limit = 20

		self.get_table_list()
		# tree.insert("",1,text="line1" ,values=("1","2","3"))
		# tree.insert("",2,text="line1" ,values=("1","2","3"))
		# tree.insert("",3,text="line1" ,values=("1","2","3"))

		self.tree.grid(row=0, column=0, sticky=NSEW)
		self.vbar.grid(row=0, column=1, sticky=NS)

		# 底部翻页部分
		self.button_prev = Button(self.frame_bottom, text='上一页', command=self.prev_page)
		self.button_next = Button(self.frame_bottom, text='下一页', command=self.next_page)

		self.button_prev.grid(row=0, column=0)
		self.button_next.grid(row=0, column=1)

		self.frame_title.grid(row=0, column=0, padx=4, pady=4)
		self.frame_content.grid(row=1, column=0, padx=8, pady=8)
		self.frame_bottom.grid(row=2, column=0, padx=4, pady=4)
		self.root.mainloop()

	def get_table_list(self):
		self.offset = (self.page - 1) * self.limit
		# 删除原节点
		for _ in map(self.tree.delete, self.tree.get_children("")):
			pass
		data_class = DataClass()
		data_list = data_class.getData(self.offset, self.limit)
		for data, i in zip(data_list, range(self.limit)):
			self.tree.insert("", i + 1, values=(data[0], data[1], data[2], data[3], data[4]))

	def prev_page(self):
		if self.page > 1:
			self.page = self.page - 1
		else:
			self.page = 1
		self.get_table_list()

	def next_page(self):
		self.page = self.page + 1
		self.get_table_list()

	def new(self):
		pass

	def openfile(self):
		pass

	def save(self):
		pass

	def saveas(self):
		pass

if __name__ == '__main__':
	MainWindow()



