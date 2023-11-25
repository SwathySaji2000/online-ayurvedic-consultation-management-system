
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class Login(models.Model):
    username = models.CharField( max_length=50)
    password = models.CharField(max_length=50)
    type=models.CharField(max_length=50)

class Doctors(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    Name   =  models.CharField( max_length=50)
    gender = models.CharField( max_length=50)
    dob = models.CharField( max_length=50)
    specialization = models.CharField( max_length=50)
    place = models.CharField( max_length=50)
    phone = models.CharField( max_length=50)
    email = models.CharField( max_length=50)
    #pic =   models.ImageField(upload_to='profile_pic_doc/', null=True, blank=True)

class Users(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    FullName = models.CharField( max_length=50)
    Age= models.CharField(max_length=50)
    Place= models.CharField(max_length=50)
    Gender = models.CharField(max_length=50)
    phone = models.CharField( max_length=50)
    email = models.CharField( max_length=50)

class Feedback(models.Model):
    DOCTOR = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    USER = models.ForeignKey(Users, on_delete=models.CASCADE)
    feedback = models.CharField( max_length=50)
    date = models.DateField(auto_now=False, auto_now_add=False)


class Schedule(models.Model):
     DOCTOR = models.ForeignKey(Doctors, on_delete=models.CASCADE)
     date = models.DateField( auto_now=False, auto_now_add=False)
     timefrom = models.TimeField(auto_now=False, auto_now_add=False)
     timeto = models.TimeField( auto_now=False, auto_now_add=False)

class Booking(models.Model):
      SCHEDULE = models.ForeignKey(Schedule, on_delete=models.CASCADE)
      USER = models.ForeignKey(Users, on_delete=models.CASCADE)
      dateofbooking = models.DateField(auto_now=False, auto_now_add=False)
      Status = models.CharField( max_length=50)

class Prescription(models.Model):
      BOOKING = models.ForeignKey(Booking, on_delete=models.CASCADE)
      description = models.CharField( max_length=500)
     

 