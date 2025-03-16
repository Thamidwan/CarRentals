from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Car, Profile, Booking  # Assuming you have a Booking model
from django.utils import timezone

def home(request):
    return render(request, "Users/index.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('landing')  
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "Users/login.html")

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        phone_number = request.POST.get("phone_number")

        if password == confirm_password:
            try:
                user = User.objects.create_user(
                    username=username,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password
                )
                user.save()
                Profile.objects.create(user=user, phone_number=phone_number)
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('login') 
            except Exception as e:
                messages.error(request, f"Error creating account: {e}")
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, "Users/signup.html")

def userInfo(request):
    user = request.user  
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'unit_number': user.profile.unit_number if hasattr(user, 'profile') else None,
        'phone_number': user.profile.phone_number if hasattr(user, 'profile') else None,
    }
    return render(request, "Users/user_info.html", {'user': user_data})

def update_user_info(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.email = request.POST.get('email')

        if hasattr(user, 'profile'):
            user.profile.phone_number = request.POST.get('phone_number')
            user.profile.save()
        
        user.save()
        messages.success(request, "Your information has been updated successfully!")
        return redirect('user_info')  

    return redirect('user_info')  # Handle other methods

def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('home')

def landing(request):
    cars = Car.objects.filter(available=True)
    return render(request, "users/landing.html", {'cars': cars})

def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == "POST":
        return_date = request.POST.get("return_date")
        
        if return_date:
            booking = Booking.objects.create(
                user=request.user,
                car=car,
                return_date=timezone.datetime.strptime(return_date, '%Y-%m-%d')
            )
            car.available = False  # Mark the car as not available
            car.save()
            messages.success(request, "Car booked successfully!")
            return redirect('landing')
        else:
            messages.error(request, "Please provide a return date.")

    return render(request, "book_car.html", {'car': car})

def profile(request):
    return render(request, "Users/profile.html", {'user': request.user})

def booked_cars(request):
    user = request.user
    booked_cars = Booking.objects.filter(user=user).select_related('car')
    return render(request, "users/bookedCars.html", {'booked_cars': booked_cars})

def cancel_booking(request, car_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, car_id=car_id, user=request.user)
        booking.delete()
        messages.success(request, "Booking cancelled successfully.")
        return redirect('booked_cars')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Car, Profile, Booking  # Assuming you have a Booking model
from django.utils import timezone

def home(request):
    return render(request, "Users/index.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('landing')  
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "Users/login.html")

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        phone_number = request.POST.get("phone_number")

        if password == confirm_password:
            try:
                user = User.objects.create_user(
                    username=username,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password
                )
                user.save()
                Profile.objects.create(user=user, phone_number=phone_number)
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('login') 
            except Exception as e:
                messages.error(request, f"Error creating account: {e}")
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, "Users/signup.html")

def userInfo(request):
    user = request.user  
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'unit_number': user.profile.unit_number if hasattr(user, 'profile') else None,
        'phone_number': user.profile.phone_number if hasattr(user, 'profile') else None,
    }
    return render(request, "Users/user_info.html", {'user': user_data})

def update_user_info(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.email = request.POST.get('email')

        if hasattr(user, 'profile'):
            user.profile.phone_number = request.POST.get('phone_number')
            user.profile.save()
        
        user.save()
        messages.success(request, "Your information has been updated successfully!")
        return redirect('user_info')  

    return redirect('user_info')  # Handle other methods

def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('home')

def landing(request):
    cars = Car.objects.filter(available=True)
    return render(request, "users/landing.html", {'cars': cars})

def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == "POST":
        return_date = request.POST.get("return_date")
        
        if return_date:
            booking = Booking.objects.create(
                user=request.user,
                car=car,
                return_date=timezone.datetime.strptime(return_date, '%Y-%m-%d')
            )
            car.available = False  # Mark the car as not available
            car.save()
            messages.success(request, "Car booked successfully!")
            return redirect('landing')
        else:
            messages.error(request, "Please provide a return date.")

    return render(request, "book_car.html", {'car': car})

def profile(request):
    return render(request, "Users/profile.html", {'user': request.user})

def booked_cars(request):
    user = request.user
    booked_cars = Booking.objects.filter(user=user).select_related('car')
    return render(request, "users/bookedCars.html", {'booked_cars': booked_cars})

def cancel_booking(request, car_id):
    if request.method == 'POST':
        # Get the booking associated with the car and user
        booking = get_object_or_404(Booking, car_id=car_id, user=request.user)
        booking.delete()  # Delete the booking
        messages.success(request, "Booking cancelled successfully.")
        return redirect('booked_cars')

    return redirect('booked_cars')  # Redirect if not a POST request
