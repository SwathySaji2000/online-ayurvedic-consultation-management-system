
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import logout
from . models import *
from datetime import datetime
from django.utils import timezone
#from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
# from django.core.mail import send_mail
# from django.conf import Settings
from django.core.mail import send_mail
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required

from django.conf import settings
from .models import Category
from .models import Subcategory
from .models import Product,CartItem,Cart
from django.views.decorators.cache import *

def new_password(request):
    request.session['lid']
    if 'new_p' in request.POST:
        np=request.POST['np']
        cp=request.POST['cp']
        if np == cp:
            
            lg=Login.objects.get(pk=request.session['lid'])
            lg.password=cp
            lg.save()
            return HttpResponse("<script>alert('Password Successfully Changed.');window.location='/login_fun_page'</script>")
        else:
            return HttpResponse("<script>alert('Confirm password mismatched.');window.location='/new_password'</script>")
   

    return render(request,'new_password.html')



def enter_otp(request):
    print("#############", request.session['otp'])
    if 'et_otp' in request.POST:
        otp_v=int(request.POST['otp_v'])
        if otp_v == request.session['otp']:
            return HttpResponse("<script>alert('Successfully Verified.');window.location='/new_password'</script>")
        else:
            return HttpResponse("<script>alert('Invalid OTP.');window.location='/enter_otp'</script>")
   

    return render(request,'enter_otp.html')



def forgot_password(request):
    import random
    otp = random.randint(1000, 9999)
    request.session['otp'] = otp
    print(random.randint(1000, 9999))
    if 'forgot' in request.POST:
        uname = request.POST['uname']
        email = request.POST['email']
        try:
            uu = Login.objects.get(username=uname)
            if uu:
                if uu.type == "Doctors":
                    try:
                        ee = Doctors.objects.get(email=email)
                        if ee:
                            request.session['lid'] = uu.pk
                            send_mail(
                                'Forgot Password Request' + uname,
                                'Your OTP(One Time Password) is: ' + str(otp),
                                'swathysaji143@gmail.com',
                                [email],
                                fail_silently=False,
                            )
                            return HttpResponse("<script>alert('Check Your Email.');window.location='/enter_otp'</script>")
                        else:
                            return HttpResponse("<script>alert('Invalid Email');window.location='/forgot_password'</script>")
                    except:
                        return HttpResponse("<script>alert('Invalid Email');window.location='/forgot_password'</script>")
                elif uu.type == "user":
                    
                    try:
                        ee1 = Users.objects.get(email=email)
                        print(ee1.FullName, '//////////////////////////////////')
                        if ee1:
                            print('gggggggggggggggggggggggggggg')
                            request.session['lid'] = uu.pk
                            send_mail(
                                'Forgot Password Request' + uname,
                                'Your OTP(One Time Password) is: ' + str(otp),
                                'swathysaji143@gmail.com',
                                [email],
                                fail_silently=False,
                            )
                            return HttpResponse("<script>alert('Check Your Email.');window.location='/enter_otp'</script>")
                        else:
                            return HttpResponse("<script>alert('Invalid Email');window.location='/forgot_password'</script>")
                    except:
                        return HttpResponse("<script>alert('Invalid Email');window.location='/forgot_password'</script>")
            else:
                return HttpResponse("<script>alert('Invalid Username.');window.location='/forgot_password'</script>")
        except:
            return HttpResponse("<script>alert('Invalid Username.');window.location='/forgot_password'</script>")
    return render(request, 'forgot_password.html')






def index(request):
    return render(request, 'indexxxx.html')


def doctor_index(request):
    dr=Doctors.objects.get(id=request.session['doc_id'])
    if dr:
        fns=dr.Name

    return render(request, 'doctor_index.html',{'fns':fns})



def landing_page(request):
    return render(request, 'landing_page.html')

def admin_home(request):
    return render(request, 'admin_home.html')


def logout_view(request):
    # Perform logout-related actions
    logout(request)

    # Redirect to the same page (refresh the page)
    return redirect('index')



def login_fun_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
     
        try:
            
            q = Login.objects.get(username=username, password=password)
        
            print(q)
            request.session['id'] = q.pk
            if q:
                if q.type == 'admin':
                    return HttpResponse("<script>alert('login successful'); window.location='/admin_home'</script>")
                elif q.type == 'Doctors':
                    qd = Doctors.objects.get(LOGIN_id=request.session['id'])
                    if qd:
                        request.session['doc_id'] = qd.pk
                        request.session['doctor'] = username
                    return HttpResponse("<script>alert('login successful'); window.location='/doctor_index'</script>")
                elif q.type == 'user':
                    qr = Users.objects.get(LOGIN_id=request.session['id'])
                    if qr:
                        request.session['email']=qr.email
                        request.session['uid'] = qr.pk
                    return HttpResponse("<script>alert('login successful');window.location='/patient_index'</script>")
                elif q.type == 'seller':
                    qs = Seller.objects.get(LOGIN_id=request.session['id'])
                    if qs:
                        request.session['seller'] = username
                        request.session['sid'] = qs.pk
                    return HttpResponse("<script>alert('login successful'); window.location='/seller_index'</script>")

        except:
            return HttpResponse("<script>alert('Invalid Username or Password');window.location='/login_fun_page'</script>")       
    return render(request, 'login_fun_page.html')




def patient_index(request):
    usr=Users.objects.get(id=request.session['uid'])
    if usr:
        fn=usr.FullName

    return render(request, 'patient_index.html',{'fn':fn})

def seller_index(request):
    sr=Seller.objects.get(id=request.session['sid'])
    if sr:
        f=sr.Name
    return render(request,'seller_index.html',{'f':f}) 


def register_user(request):
    if request.method == 'POST':
        fullName = request.POST['fullName']
        place = request.POST['place']
        age = request.POST['age']
        gender = request.POST['genderxxx']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        qr=Login(username=email,password=password,type="user")
        qr.save()

        qc=Users(FullName=fullName,Age=age,Place=place,Gender=gender,phone=phone,email=email,LOGIN=qr)
        qc.save()
        return HttpResponse("<script>alert('User registration successfully');window.location='/login_fun_page'</script>") 
    return render(request,'register_user.html')

def patient_profile(request):
    patient_up=Users.objects.get(id=request.session['uid'])
    if request.method == 'POST':
       patient_up.FullName = request.POST['fullName'] 
       patient_up.Age = request.POST['age']
       patient_up.Place = request.POST['place']
       patient_up.Gender = request.POST['genderxxx']
       patient_up.email = request.POST['email']
       patient_up.save()
       return HttpResponse("<script>alert('Your Profile updated  successfully');window.location='/home_patient'</script>") 
    return render(request,'patient_profile.html',{'patient_up':patient_up})

def doctor_profile(request):
    doctor_up=Doctors.objects.get(id=request.session['doc_id'])
    if request.method == 'POST':
        doctor_up.Name = request.POST['Name'] 
        doctor_up.email = request.POST['email'] 
        doctor_up.specialization = request.POST['specialization']
        doctor_up.place = request.POST['place']
        doctor_up.gender = request.POST['genderxxx']
        doctor_up.phone = request.POST['phone']
        doctor_up.save()  
        return HttpResponse("<script>alert('Your Profile updated  successfully');window.location='/landing_page'</script>") 
    return render(request,'doctor_profile.html',{'doctor_up':doctor_up})

def register_seller(request):
    if request.method == "POST" :
        Sellername = request.POST['Name']
        phone = request.POST['phone']
        email = request.POST['email']
        brandname = request.POST['brand_name']
        password = request.POST['password']
        pics = request.FILES.get('pic')
        password = request.POST['password']
        date = request.POST.get('registration_date')
        qs=Login(username=email,password=password,type="seller")
        qs.save()

        qs=Seller(Name=Sellername,phone=phone,email=email,brand_name=brandname,pic=pics,registration_date=date,password=password,LOGIN=qs)
        qs.save()
        return HttpResponse("<script>alert('Seller registration successfully');window.location='/login_fun_page'</script>") 
    return render(request,'register_seller.html')



def register_doctor(request):
    if request.method == "POST" :
        Namess = request.POST['Name']
        place = request.POST['place']
        DOB = request.POST['DOB']
        gender = request.POST['genderxxx']
        phone = request.POST['phone']
        email = request.POST['email']
        specialization = request.POST['specialization']
        d = request.FILES['pictures']
        # print("==================================",type(profile_picture))
        # fss = FileSystemStorage()
        # file_name = fss.save(profile_picture.name, profile_picture)
        fs=FileSystemStorage()
        fn=fs.save(d.name,d)



        password = request.POST['password']
        dr=Login(username=email,password=password,type="Doctors")
        dr.save()
        qdr=Doctors(Name=Namess,dob=DOB,place=place,specialization=specialization,gender=gender,phone=phone,email=email,LOGIN=dr, 
                    pic=d
                    )
        qdr.save()
        return HttpResponse("<script>alert('Doctor registration successfully');window.location='/login_fun_page'</script>") 
    return render(request, "register_doctor.html")
    


def adminmanage_doctor(request):
    if request.method == "POST":
        Namess = request.POST['Name']
        place = request.POST['place']
        DOB = request.POST['DOB']
        gender = request.POST['genderxxx']
        phone = request.POST['phone']
        email = request.POST['email']
        specialization = request.POST['specialization']
        password = request.POST['password']
        dr=Login(username=email,password=password,type="Doctors")
        dr.save()
        qdr=Doctors(Name=Namess,dob=DOB,place=place,specialization=specialization,gender=gender,phone=phone,email=email,LOGIN=dr)
        qdr.save()
        return HttpResponse("<script>alert('Doctor registration successfully');window.location='/login_fun'</script>") 
    return render(request, 'adminmanage_doctor.html')
    
def adminmando_view(request):
    docview=Doctors.objects.all()
    return render(request, 'adminmando_view.html',{'docview':docview})







def delete_doctor(request,id):
    docview=Doctors.objects.filter(LOGIN_id=id)
    docview.delete()
    dr=Login.objects.get(id=id)
    dr.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/admin_home'</script>")


def admin_update_doctor_details(request,id):
 qt=Doctors.objects.get(id=id)
 if request.method == "POST":   
    
    qt.Name=request.POST['firstname']
    qt.specialization=request.POST['specialization']
    qt.place=request.POST['place']
    qt.phone=request.POST['phone']
    qt.email=request.POST['email']
    qt.dob=request.POST['dob']
    qt.gender=request.POST['genderxxx']
    qt.save()
    return HttpResponse("<script>alert('Update Successfully');window.location='/admin_home'</script>")
 return render(request, 'admin_update_doctor_details.html',{'doc_up':qt})



def schedule_doctor(request):


 if request.method == "POST": 
    Date=request.POST['date']
    Timefrom=request.POST['timefrom']
    Timeto=request.POST ['timeto'] 
    sc=Schedule(date=Date,timefrom=Timefrom,timeto=Timeto)
    sc.save()
    return HttpResponse("<script>alert('Booking successfully');window.location='/schedule_doctor'</script>") 
 return render(request, "landingpage.html")









def adminmanage_user(request):
    if request.method == "POST":
        fullName = request.POST['fullName']
        place = request.POST['place']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        qr=Login(username=email,password=password,type="user")
        qr.save()
        qc=Users(FullName=fullName,Age=age,Place=place,Gender=gender,phone=phone,email=email,LOGIN=qr)
        qc.save()
        return HttpResponse("<script>alert('User registration Successfully');window.location='/login_fun'</script>")
    return render(request,'adminmanage_user.html')

def adminmanpa_view(request):
    docviews=Users.objects.all()
    return render(request, 'adminmanpa_view.html',{'docviews':docviews})

def delete_user(request,id):
    docviews=Users.objects.filter(LOGIN_id=id)
    docviews.delete()
    qr=Login.objects.get(id=id)
    qr.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/admin_home'</script>")



def admin_update_user(request,id):
 ur=Users.objects.get(id=id)
 if request.method == "POST":   
    ur.FullName=request.POST['fullName']
    ur.Place=request.POST['place']
    ur.phone=request.POST['phone']
    ur.email=request.POST['email']
    ur.Age=request.POST['age']
    ur.Gender=request.POST['gender']
    ur.Password=request.POST['password']
    ur.save()
    return HttpResponse("<script>alert('Update Successfully');window.location='/admin_home'</script>")
 return render(request, 'admin_update_user.html',{'docs_up':ur})













def schedule_form(request):
    from datetime import date
    cdate=date.today()
    if request.method == 'POST':
        date = request.POST['date']
        timefrom = request.POST['timefrom']
        timeto = request.POST['timeto']
        doctor_username = request.session.get('doctor')
        
        # Retrieve the doctor instance using the email
        doctor_instance = Doctors.objects.get(email=doctor_username)
        
        # Create a new Schedule instance with the retrieved Doctor instance
        sch = Schedule(DOCTOR=doctor_instance, date=date, timefrom=timefrom, timeto=timeto)
        sch.save()
        
        # Retrieve the updated doctor's schedule
        doctors_schedule = Schedule.objects.filter(DOCTOR=doctor_instance)
        
        return render(request, 'schedule_form.html', {'doctors_schedule': doctors_schedule,'cdate':cdate})
    
    # If it's a GET request, just display the form
    doctor_username = request.session.get('doctor')
    doctor_instance = Doctors.objects.get(email=doctor_username)
    sh = Schedule.objects.filter(DOCTOR=doctor_instance)
    
    return render(request, 'schedule_form.html', {'doctors_schedule': sh,'cdate':cdate})






def home_patient(request):
    docview=Doctors.objects.all()
    return render(request, 'home_patient.html',{'docview':docview})
    # return render(request, 'home_patient.html')



def view_slots(request, doctor_id):
    slots = Schedule.objects.filter(DOCTOR=doctor_id)
    return render(request, 'view_slots.html', { 'slots': slots})




def booking_doctor(request, id):
    print("......",request.session.get('uid'))
    current_date = timezone.now().date()
    print(current_date)
    myqr = Booking.objects.filter(SCHEDULE_id=id)
    print(myqr,"///////////////////////")
    if myqr:
        return HttpResponse("<script>alert('Already Booked Time');window.location='/home_patient'</script>")
    else:
        qr = Booking(SCHEDULE_id=id, USER_id=request.session.get('uid'), dateofbooking=current_date, Status='success')
        qr.save()

        subject = 'YOUR BOOKED APPOINTMENT'
        message = "Dear Sir/Madam,\nYour appointment has been successfully booked."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.session['email']]
        
        #send_mail(subject, message, email_from, recipient_list)

        
        return HttpResponse("<script>alert('Booked Successfully');window.location= '/home_patient'</script>")
    





def view_mybooking(request):
    uid = request.session.get('uid')
    bookings = Booking.objects.filter(USER=uid)
    return render(request, 'patient_view_mybook.html', {'bookings': bookings})
    # return render(request, 'home_patient.html')





def doctor_page(request):
    uid = request.session.get('doc_id')
    q = Schedule.objects.filter(DOCTOR_id=uid)
    
    all_bookings = []

    for schedule in q:
        sid = schedule.id
        bookings = Booking.objects.filter(SCHEDULE_id=sid)
        all_bookings.extend(bookings)


    return render(request, 'doctor_page.html', {'bookings': all_bookings})


def payment_check(request,b_id):
    current_date = timezone.now().date()

    if request.method == "POST":  

        qr = paymentss(booking_id_id=b_id, user_id_id=request.session.get('uid'),amount='300', date=current_date)
        qr.save()
        q=Booking.objects.get(id=b_id)
        if q:
            q.Status='paid'
            q.save()
            return HttpResponse("<script>alert('Payment success');window.location= '/mybookings'</script>")




        subject = 'PAYMENT SUCCESSFULL'
        message = "Dear Sir/Madam,\n Your Payment have  been successfully completed."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.session['email']]
        
        send_mail(subject, message, email_from, recipient_list)



    return render(request, 'payment_check.html')






def doctor_add_prescription(request,id):
    if request.method == "POST":
        medicine_name = request.POST['medicine_name']
        dosage = request.POST['dosage']
        ps=Prescriptions(medicine_name=medicine_name,dosage=dosage,BOOKING_id=id)
        ps.save()
    return render(request, 'doctor_add_prescription.html')

# def view_mypres(request):
#     uid=request.session.get('uid')
#     pre=Prescriptions.objects.all()
#     print("uuuuuuuuuuuuu",pre)
#     return render(request, 'view_pres.html',{pre:pre})

def user_view_pres(request):
    docviews=Prescriptions.objects.all()
    return render(request, 'user_view_pres.html',{'docviews':docviews})

def demoschedule(request):
    from datetime import date
    cdate=date.today()
    if request.method == 'POST':
        date = request.POST['date']
        timefrom = request.POST['timefrom']
        timeto = request.POST['timeto']
        doctor_username = request.session.get('doctor')
        
        # Retrieve the doctor instance using the email
        doctor_instance = Doctors.objects.get(email=doctor_username)
        
        # Create a new Schedule instance with the retrieved Doctor instance
        sch = Schedule(DOCTOR=doctor_instance, date=date, timefrom=timefrom, timeto=timeto)
        sch.save()
        
        # Retrieve the updated doctor's schedule
        doctors_schedule = Schedule.objects.filter(DOCTOR=doctor_instance)
        
        return render(request, 'schedule_form.html', {'doctors_schedule': doctors_schedule,'cdate':cdate})
    
    # If it's a GET request, just display the form
    doctor_username = request.session.get('doctor')
    doctor_instance = Doctors.objects.get(email=doctor_username)
    sh = Schedule.objects.filter(DOCTOR=doctor_instance)
    
    return render(request, 'demoschedule.html', {'doctors_schedule': sh,'cdate':cdate})



def category_product(request):
    if request.method == 'POST':
        categoryName = request.POST['name']
        cat = Category()
        cat.name = categoryName
        cat.save()  
        return redirect('sub_category') 
    categories = Category.objects.filter(name__in=["AYURVEDIC ARISHTAS & ASAVAS", "HOMEOPATHIC REMEDIES", "AYURVEDIC CHOORNAS & POWDERS"])
    context = {
        "categories": categories,
    }
    return render(request, 'category_page.html',context)
    
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
def delete_category(request, category_id):
    if request.method == 'POST':
        try:
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            messages.success(request, 'Category deleted successfully')
        except Category.DoesNotExist:
            messages.error(request, 'Category not found')
    # Redirect to category_product view after deleting the category
    return redirect('seller_index')
    #return HttpResponse("<script>alert('deleted successfully');window.location='/seller_index'</script>")     






def sub_category(request):
    if request.method == 'POST':       
       subcategoryname = request.POST['name']
       category_id = request.POST['category_id']
       category = Category.objects.get(id=category_id)
       scat = Subcategory(name=subcategoryname,category=category)
       scat.name= subcategoryname
       scat.category_id = category_id 
       scat.save()
       return redirect('product_list')
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request,'add_subcategory.html', context)   
    
from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist
from .models import Product, Category, Subcategory, Seller

def product_list(request):
    if request.method == 'POST':
        try:
            # Extract data from the POST request
            productname = request.POST.get('productname')
            productdescription = request.POST.get('productdescription')
            productprice = request.POST.get('productprice')
            productdiscount = request.POST.get('productdiscount')
            productquantityavailable = request.POST.get('productquantityavailable')
            
            productingredients = request.POST.get('productingredients')
          
            productusageinstructions = request.POST.get('productusageinstructions')
            productcertificate = request.FILES.get('productcertificate')
            productexpirydate = request.POST.get('productexpirydate')
            productmanufacturer = request.POST.get('productmanufacturer')
            category_id = request.POST.get('category')  # Get the selected category ID
            subcategory_id = request.POST.get('subcategory')  # Get the selected subcategory ID
            seller_id = request.POST.get('seller')  # Get the selected seller ID
            product_image = request.FILES.get('product_image')
            # Get the Category, Subcategory, and Seller objects based on the selected IDs
            category = Category.objects.get(id=category_id)
            subcategory = Subcategory.objects.get(id=subcategory_id)
            seller = Seller.objects.get(id=seller_id)

            # Create and save the new product
            pr = Product.objects.create(
                name=productname,
                description=productdescription,
                price=productprice,
                discount=productdiscount,
                quantity_available=productquantityavailable,
                product_image=product_image ,
               
                ingredients=productingredients,
               
                usage_instructions=productusageinstructions,
                certifications=productcertificate,
                expiry_date=productexpirydate,
                manufacturer=productmanufacturer,
                category=category,  # Assign the category to the product
                subcategory=subcategory,  # Assign the subcategory to the product
                seller=seller  # Assign the seller to the product
                
            )

            # Redirect to prevent form resubmission on page refresh
            return redirect('product_display')
        except ObjectDoesNotExist:
            # Handle the case where the specified objects do not exist
            return HttpResponseServerError("One of the selected objects does not exist.")
        except Exception as e:
            # Handle other exceptions
            return HttpResponseServerError(f"An error occurred: {e}")
    else:
        # Handle GET request to render the page with the form
        products = Product.objects.all()
        categories = Category.objects.all()  # Fetch all categories
        subcategories = Subcategory.objects.all()  # Fetch all subcategories
        sellers = Seller.objects.all()  # Fetch all sellers
        return render(request, 'ayurproduct_list.html', {'products': products, 'categories': categories, 'subcategories': subcategories, 'sellers': sellers})
    

def added_products(request):
     # Fetch all added products
    products = Product.objects.all()
     
    return render(request, 'added_product.html', {'products': products})      

from django.shortcuts import render, get_object_or_404
def update_product_details(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        # Update product details based on the POST data
        product.name = request.POST['productname']
        product.description = request.POST['productdescription']
        product.price = request.POST['productprice']
        product.discount = request.POST['productdiscount']
        product.quantity_available = request.POST['productquantityavailable']
        product.ingredients = request.POST['productingredients']
        product.usage_instructions = request.POST['productusageinstructions']
        product.certifications = request.FILES.get('productcertificate')
        product.expiry_date = request.POST['productexpirydate']
        product.manufacturer = request.POST['productmanufacturer']
        product.category_id = request.POST.get('category')  # corrected method
        product.subcategory_id = request.POST.get('subcategory')  # corrected method
        product.seller_id = request.POST.get('seller')  # corrected method
        product.product_image = request.FILES.get('product_image')
        product.save()
        return render(request, 'seller_index.html')  # Redirect to a success page or any other desired page
    else:
        # Render the edit product form with the product details
        categories = Category.objects.all()  # Assuming you have a Category model
        subcategories = Subcategory.objects.all()  # Assuming you have a Subcategory model
        sellers = Seller.objects.all()  # Assuming you have a Seller model
        return render(request, 'edit_product.html', {'product': product, 'categories': categories, 'subcategories': subcategories, 'sellers': sellers})
    
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('category') 

def search_products(request):
    query = request.GET.get('query')
    category_id = request.GET.get('category')
    products = Product.objects.all()
    categories = Category.objects.all()
    
    if query:
        products = products.filter(name__icontains=query)
    if category_id:
        products = products.filter(category_id=category_id)
    
    context = {
        "products": products,
        "categories": categories,
    }
    return render(request, 'added_product.html', context)


from django.shortcuts import render
from .models import Product

def patient_product_list(request):
    products = Product.objects.all()  # Retrieve all products
    return render(request, 'patient_product_list.html', {'products': products})

# @login_required(login_url='login_fun_page')
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     if request.method == 'POST':
#         quantity = int(request.POST.get('quantity', 1))
#         cart, created = Cart.objects.get_or_create(user=request.user)
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#         cart_item.quantity += quantity
#         cart_item.save()
#         return redirect('cart')
#     return redirect('product_detail', product_id=product_id)

from django.contrib.auth.decorators import login_required


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            # Redirect or display a message indicating invalid quantity
            return redirect('product_detail', product_id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Check if the product already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        # If the product already exists, update the quantity
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return redirect('cart')
    else:
        if request.user.is_authenticated:
            # User is authenticated, redirect to the login page with the next parameter
            return redirect('login_fun_page', next=request.path)
        else:
            # User is not authenticated, render a template indicating login is required
            return render(request, 'patient_imdex.html')





@login_required(login_url='login_fun_page')
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    try:
        cart_item = cart.cartitem_set.get(product=product)
        if cart_item.quantity >= 1:
             cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    
    return redirect('cart')


@login_required(login_url='login_fun_page')
def view_cart(request):
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required(login_url='login_fun_page')
def increase_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

@login_required(login_url='login_fun_page')
def decrease_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item = cart.cartitem_set.get(product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

@login_required(login_url='login_fun_page')
def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})




def get_cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart=request.user.cart)
        cart_count = cart_items.count()
    else:
        cart_count = 0
    return cart_count



def checkout(request, product_id):
    # Retrieve the product based on the provided product_id
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('patient_index')  # Redirect to home page or any other appropriate URL
    
    # Perform checkout logic here, such as processing payment, updating inventory, etc.
    
    messages.success(request, f"Checkout successful! Thank you for your purchase of {product.name}.")
    return redirect('checkout.html')
















































# @login_required(login_url='login_fun_page')

# def add_to_cart(request, product_id):
#     if request.user.is_authenticated:
#         product = Product.objects.get(id=product_id)
#         cart, created = Cart.objects.get_or_create(user=request.user)
#         cart.items.add(product)
#         messages.success(request, f"{product.name} added to cart successfully.")
#         # Retrieve all cart items including the newly added product
#         cart_items = cart.items.all()
#         context = {
#             'cart_items': cart_items,
#             'product_added': product  # Pass the product added to the cart for display on cart page
#         }
#         return render(request, 'cart.html', context)  # Render cart page with updated cart items and product details
#     else:
#         messages.error(request, "You need to be logged in to add items to the cart.")
#         return redirect('cart')
    
# def remove_from_cart(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     cart = Cart.objects.get(user=request.user)
#     try:
#         cart_item = cart.cartitem_set.get(product=product)
#         if cart_item.quantity >= 1:
#              cart_item.delete()
#     except CartItem.DoesNotExist:
#         pass
    
#     return redirect('cart')


# def cart_view(request):
#     # Assuming you have a Cart model associated with the user
#     if hasattr(request.user, 'cart'):
#         cart_items = request.user.cart.items.all()
#     else:
#         # If the user is anonymous or doesn't have a cart, handle accordingly
#         cart_items = []

#     context = {
#         'cart_items': cart_items
#     }
#     return render(request, 'cart.html', context)



# def increase_cart_item(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     cart = request.user.cart
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

#     cart_item.quantity += 1
#     cart_item.save()

#     return redirect('cart')


# def decrease_cart_item(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     cart = request.user.cart
#     cart_item = cart.cartitem_set.get(product=product)

#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()

#     return redirect('cart')   


# def add_to_wishlist(request, product_id):
#     # Add logic to add the product to the wishlist
#     # For example:
#     if request.method == 'POST':
#         # Logic to add the product to the wishlist
#         return HttpResponse("Product added to wishlist successfully!")  

# def checkout_view(request):
#     if request.method == 'POST':
#         # Process the form data here (e.g., save to database)
#         # Redirect to a thank you page or order summary page
#         return render(request, 'thank_you.html')  # Example: thank_you.html is the template for the thank you page
#     else:
#         return render(request, 'checkout.html')     

# def purchase(request):
#     if request.method == 'POST':
#         cart = Cart.objects.get(user=request.user)
#         cart_items = cart.items.all()
#         for cart_item in cart_items:
#             product = cart_item.product
#             quantity_purchased = cart_item.quantity
#             if product.quantity_available < quantity_purchased:
#                 messages.error(request, f"Not enough quantity available for {product.name}.")
#                 return redirect('cart')
#             product.quantity_available -= quantity_purchased
#             product.save()
#         # Process payment and create order
#         # Clear the cart after successful purchase
#         cart.items.clear()
#         messages.success(request, "Purchase successful. Your order has been placed.")
#         return redirect('home')  # Redirect to home page or order confirmation page
#     else:
#         return redirect('cart')