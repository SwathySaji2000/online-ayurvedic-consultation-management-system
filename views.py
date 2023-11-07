
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
from . models import *
#from django.contrib.auth.models import User

def index(request):
    return render(request, 'index.html')

def login_fun(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            q = Login.objects.get(username=username, password=password)
            request.session['id'] = q.pk
            if q:
                if q.type == 'admin':
                    return HttpResponse("<script>alert('login successful');window.location='/admin_home'</script>")
                elif q.type == 'doctor':
                    q3 = Doctors.objects.get(LOGIN_id=request.session['id'])
        
                    if q3:
                        request.session['f_id'] = q3.pk
                        print("============================,",request.session['f_id'])
                    return HttpResponse("<script>alert('login successful');window.location='/doctor_home'</script>")
                elif q.type == 'user':
                    qr = Users.objects.get(LOGIN_id=request.session['id'])
                    if qr:
                        request.session['uid'] = qr.pk
                    return HttpResponse("<script>alert('login successful');window.location='/landing_page'</script>")
        except:
            return HttpResponse("<script>alert('Invalid Username or Password');window.location='login'</script>")       
    return render(request, 'login_fun.html')


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
        return HttpResponse("<script>alert('User registration successfully');window.location='/login_fun'</script>") 
    return render(request,'register_user.html')

def register_doctor(request):
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

def delete_patient(request,id):
    docviews=Users.objects.filter(LOGIN_id=id)
    docviews.delete()
    qr=Login.objects.get(id=id)
    qr.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/admin_home'</script>")












def admin_home(request):
   return render(request, 'admin_home.html')





    
        
