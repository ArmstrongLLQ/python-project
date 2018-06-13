from django.db import models
class Teacher(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'teacher'

class Student(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    intime = models.DateTimeField()
    sex = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'student'
