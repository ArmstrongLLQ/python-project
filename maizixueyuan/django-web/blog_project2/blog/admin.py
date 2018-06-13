from django.contrib import admin
from blog.models import *
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'desc', 'click_count',)
	list_display_links = ('title', 'desc',)
	list_editable = ('click_count',)

	fieldsets = (
		(None, {
			'fields': ('title', 'desc', 'content', 'user', 'category', 'tag',)
		}),
		('高级设置', {
			'classes': ('collapse',),
			'fields': ('click_count', 'is_recommend',)
		}),
	)
	class Media:
		js = (
		    '/static/js/kindeditor-4.1.10/kindeditor-min.js',
		    '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
		    '/static/js/kindeditor-4.1.10/config.js',
		)

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'index',)

class TagAdmin(admin.ModelAdmin):
	list_display = ('name',)

admin.site.register(User)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)
