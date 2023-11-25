from django.contrib import admin
from django.urls import path,include 
from.import views 



urlpatterns = [
    path('', views.index,name="index"),
    path('doc_indexx/', views.doc_indexx,name="doc_indexx"),
    path('register_user/', views.register_user,name="register_user"),
    path('login_fun_page/', views.login_fun_page,name="login_fun_page"),
    path('landing_page/',views.landing_page,name="landing_page"),
    path('admin_home/', views.admin_home,name="admin_home"),
    path('adminmanage_doctor/', views.adminmanage_doctor,name="adminmanage_doctor"),
    path('adminmando_view/',views.adminmando_view,name="adminmando_view"),
    path('delete_doctor/<id>',views.delete_doctor,name="delete_doctor"),
    path('admin_update_doctor_details/<id>',views.admin_update_doctor_details,name="admin_update_doctor_details"),
    path('admin_update_doctor_details/<id>',views.admin_update_doctor_details,name="admin_update_doctor_details"),
    path('register_doctor/', views.register_doctor,name="register"),
    path('schedule_doctor/',views.schedule_doctor,name="schedule"),
    path('adminmanage_user/',views.adminmanage_user,name="adminmanage_user"),
    path('adminmanagepa_view/',views.adminmanpa_view,name="adminmanage_patient"),
    path('delete_user/<id>',views.delete_user,name="delete_user"),
    path('admin_update_user/<id>',views.admin_update_user,name="admin_update_user"),
    
    
    
    #path('schedule/', views.schedule_doctor, name="schedule_doctor"),

    
    path('schedule_form/',views.schedule_form,name="schedule_form"),

    
    path('home_patient/', views.home_patient,name="home_patient"),
    #path('doctor_search/', views.doctor_search, name="doctor_search"),


   

    path('schedule/', views.schedule_form, name='schedule_form'),


    
    path('view_slots/<doctor_id>/', views.view_slots, name='view_slots'),
    path('booking_doctor/<id>/', views.booking_doctor, name='booking_doctor'),
    # path('view_booking/<int:doctor_id>/', views.view_booking, name='view_booking'),
    path('mybookings/', views.view_mybooking, name='my-bookings'),
    path('logout/', views.logout_view, name='logout'),


]