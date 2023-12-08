from django.shortcuts import render, redirect
from .models import UserProfile
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.hashers import make_password, check_password


def index(request):
    return render(request, 'user_auth_app/index.html')


def signup(request):
    if request.method == 'POST':
        try:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            profilepic = request.POST['profilepicture']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirmpassword']
            address_line1 = request.POST['addressline1']
            city = request.POST['city']
            state = request.POST['state']
            pincode = request.POST['pincode']
            user_type = request.POST['usertype']

            if UserProfile.objects.filter(username=username).exists():
                return render(request, 'user_auth_app/signup.html', {'error': "Username already exists. Please choose a different one."})

            if password == confirm_password:
                hashed_password = make_password(password)
                user = UserProfile(first_name=firstname, last_name=lastname, profile_picture=profilepic, username=username,
                                   email=email, password=hashed_password, address_line1=address_line1, city=city, state=state,
                                   pincode=pincode, user_type=user_type)
                user.save()
                return redirect('/login/')
            else:
                print("Passwords don't match")
                return render(request, 'user_auth_app/signup.html', {'error': "Passwords Don't Match!"})
        except MultiValueDictKeyError as e:
            print(f"KeyError: {e}")
            return render(request, 'user_auth_app/signup.html', {'error': "Some form fields are missing."})
    else:
        return render(request, 'user_auth_app/signup.html')


def login(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            entered_password = request.POST['password']

            try:
                user = UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist:
                return render(request, 'user_auth_app/login.html', {'error': "Invalid Credentials!"})

            if check_password(entered_password, user.password):
                if user.user_type == 'doctor':
                    return redirect('/dashboard_doctor/')
                elif user.user_type == 'patient':
                    return redirect('/dashboard_patient/')
                else:
                    return render(request, 'user_auth_app/login.html', {'error': "Invalid user type."})
            else:
                return render(request, 'user_auth_app/login.html', {'error': "Invalid Credentials!"})

        except MultiValueDictKeyError as e:
            print(f"KeyError: {e}")
            return render(request, 'user_auth_app/login.html', {'error': "Some form fields are missing."})
    else:
        return render(request, 'user_auth_app/login.html')


def dashboard_patient(request):
    patient_info = UserProfile.objects.filter(user_type='patient')
    return render(request, 'user_auth_app/dashboard_patient.html', {'patient_info': patient_info})


def dashboard_doctor(request):
    doctor_info = UserProfile.objects.filter(user_type='doctor')
    return render(request, 'user_auth_app/dashboard_doctor.html', {'doctor_info': doctor_info})
