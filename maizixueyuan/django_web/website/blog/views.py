from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context
import datetime
 
def index(request):
	t = loader.get_template("index.html")
	user = {"name":"jack", "age":"17", "sex":"male"}
	booklist = ['python', 'java', 'c++']
	c = Context({"title":"django", "user":user, "booklist":booklist, "today":datetime.datetime.now})
	return HttpResponse(t.render(c))

def time(request):
	t = loader.get_template("time.html")
	user = {"name":"jack", "age":"17", "sex":"male"}
	booklist = ['python', 'java', 'c++']
	c = Context({"title":"django", "user":user, "booklist":booklist, "today":datetime.datetime.now})
	return HttpResponse(t.render(c))