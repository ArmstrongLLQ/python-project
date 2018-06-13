# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser



# 标签
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __unicode__(self):
        return self.name

# 文章分类
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField('显示顺序(从小到大)',default=999)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.name


