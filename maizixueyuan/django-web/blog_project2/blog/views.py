from django.shortcuts import render
import logging
from django.conf import settings
from blog.models import *
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger

logger = logging.getLogger('blog.views')
# Create your views here.
def global_setting(request):
	return {'SITE_NAME': settings.SITE_NAME,
	        'SITE_DESC': settings.SITE_DESC,
	        'WEIBO_SINA': settings.WEIBO_SINA,
	        'WEIBO_TENCENT': settings.WEIBO_TENCENT}

def index(requset):
	category_list = Category.objects.all()
	article_list = Category.objects.all()
	paginator = Paginator(article_list, 2)
	try:
		page = int(requset.GET.get('page', 1))
		article_list = paginator.page(page)
		print(article_list)
	except (EmptyPage, InvalidPage, PageNotAnInteger):
		article_list = paginator.page(1)

	return render(requset, 'index.html', {'category_list': category_list, 'article_list': article_list})
