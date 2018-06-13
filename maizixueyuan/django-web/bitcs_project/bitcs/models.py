from django.db import models
import mongoengine

# Create your models here.
class Student(mongoengine.Document):
	name = mongoengine.StringField(max_length=20)
	age = mongoengine.IntField(default=1)

class Inforday(mongoengine.Document):
	_id = mongoengine.ObjectIdField(primary_key=True)
	title = mongoengine.StringField()
	ExhTime = mongoengine.DateTimeField()
	Category = mongoengine.StringField()
	fromTime = mongoengine.DateTimeField()
	time = mongoengine.DateTimeField()
	srcUrl = mongoengine.StringField()
	Name = mongoengine.StringField()
	url = mongoengine.StringField()
	content = mongoengine.StringField()

class Inforconduction(mongoengine.Document):
	_id = mongoengine.ObjectIdField(primary_key=True)
	title = mongoengine.StringField()
	ExhTime = mongoengine.DateTimeField()
	Category = mongoengine.StringField()
	fromTime = mongoengine.DateTimeField()
	time = mongoengine.DateTimeField()
	url = mongoengine.StringField()
	content = mongoengine.StringField()

class Jimo(mongoengine.Document):
	_id = mongoengine.ObjectIdField(primary_key=True)
	title = mongoengine.StringField()
	Category = mongoengine.StringField()
	fromTime = mongoengine.DateTimeField()
	time = mongoengine.DateTimeField()
	srcUrl = mongoengine.StringField()
	Name = mongoengine.StringField()
	url = mongoengine.StringField()
	content = mongoengine.StringField()
	srcUrlText = mongoengine.StringField()
