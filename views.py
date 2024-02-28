
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
from django.conf import settings
from .models import Category
from .models import Subcategory
from .models import Product


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
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, 'category_page.html', context)


def sub_category(request):
    if request.method == 'POST':       
       subcategoryname = request.POST['name']
       category_id = request.POST['category_id']
       category = Category.objects.get(id=category_id)
       scat = Subcategory(name=subcategoryname,category=category)
       scat.name= subcategoryname
       scat.category_id = category_id 
       scat.save()
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request,'add_subcategory.html', context)   
    
def product_list(request):
    if request.method == 'POST':
       productname = request.POST.get('name')
       productdescription = request.POST.get('description')
       productprice = request.POST.get('price')
       productdiscount = request.POST.get('discount')
       productquantityavailable = request.POST.get('quantity_available')
       productimage = request.FILES.get('image')
       productadditionalimage = request.FILES.get('add_image')
       productingredients = request.POST.get('ingredients')
       productayurvedicproperties = request.POST.get('ayurvedic_properties')
       productusageinstructions = request.POST.get('usage_instructions')
       productcertificate = request.FILES.get('certifications')
       productexpirydate = request.POST.get('expiry_date')
       productmanufacturer = request.FILES.get('manufacturer')
       pr = Product(name=productname,description=productdescription,price=productprice,discount=productdiscount,quantity_available=productquantityavailable,image=productimage,add_image=productadditionalimage,ingredients=productingredients,ayurvedic_properties=productayurvedicproperties,usage_instructions=productusageinstructions,certifications=productcertificate,expiry_date=productexpirydate,manufacturer=productmanufacturer)
       pr.save()
       products= Product.objects.all()
       categories = Category.objects.all()
       categories.save()
       scat = Subcategory.objects.all()
       scat.save()
       seller = Seller.objects.all()
       seller.save()
       return render(request,'ayurproduct_list.html',{'products': products})
