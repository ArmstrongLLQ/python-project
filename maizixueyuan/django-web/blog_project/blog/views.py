from django.shortcuts import render
import logging

logger = logging.getLogger('blog.views')
# Create your views here.
def index(request):
	try:
		pass
	except Exception as e:
		pass
	return render(request, 'index.html', locals())