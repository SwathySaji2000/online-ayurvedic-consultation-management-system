from django.contrib import admin
from django.urls import path,include 
from.import views 



urlpatterns = [



    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('enter_otp',views.enter_otp,name='enter_otp'),
    path('new_password',views.new_password,name='new_password'),

    path('', views.index,name="index"),
    path('patient_index/', views.patient_index,name="patient_index"),
    path('doctor_index/', views.doctor_index,name="doctor_index"),
    path('seller_index/',views.seller_index,name="seller_index"),
    path('register_user/', views.register_user,name="register_user"),
    path('register_seller/',views.register_seller,name="register_seller"),
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
    #path('adminschedule/<id>',views.adminschedule,name="adminschedule"),
    path('demoschedule/',views.demoschedule,name="demoschedule"),
    path('prescription/<id>',views.doctor_add_prescription,name="prescription"),
    path('user_view_pres/',views.user_view_pres,name="user_view_pres"),
    #path('schedule/', views.schedule_doctor, name="schedule_doctor"),

    
    path('schedule_form/',views.schedule_form,name="schedule_form"),

    
    path('home_patient/', views.home_patient,name="home_patient"),
    #path('doctor_search/', views.doctor_search, name="doctor_search"),


   

    path('schedule/', views.schedule_form, name='schedule_form'),
   
    
    path('view_slots/<doctor_id>/', views.view_slots, name='view_slots'),
    path('booking_doctor/<id>/', views.booking_doctor, name='booking_doctor'),
    # path('view_booking/<int:doctor_id>/', views.view_booking, name='view_booking'),
    path('mybookings/', views.view_mybooking, name='my-bookings'),
    path('doctor_page/',views.doctor_page,name="doctor_page"),
    path('payment_check/<b_id>/',views.payment_check, name="payment_check"),



    path('patient_profile',views.patient_profile, name='patient_profile'),
    path('doctor_profile',views.doctor_profile, name='doctor_profile'),
    
    path('category_page/', views.category_product, name="category_product"),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('ayurproduct_list/',views. product_list, name='product_list'),
    path('added_product/',views. added_products, name='product_display'),
    path('edit_product/<int:product_id>/', views.update_product_details, name='update_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),  
    
    path('search_result/', views.search_products, name='search_products'),
    
    path('add_subcategory/',views.sub_category,name="sub_category"),
    
    # path('patient_product_list/', views.patient_product_list, name='patient_product_list'),
   
    path('patient_product_list/', views.patient_product_list, name='patient_product_list'),
    path('user_add_product_to_carts1/<pid>/<pname>/<rate>/<quantity>',views.user_add_product_to_carts1),
    path('user_view_cartdetailspdt/<id>',views.user_view_cartdetailspdt,name = 'user_view_cartdetails'),
    path('user_view_cart_pdt/',views.user_view_cart_pdt, name='user_view_cart_pdt'),

















    #path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    # path('remove-from-cart/<int:product_id>/',views. remove_from_cart, name='remove-from-cart'),
    # path('cart/',views.view_cart, name='cart'),
    # path('increase-cart-item/<int:product_id>/', views.increase_cart_item, name='increase-cart-item'),
    # path('decrease-cart-item/<int:product_id>/', views.decrease_cart_item, name='decrease-cart-item'),
    #  path('checkout/<int:product_id>/', views.checkout, name='checkout'),


    

    
    
    
    # path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # path('checkout/', views.checkout_view, name='checkout'), 
    # path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    # path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    # path('cart/',views.cart_view, name='cart'),
    # path('increase-cart-item/<int:product_id>/', views.increase_cart_item, name='increase-cart-item'),
    # path('decrease-cart-item/<int:product_id>/', views.decrease_cart_item, name='decrease-cart-item'),
    # path('checkout/', views.checkout_view, name='checkout'),
    # path('product/<int:product_id>/add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    # path('purchase/', views.purchase, name='purchase'),
    # path('addtocart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('logout/', views.logout_view, name='logout'),


]