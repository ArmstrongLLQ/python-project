from django.shortcuts import render
import logging
from bitcs.models import *
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger

logger = logging.getLogger("bitcs.views")
# Create your views here.
def index(request):
	try:
		menu = request.GET.get('menu', 'inforday')
		if menu=='inforday':
			inf_list = Inforday.objects.order_by('-time')
		elif menu=='jimo':
			inf_list = Jimo.objects.order_by('-time')
		else:
			inf_list = Inforconduction.objects.order_by('-time')
	except Exception as e:
		print(e)

	paginator = Paginator(inf_list, 10)
	try:
		page = int(request.GET.get('page', 1))
		inf_list = paginator.page(page)
	except (EmptyPage, InvalidPage, PageNotAnInteger):
		inf_list= paginator.page(1)
	return render(request, 'index.html', locals())

def detailPage(request):
	_id = request.GET.get('_id', '')
	# menu = request.GET.get('menu', 'inforday')
	if Inforday.objects.filter(_id=_id).only('title', 'content', 'time', 'url'):
		news = Inforday.objects.filter(_id=_id).only('title', 'content', 'time', 'url')
	elif Jimo.objects.filter(_id=_id).only('title', 'content', 'time', 'url'):
		news = Jimo.objects.filter(_id=_id).only('title', 'content', 'time', 'url')
	elif Inforconduction.objects.filter(_id=_id).only('title', 'content', 'time', 'url'):
		news = Inforconduction.objects.filter(_id=_id).only('title', 'content', 'time', 'url')
	else:
		pass
	# news = chain(news1, news2, news3)
	# news = [news1, news2, news3]


	#

	# news.extend(Inforconduction.objects.filter(_id=_id))
	# if menu == 'inforday':
	# 	news = Inforday.objects.filter(_id=_id)
	# elif menu == 'jimo':
	# 	news = Jimo.objects.filter(_id=_id)
	# else:
	# 	news = Inforconduction.objects.filter(_id=_id)
	return render(request, 'detailPage.html', locals())

def searchPage(request):
	kw = request.GET.get('kw', '')
	query_results1 = Inforday.objects.filter(title__icontains=kw)
	query_results2 = Jimo.objects.filter(title__icontains=kw)
	query_results3 = Inforconduction.objects.filter(title__icontains=kw)
	# query_results = chain(query_results1, query_results2, query_results3)
	query_results = []
	query_results.extend(query_results1)
	query_results.extend(query_results2)
	query_results.extend(query_results3)


	paginator = Paginator(query_results, 10)
	try:
		page = int(request.GET.get('page', 1))
		query_results = paginator.page(page)
	except (EmptyPage, InvalidPage, PageNotAnInteger):
		query_results = paginator.page(1)
	return render(request, 'searchPage.html', locals())

def advSearchPage(request):
	return render(request, 'advSearchPage.html', locals())

def advSearchResult(request):
	return render(request, 'advSearchResult.html', locals())
