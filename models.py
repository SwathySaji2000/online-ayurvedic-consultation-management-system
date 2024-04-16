
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

class Payment(models.Model):
    P_booking = models.ForeignKey(P_booking,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.CASCADE) 
    date = models.CharField(max_length=2000,null=True)
    py_status = models.CharField(max_length=225,null=True)


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('ac', 'AC'),
        ('non_ac', 'Non-AC'),
    ]

    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)

    def __str__(self):
        return self.name

class Bookings(models.Model):
    TREATMENT_CHOICES = [
        ('panchakarma', 'Panchakarma'),
        ('vamanan', 'Vamanan'),
        ('snehavasthy', 'Snehavasthy'),
        ('nasyam', 'Nasyam'),
        ('shirodhara', 'Shirodhara'),
        ('tharpanam', 'Tharpanam'),
        ('putapakam', 'Putapakam'),
        # Add more treatment options as needed
    ]
    FOOD_PLAN_CHOICES = [
        ('regular', 'Regular'),
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('gluten_free', 'Gluten-Free'),
        # Add more food plan options as needed
    ]
    NUMBER_OF_DAYS_CHOICES = [
        (3, '3 days'),
        (5, '5 days'),
        (7, '7 days'),
        # Add more number of days options as needed
    ]
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_start = models.DateField()
    treatment_type = models.CharField(max_length=100, choices=TREATMENT_CHOICES)
    food_plan = models.CharField(max_length=100, choices=FOOD_PLAN_CHOICES)
    number_of_days = models.PositiveIntegerField(choices=NUMBER_OF_DAYS_CHOICES)
    status = models.CharField(max_length=100, default='pending')
    


    def save(self, *args, **kwargs):
        if not self.pk and self.room is None:
            # Automatically allocate room based on the room type selected by the user
            if self.room_type:
                available_rooms = Room.objects.filter(room_type=self.room_type)
                if available_rooms.exists():
                    self.room = available_rooms.first()
                else:
                    # Handle case where no rooms of the selected type are available
                    raise Exception("No available rooms of selected type")
            else:
                # Handle case where room_type is not provided
                raise Exception("Room type is required")
        super().save(*args, **kwargs)



# class Paymentt(models.Model):
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     user = models.ForeignKey(Users, on_delete=models.CASCADE,default=True)

#     def __str__(self):
#         return f"Payment ID: {self.payment_id}, Amount: {self.amount}"