# coding:utf-8
import pygame
import sys

#初始化pygame
pygame.init()

size = width, height = 600, 400
speed = [-2, 1]
bg = (255, 255, 255)

fullscreen = False

#创建指定大小的窗口
screen = pygame.display.set_mode(size)
#设置窗口标题
pygame.display.set_caption("first pygame")

#加载图片
tutle = pygame.image.load("3.gif")
#获取图像的位置矩形
position = tutle.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = [-1, 0]
            if event.key == pygame.K_RIGHT:
                speed = [1, 0]
            if event.key == pygame.K_UP:
                speed = [0, -1]
            if event.key == pygame.K_DOWN:
                speed = [0, 1]

            if event.key == pygame.K_F1:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((1366, 768))
                else:
                    screen = pygame.display.set_mode(size)
        

    #移动图像
    position = position.move(speed)

    if position.left < 0 or position.right > width:
        tutle = pygame.transform.flip(tutle, True, False)
        speed[0] = -speed[0]

    if position.top < 0 or position.bottom > height:
        speed[1] = -speed[1]

    #填充背景
    screen.fill(bg)
    #更新图像
    screen.blit(tutle, position)
    #更新界面
    pygame.display.flip()
    #延时10毫秒
    pygame.time.delay(10)

