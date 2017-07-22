# coding:utf-8
import pygame
import sys

#初始化pygame
pygame.init()

size = width, height = 600, 400
#创建指定大小的窗口
screen = pygame.display.set_mode(size)
#设置窗口标题
pygame.display.set_caption("first pygame")

f = open('record.txt', 'w')

while True:
    for event in pygame.event.get():
        f.write(str(event) + '\n')

        if event.type == pygame.QUIT:
            sys.exit()



