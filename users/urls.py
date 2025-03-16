from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
     path('', views.home, name='home'),                
    path('login/', views.login, name='login'),        
    path('signup/', views.signup, name='signup'),      
    path('logout/', views.signout, name='logout'), 
    path('userInfo/', views.userInfo, name='user_info'), 
    path('updateUserInfo/', views.update_user_info, name='update_user_info'),
    path('landing/', views.landing, name='landing'),
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('profile/', views.profile, name='profile'),
    path('booked_cars/', views.booked_cars, name='booked_cars'),
    path('cancel_booking/<int:car_id>/', views.cancel_booking, name='cancel_booking'),
]