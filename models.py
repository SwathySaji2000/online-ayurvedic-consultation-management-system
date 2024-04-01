
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.utils import timezone

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
    pic =   models.ImageField(max_length=1000)

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


        
class paymentss(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    amount = models.CharField( max_length=50)
    date = models.CharField( max_length=500)

class Prescriptions(models.Model):
    BOOKING = models.ForeignKey(Booking, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=500)
    dosage = models.CharField(max_length=400)

    
class Seller(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    Name   =  models.CharField( max_length=50)
    brand_name = models.CharField(max_length=255)
    phone = models.CharField( max_length=50)
    email = models.CharField( max_length=50)
    pic =   models.ImageField(max_length=1000)
    registration_date = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.brand_name    
    

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


       

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.CharField(max_length=200,default=False)
    quantity_available = models.IntegerField()
    ingredients = models.TextField(blank=True, null=True)
    usage_instructions = models.TextField(blank=True, null=True)
    certifications = models.ImageField(max_length=1000,default=True)
    expiry_date = models.DateField(blank=True, null=True)
    manufacturer = models.CharField(max_length=2000,null=True)
    product_image = models.ImageField(upload_to='product_images/', max_length=1000, blank=True, null=True)
    def __str__(self):
        return self.name 
    
class P_booking(models.Model):
    p_amount = models.CharField(max_length=2000,null=True)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    p_date = models.CharField(max_length=2000,null=True)
    p_status = models.CharField(max_length=225,null=True)

class P_bookingchild(models.Model):
    P_booking = models.ForeignKey(P_booking,on_delete=models.CASCADE)   
    book_amount = models.CharField(max_length=225)
    quantity = models.CharField(max_length=225)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)