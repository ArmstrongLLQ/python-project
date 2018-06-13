from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import datetime
from blog.models import Student, Teacher
# Create your views here.


def index(request):
	t = loader.get_template('index.html')
	user = {'name':'Tom', 'age':'23', 'sex':'male'}
	c = {'title':'django', 'user':user}
	return HttpResponse(t.render(c))

def time(request):
	t = loader.get_template('time.html')
	id = request.GET.get('id')
	c = {'today': datetime.datetime.now(), 'id':id}
	return HttpResponse(t.render(c))

def stu_list(request):
	t = loader.get_template('stu_list.html')

	# select sql
	student_list = Student.objects.all() # select * from student
	student_list = Student.objects.all().order_by('age') # order by age
	student_list = Student.objects.all().filter(age = 16) # age = 16
	student_list = Student.objects.all().filter(age__gt = 16) # age > 16
	student_list = Student.objects.all().filter(age__gte = 16) # age >= 16
	student_list = Student.objects.all().filter(name__contains = 'tom') # name like "%tom%"

	# update sql
	student = Student.objects.get(id=2) # get one student
	student.name = 'jerry'
	student.age = 50
	student.save()
	# update age < 20 student name = 'sss'
	update_stu = Student.objects.filter(age__lt = 20).update(name='sss')

	# insert sql
	new_stu = Student(name='armstrong', age=25, intime='2017-01-01', sex = 1)
	new_stu.save()

	# delete sql
	# delete one
	student = Student.objects.get(id=2)
	student.delete()
	# delete more than one 
	student = Student.objects.filter(name='armstrong')
	student.delete()
	# delete all
	student = Student.objects.all().delete()

	c = {'stu_list': student_list}
	return HttpResponse(t.render(c))
