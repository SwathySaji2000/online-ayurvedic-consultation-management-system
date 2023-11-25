
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import logout
from . models import *
from datetime import datetime
from django.utils import timezone
#from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

def index(request):
    return render(request, 'index.html')

def doc_indexx(request):
    return render(request, 'doc_indexx.html')

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
            request.session['id'] = q.pk
            if q:
                if q.type == 'admin':
                    return HttpResponse("<script>alert('login successful'); window.location='/admin_home'</script>")
                elif q.type == 'Doctors':
                    qd = Doctors.objects.get(LOGIN_id=request.session['id'])
                    if qd:
                        request.session['doc_id'] = qd.pk
                        request.session['doctor'] = username
                    return HttpResponse("<script>alert('login successful'); window.location='/landing_page'</script>")
                elif q.type == 'user':
                    qr = Users.objects.get(LOGIN_id=request.session['id'])
                    if qr:
                        request.session['uid'] = qr.pk
                    return HttpResponse("<script>alert('login successful');window.location='/home_patient'</script>")
        except:
            return HttpResponse("<script>alert('Invalid Username or Password');window.location='/login_fun_page'</script>")       
    return render(request, 'login_fun_page.html')

# def login_fun_page(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         try:
#             q = Login.objects.get(username=username, password=password)
#             # request.session['id'] = q.pk
#             if q:
#                 if q.type == 'admin':
#                     return HttpResponse("<script>alert('login successful'); window.location='/admin_home'</script>")
#                 # elif q.type == 'Doctors':
#                 #     q3 = Doctors.objects.get(LOGIN_id=request.session['id'])
#                 #     request.session['doctor'] =  username
#                 #     return render(request, 'landing_page.html')
#                 #     # if q3:
#                 #     #     request.session['f_id'] = q3.pk
#                 #     #     print("============================,",request.session['f_id'])
#                 #     # #return HttpResponse("<script>alert('login successful');window.location='/doctor_home'</script>")
#                 #     # return render(request, 'landing_page.html')
#                 # elif q.type == 'user':
#                 #     qr = Users.objects.get(LOGIN_id=request.session['id'])
#                 #     if qr:
#                 #         request.session['uid'] = qr.pk
#                 #              # docview=Doctors.objects.all()
#                 #     # return render(request, 'home_patient.html',{'docview':docview})
#                 #     return HttpResponse("<script>alert('login successful');window.location='/home_patient'</script>")
#         except:
#             return HttpResponse("<script>alert('Invalid Username or Password');window.location='/login_fun'</script>")       
#     return render(request, 'login_fun.html')


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

def register_doctor(request):
    if request.method == "POST" :
        Namess = request.POST['Name']
        place = request.POST['place']
        DOB = request.POST['DOB']
        gender = request.POST['genderxxx']
        phone = request.POST['phone']
        email = request.POST['email']
        specialization = request.POST['specialization']
        profile_picture = request.FILES['pictures']
        print("==================================",type(profile_picture))
        fss = FileSystemStorage(profile_picture)
        file_name = fss.save()
        password = request.POST['password']
        dr=Login(username=email,password=password,type="Doctors")
        dr.save()
        qdr=Doctors(Name=Namess,dob=DOB,place=place,specialization=specialization,gender=gender,phone=phone,email=email,LOGIN=dr, 
                    pic=file_name
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
        
        return render(request, 'schedule_form.html', {'doctors_schedule': doctors_schedule})
    
    # If it's a GET request, just display the form
    doctor_username = request.session.get('doctor')
    doctor_instance = Doctors.objects.get(email=doctor_username)
    sh = Schedule.objects.filter(DOCTOR=doctor_instance)
    
    return render(request, 'schedule_form.html', {'doctors_schedule': sh})






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
        qr = Booking(SCHEDULE_id=id, USER_id=request.session.get('uid'), dateofbooking=current_date, Status='sucess')
        qr.save()
        return HttpResponse("<script>alert('Booked Successfully');window.location= '/home_patient'</script>")
    


def view_mybooking(request):
    uid = request.session.get('uid')
    bookings = Booking.objects.filter(USER=uid)
    return render(request, 'patient_view_mybook.html', {'bookings': bookings})
    # return render(request, 'home_patient.html')



    
























































# def view_booking(request,id):
#     myqr=Booking.objects.all()
#     return render(request, 'home_patient.html',{'myqr':myqr



# def book_appointment(request):
#     if request.method == 'POST':
#         schedule_id = request.POST.get('schedule_id')
#         date = request.POST.get('date')
        
#         date_object = datetime.strptime(date, '%b. %d, %Y')
#         formatted_date = date_object.strftime('%Y-%m-%d')
#         timefrom = request.POST.get('timefrom')
#         timeto = request.POST.get('timeto')
#         user_id = request.session.get('uid')  # Assuming 'uid' contains the USER ID


#         # Create a booking
#         booking = Booking.objects.create(
#             SCHEDULE_id=schedule_id,
#             USER_id=user_id,
#             dateofbooking=formatted_date,
#             Status='success'
#         )


#         messages.success(request, 'Appointment booked successfully.')
#         return redirect('booking_confirmation')  # Redirect to a confirmation page

#     return redirect('display_schedule')
    




    
        
