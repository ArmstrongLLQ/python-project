# -*- coding: utf-8 -*-
'''
窗口程序，用于处理eisc_data文献数据的清洗和入库
'''
__author__ = 'Armstrong'

from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msgb
from BASE import excelTableByIndex, fileExist, updateData, updateS_source
from BASE import insertErrorData, changeDocidById, insertNewDataToS_data, excelDataChange

class MainWindow:
	def __init__(self):
		self.root = Tk()
		self.root.title('eisc_data处理')

		# 总体布局
		self.frame_title = ttk.Frame(width=700, height=100)
		self.frame_content = ttk.Frame(width=700, height=500)
		self.frame_value = ttk.Frame(width=700, height=300)
		self.frame_bottom = ttk.Frame(width=700, height=100)

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
		self.title_label = ttk.Label(self.frame_title, text='eisc_data处理', font='Arial 16 bold')
		self.title_label.pack()

		# 文件路径参数部分
		self.entry_width = 40
		self.excel_filepath_label = ttk.Label(self.frame_content, text='excel文件路径:').grid(row=0, column=0)
		self.excel_filepath = StringVar()
		self.excel_filepath.set('Z:/ALLPDF/SPIE-FULLTXT/2018005/SPIE会议.xlsx')
		self.excel_filepath_entry = ttk.Entry(self.frame_content, textvariable=self.excel_filepath, width=self.entry_width).grid(row=0, column=1, columnspan=2)

		self.actual_filepath_label = ttk.Label(self.frame_content, text='实际pdf文件路径:').grid(row=1, column=0)
		self.actual_filepath = StringVar()
		self.actual_filepath.set('Z:/ALLPDF/SPIE-FULLTXT/2018005/HY')
		self.actual_filepath_entry = ttk.Entry(self.frame_content, textvariable=self.actual_filepath, width=self.entry_width).grid(row=1, column=1, columnspan=2)

		self.report_type_label = ttk.Label(self.frame_content, text='选择report_type:').grid(row=2, column=0)
		self.report_type = StringVar()
		self.report_type_combobox = ttk.Combobox(self.frame_content, textvariable=self.report_type, width=self.entry_width-2)
		self.report_type_combobox['values'] = ('会议', '期刊', '报告', '标准', '汇编', '论文', '专利', '专著', '参考', '文摘')
		self.report_type_combobox.current(1)
		self.report_type_combobox.grid(row=2, column=1, columnspan=2)

		self.report_name_label = ttk.Label(self.frame_content, text='选择report_name:').grid(row=3, column=0)
		self.report_name = StringVar()
		self.report_name_combobox = ttk.Combobox(self.frame_content, textvariable=self.report_name, width=self.entry_width-2)
		self.report_name_combobox['values'] = ('IEL', 'SPIE', 'AIAA', 'IQPC', 'AD', 'DE', 'PB', 'NASA',
		                                       'DMS', 'JANES', 'ELSEVIER', 'NTIS', 'INSPEC','EI', 'AERO',
		                                       '电子科技文摘库', '硕博论文库', '科技成果库', '综合数据库',
		                                       '预留数据库', '自建库')
		self.report_name_combobox.current(1)
		self.report_name_combobox.grid(row=3, column=1, columnspan=2)

		self.filepath_in_computer_label = ttk.Label(self.frame_content, text='filepath修改参数:').grid(row=4, column=0)
		self.filepath_in_computer = StringVar()
		self.filepath_in_computer.set('/SPIE-FULLTXT/2018005/HY')
		self.filepath_in_computer_entry = ttk.Entry(self.frame_content, textvariable=self.filepath_in_computer, width=self.entry_width).grid(row=4, column=1, columnspan=2)

		# 各功能按键部分
		self.button_width = 22
		self.file_exist_button = ttk.Button(self.frame_content, text='file exist test',
		                                    command=self.mainFileExist, width=self.button_width)
		self.file_exist_button.grid(row=5, column=0)

		self.update_data_button = ttk.Button(self.frame_content, text='update data',
		                                     command=self.mainUpdateData, width=self.button_width)
		self.update_data_button.grid(row=5, column=1)

		self.update_s_source_button = ttk.Button(self.frame_content, text='update s_source',
		                                         command=self.mainUpdateS_source, width=self.button_width)
		self.update_s_source_button.grid(row=5, column=2)

		self.excel_data_change_button = ttk.Button(self.frame_content, text='excel data change',
		                                           command=self.mainExcelDataChange, width=self.button_width)
		self.excel_data_change_button.grid(row=6, column=0)

		self.insert_data_to_s_data_button = ttk.Button(self.frame_content, text='insert data to s_data',
		                                               command=self.mainInsertNewDataToS_data, width=self.button_width)
		self.insert_data_to_s_data_button.grid(row=6, column=1)

		self.insert_error_data_button = ttk.Button(self.frame_content, text='insert error data to s_data',
		                                           command=self.mainInsertErrorData, width=self.button_width)
		self.insert_error_data_button.grid(row=6, column=2)


		self.split_line_label =ttk.Label(self.frame_content,
								text='---------------------------------------------------------------------------------------').grid(row=7,column=0,columnspan=3)

		# 字段对应部分
		self.combobox_width = 12
		self.value_vol_label = ttk.Label(self.frame_value, text='vol:').grid(row=0, column=0)
		self.value_vol = StringVar()
		self.value_vol_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_vol, width=self.combobox_width)
		self.value_vol_combobox['values'] = ('', 'volume', 'Volume', 'MeetingVolume')
		self.value_vol_combobox.current(1)
		self.value_vol_combobox.grid(row=0, column=1)

		self.value_issue_label = ttk.Label(self.frame_value, text='issue:').grid(row=0, column=2)
		self.value_issue = StringVar()
		self.value_issue_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_issue, width=self.combobox_width)
		self.value_issue_combobox['values'] = ('', 'issue', 'Issue', 'ISSUE')
		self.value_issue_combobox.current(1)
		self.value_issue_combobox.grid(row=0, column=3)
		
		self.value_doi_label = ttk.Label(self.frame_value, text='doi:').grid(row=0, column=4)
		self.value_doi = StringVar()
		self.value_doi_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_doi, width=self.combobox_width)
		self.value_doi_combobox['values'] = ('', 'DOI', 'doi')
		self.value_doi_combobox.current(1)
		self.value_doi_combobox.grid(row=0, column=5)

		self.value_year_label = ttk.Label(self.frame_value, text='year:').grid(row=1, column=0)
		self.value_year = StringVar()
		self.value_year_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_year, width=self.combobox_width)
		self.value_year_combobox['values'] = ('', 'year', 'Year', 'YEAR')
		self.value_year_combobox.current(1)
		self.value_year_combobox.grid(row=1, column=1)
		
		self.value_mtitle_label = ttk.Label(self.frame_value, text='mtitle:').grid(row=1, column=2)
		self.value_mtitle = StringVar()
		self.value_mtitle_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_mtitle, width=self.combobox_width)
		self.value_mtitle_combobox['values'] = ('', 'title', 'Title', 'TITLE')
		self.value_mtitle_combobox.current(1)
		self.value_mtitle_combobox.grid(row=1, column=3)

		self.value_authors_label = ttk.Label(self.frame_value, text='authors:').grid(row=1, column=4)
		self.value_authors = StringVar()
		self.value_authors_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_authors, width=self.combobox_width)
		self.value_authors_combobox['values'] = ('', 'author', 'Author', 'authors', 'Authors')
		self.value_authors_combobox.current(1)
		self.value_authors_combobox.grid(row=1, column=5)

		self.value_authorunit_label = ttk.Label(self.frame_value, text='authorunit:').grid(row=2, column=0)
		self.value_authorunit = StringVar()
		self.value_authorunit_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_authorunit, width=self.combobox_width)
		self.value_authorunit_combobox['values'] = ('', 'organ', 'Organ')
		self.value_authorunit_combobox.current(1)
		self.value_authorunit_combobox.grid(row=2, column=1)

		self.value_keyword_label = ttk.Label(self.frame_value, text='keyword:').grid(row=2, column=2)
		self.value_keyword = StringVar()
		self.value_keyword_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_keyword, width=self.combobox_width)
		self.value_keyword_combobox['values'] = ('', 'keyword', 'Keyword')
		self.value_keyword_combobox.current(1)
		self.value_keyword_combobox.grid(row=2, column=3)

		self.value_abstracts_label = ttk.Label(self.frame_value, text='abstracts:').grid(row=2, column=4)
		self.value_abstracts = StringVar()
		self.value_abstracts_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_abstracts, width=self.combobox_width)
		self.value_abstracts_combobox['values'] = ('', 'abstract', 'Abstract')
		self.value_abstracts_combobox.current(1)
		self.value_abstracts_combobox.grid(row=2, column=5)

		self.value_pages_label = ttk.Label(self.frame_value, text='pages:').grid(row=3, column=0)
		self.value_pages = StringVar()
		self.value_pages_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_pages, width=self.combobox_width)
		self.value_pages_combobox['values'] = ('', 'pages', 'Pages', 'page', 'Page')
		self.value_pages_combobox.current(1)
		self.value_pages_combobox.grid(row=3, column=1)
		
		self.value_bepage_label = ttk.Label(self.frame_value, text='bepage:').grid(row=3, column=2)
		self.value_bepage = StringVar()
		self.value_bepage_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_bepage, width=self.combobox_width)
		self.value_bepage_combobox['values'] = ('', 'strpage', 'strPage')
		self.value_bepage_combobox.current(1)
		self.value_bepage_combobox.grid(row=3, column=3)
		
		self.value_filename_label = ttk.Label(self.frame_value, text='filename:').grid(row=3, column=4)
		self.value_filename = StringVar()
		self.value_filename_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_filename, width=self.combobox_width)
		self.value_filename_combobox['values'] = ('', 'FileName', 'filename')
		self.value_filename_combobox.current(1)
		self.value_filename_combobox.grid(row=3, column=5)
		
		self.value_filesize_label = ttk.Label(self.frame_value, text='filesize:').grid(row=4, column=0)
		self.value_filesize = StringVar()
		self.value_filesize_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_filesize, width=self.combobox_width)
		self.value_filesize_combobox['values'] = ('', 'filesize', 'FileSize')
		self.value_filesize_combobox.current(1)
		self.value_filesize_combobox.grid(row=4, column=1)
		
		self.value_isbn_label = ttk.Label(self.frame_value, text='isbn:').grid(row=5, column=0)
		self.value_isbn = StringVar()
		self.value_isbn_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_isbn, width=self.combobox_width)
		self.value_isbn_combobox['values'] = ('', 'isbn', 'ISBN')
		self.value_isbn_combobox.current(1)
		self.value_isbn_combobox.grid(row=5, column=1)
		
		self.value_issn_label = ttk.Label(self.frame_value, text='issn:').grid(row=5, column=2)
		self.value_issn = StringVar()
		self.value_issn_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_issn, width=self.combobox_width)
		self.value_issn_combobox['values'] = ('', 'issn', 'ISSN')
		self.value_issn_combobox.current(1)
		self.value_issn_combobox.grid(row=5, column=3)
		
		self.value_sourcename_label = ttk.Label(self.frame_value, text='sourcename:').grid(row=5, column=4)
		self.value_sourcename = StringVar()
		self.value_sourcename_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_sourcename, width=self.combobox_width)
		self.value_sourcename_combobox['values'] = ('', 'journalname', 'JournamlName', 'MeetingName', 'meetingname')
		self.value_sourcename_combobox.current(1)
		self.value_sourcename_combobox.grid(row=5, column=5)
		
		self.value_pubunit_label = ttk.Label(self.frame_value, text='pubunit:').grid(row=6, column=0)
		self.value_pubunit = StringVar()
		self.value_pubunit_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_pubunit, width=self.combobox_width)
		self.value_pubunit_combobox['values'] = ('', 'pubunit', 'PubUnit')
		self.value_pubunit_combobox.current(1)
		self.value_pubunit_combobox.grid(row=6, column=1)
		
		self.value_pubaddress_label = ttk.Label(self.frame_value, text='pubaddress:').grid(row=6, column=2)
		self.value_pubaddress = StringVar()
		self.value_pubaddress_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_pubaddress, width=self.combobox_width)
		self.value_pubaddress_combobox['values'] = ('', 'publicationaddress', 'publicationAddress')
		self.value_pubaddress_combobox.current(1)
		self.value_pubaddress_combobox.grid(row=6, column=3)
		
		self.value_pubdate_label = ttk.Label(self.frame_value, text='pubdate:').grid(row=6, column=4)
		self.value_pubdate = StringVar()
		self.value_pubdate_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_pubdate, width=self.combobox_width)
		self.value_pubdate_combobox['values'] = ('', 'publicationdate', 'publicationDate', 'issueDate')
		self.value_pubdate_combobox.current(1)
		self.value_pubdate_combobox.grid(row=6, column=5)
		
		self.value_confaddress_label = ttk.Label(self.frame_value, text='confaddress:').grid(row=7, column=0)
		self.value_confaddress = StringVar()
		self.value_confaddress_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_confaddress, width=self.combobox_width)
		self.value_confaddress_combobox['values'] = ('', 'MeetingAddress', 'meetingaddress')
		self.value_confaddress_combobox.current(1)
		self.value_confaddress_combobox.grid(row=7, column=1)
		
		self.value_confdate_label = ttk.Label(self.frame_value, text='confdate:').grid(row=7, column=2)
		self.value_confdate = StringVar()
		self.value_confdate_combobox = ttk.Combobox(self.frame_value, textvariable=self.value_confdate, width=self.combobox_width)
		self.value_confdate_combobox['values'] = ('', 'MeetingDate', 'meetingdate')
		self.value_confdate_combobox.current(1)
		self.value_confdate_combobox.grid(row=7, column=3)

		#
		self.author_label = ttk.Label(self.frame_bottom, text='有问题请联系李岚清', font='Arial 12 bold')
		self.author_label.pack()

		# 页面布局
		self.frame_title.grid(row=0, column=0, padx=4, pady=4)
		self.frame_content.grid(row=1, column=0, padx=8, pady=8)
		self.frame_value.grid(row=2, column=0, padx=8, pady=8)
		self.frame_bottom.grid(row=3, column=0, padx=4, pady=4)

		self.root.mainloop()

	# file exist test Button 回调函数，验证所有的pdf文件是否都存在
	def mainFileExist(self):
		excel_file = self.excel_filepath.get().replace('\\', '/')
		actual_filepath = self.actual_filepath.get().replace('\\', '/')
		table_list = excelTableByIndex(excel_file)
		if fileExist(table_list, actual_filepath):
			msgb.showinfo('congragulate!', 'all file exist!')
		else:
			msgb.showerror('error!', 'some file not exist, please check it!')

	# 用来获取所有字段的值，然后以字典形式返回，便于其他函数使用
	def mainGetFieldToFieldDict(self):
		field_to_field_dict = {}

		field_to_field_dict['vol'] = self.value_vol.get()
		field_to_field_dict['issue'] = self.value_issue.get()
		field_to_field_dict['doi'] = self.value_doi.get()
		field_to_field_dict['year'] = self.value_year.get()
		field_to_field_dict['mtitle'] = self.value_mtitle.get()
		field_to_field_dict['authors'] = self.value_authors.get()
		field_to_field_dict['authorunit'] = self.value_authorunit.get()
		field_to_field_dict['keyword'] = self.value_keyword.get()
		field_to_field_dict['abstracts'] = self.value_abstracts.get()
		field_to_field_dict['pages'] = self.value_pages.get()
		field_to_field_dict['bepage'] = self.value_bepage.get()
		field_to_field_dict['filename'] = self.value_filename.get()
		field_to_field_dict['filesize'] = self.value_filesize.get()
		field_to_field_dict['isbn'] = self.value_isbn.get()
		field_to_field_dict['issn'] = self.value_issn.get()
		field_to_field_dict['sourcename'] = self.value_sourcename.get()
		field_to_field_dict['pubunit'] = self.value_pubunit.get()
		field_to_field_dict['pubaddress'] = self.value_pubaddress.get()
		field_to_field_dict['pubdate'] = self.value_pubdate.get()
		field_to_field_dict['confaddress'] = self.value_confaddress.get()
		field_to_field_dict['confdate'] = self.value_confdate.get()

		return field_to_field_dict

	# update data Button 回调函数，用来更新旧的excel文件中一些字段的值，然后生成新的excel文件
	def mainUpdateData(self):
		field_to_field_dict = self.mainGetFieldToFieldDict()
		excel_file = self.excel_filepath.get().replace('\\', '/')
		table_list = excelTableByIndex(excel_file)
		filepath_in_computer = self.filepath_in_computer.get().replace('\\', '/')

		updateData(excel_file, table_list, field_to_field_dict, filepath_in_computer)
		msgb.showinfo('congragulate!', 'success generate a new excel file!')

	# update s_source Button 回调函数，读取新的excel文件的数据，然后更新s_source数据库
	def mainUpdateS_source(self):
		field_to_field_dict = self.mainGetFieldToFieldDict()
		report_type = self.report_type.get()
		excel_file = self.excel_filepath.get().replace('\\', '/')
		new_excel_file = excel_file.split('.')[0] + '.new.xls'
		updateS_source(new_excel_file, field_to_field_dict, report_type)
		msgb.showinfo('congragulate!', 'success update s_source!')

	# excel data change Button 回调函数，对新的excel中字段的值进行转换，使其符合标准格式，并添加一些字段，并返回数据列表
	# 用于数据库插入操作，此步骤为在数据库操作之前测试数据是否存在问题，若存在问题，则应进行修改
	def mainExcelDataChange(self):
		field_to_field_dict = self.mainGetFieldToFieldDict()
		excel_file = self.excel_filepath.get().replace('\\', '/')
		new_excel_file = excel_file.split('.')[0] + '.new.xls'
		report_name = self.report_name.get()

		data_list = excelDataChange(new_excel_file, report_name, field_to_field_dict)
		print(len(data_list))
		msgb.showinfo('congragulate!', 'success change data!')

	# insert data into s_data Button 回调函数，用于数据库插入操作，此操作之前应先使用excel data change测试数据是否是标准格式
	def mainInsertNewDataToS_data(self):
		field_to_field_dict = self.mainGetFieldToFieldDict()
		excel_file = self.excel_filepath.get().replace('\\', '/')
		new_excel_file = excel_file.split('.')[0] + '.new.xls'
		report_name = self.report_name.get()

		data_list = excelDataChange(new_excel_file, report_name, field_to_field_dict)
		count = len(data_list)
		count1 = insertNewDataToS_data(data_list, report_name)
		count2 = changeDocidById(report_name)

		if count==count1 and count==count2:
			msgb.showinfo('congragulate!', 'you have finished this excel file, please select a new excel file or close main window')
		else:
			error_num = count - count1
			msgb.showerror('error!', 'you have %s data insert into s_data failed, please check it!' % error_num)

	# insert error data Button 回调函数，若前面插入数据出现问题，在解决问题后执行此操作，将会插入前面插入失败的数据
	# 正常情况下不需要点击此按钮
	def mainInsertErrorData(self):
		field_to_field_dict = self.mainGetFieldToFieldDict()
		excel_file = self.excel_filepath.get().replace('\\', '/')
		new_excel_file = excel_file.split('.')[0] + '.new.xls'
		report_name = self.report_name.get()

		data_list = excelDataChange(new_excel_file, report_name, field_to_field_dict)
		count1 = insertNewDataToS_data(data_list, report_name)
		count2 = changeDocidById(report_name)

		if count1 == count2:
			msgb.showinfo('congragulate!',
			              'you have inserted %d data into s_data, please check if the number equal the error_num.if')

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