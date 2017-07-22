# -*- coding: utf-8 -*-
import os

#查找文件函数，返回文件绝对路径
def get_file(path):
    tail = "txt"
    fullpath=[]
    for dirpath,dirname,files in os.walk(path):
        for filename in files:
            if "." in filename:
                if filename.split(".")[-1] == tail:
                    fullpath.append(os.path.join(dirpath,filename))
    return fullpath

keyword = "os"
line_number = 0
path_collection = get_file(".")
for file_path in path_collection:
    with open(file_path) as f, open("../result.txt", "a+") as f1:
        for line in f.readlines():
             line_number += 1
             if keyword in line:
                 f1.write("".join([file_path, " ", str(line_number), " ", line]))