from datetime import datetime, time
import re
from googleapiclient.discovery import build
from google.oauth2 import service_account
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from .models import UserProfile, Blog, Appointments
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.hashers import make_password, check_password
import os
from django.conf import settings

BASE_DIR = settings.BASE_DIR

key_path = os.path.join(BASE_DIR, 'config', 'service_account_key.json')
credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=['https://www.googleapis.com/auth/calendar']
)


def index(request):
    return render(request, 'user_auth_app/index.html')


def signup(request):
    if request.method == 'POST':
        try:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            profilepic = request.FILES['profilepicture']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirmpassword']
            address_line1 = request.POST['addressline1']
            city = request.POST['city']
            state = request.POST['state']
            pincode = request.POST['pincode']
            user_type = request.POST['usertype']
            if user_type == 'doctor':
                specialization = request.POST['specialization']
            else:
                specialization = ''

            if UserProfile.objects.filter(username=username).exists():
                return render(request, 'user_auth_app/signup.html', {'error': "Username already exists. Please choose a different one."})

            if password == confirm_password:
                hashed_password = make_password(password)
                user = UserProfile(first_name=firstname, last_name=lastname, profile_picture=profilepic, username=username,
                                   email=email, password=hashed_password, address_line1=address_line1, city=city, state=state,
                                   pincode=pincode, user_type=user_type, specialization=specialization)
                user.save()
                return redirect('/login/')

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
                    redirect_url = f'/doctor-dashboard/?username={username}'
                    return redirect(redirect_url)

                elif user.user_type == 'patient':
                    return redirect(f'/patient-dashboard/?username={username}')

                else:
                    return render(request, 'user_auth_app/login.html', {'error': "Invalid user type."})
            else:
                return render(request, 'user_auth_app/login.html', {'error': "Invalid Credentials!"})

        except MultiValueDictKeyError as e:
            print(f"KeyError: {e}")
            return render(request, 'user_auth_app/login.html', {'error': "Some form fields are missing."})
    else:
        return render(request, 'user_auth_app/login.html')


def add_new_blog(request):
    username = request.GET.get('username', None)

    if username is None:
        return HttpResponseBadRequest("Username parameter missing.")

    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        is_draft = 'save_as_draft' in request.POST
        image_url = request.POST.get('image')

        Blog.objects.create(
            title=title,
            category=category,
            summary=summary,
            content=content,
            is_draft=is_draft,
            author=username,
            image_url=image_url,
        )

        if is_draft:
            redirect_url = f'/doctor-dashboard/?username={username}'
            return redirect(redirect_url)
        else:
            redirect_url = f'/doctor-dashboard/?username={username}'
            return redirect(redirect_url)

    return render(request, 'user_auth_app/addblog.html', {'username': username})


def patient_dashboard(request):
    try:
        username = request.GET.get('username', None)
        user = UserProfile.objects.get(username=username)
        return render(request, 'user_auth_app/dashboard_patient.html', {'user': user})
    except UserProfile.DoesNotExist:
        return HttpResponse("User not found", status=404)


def doctor_dashboard(request):
    try:
        username = request.GET.get('username', None)
        user = UserProfile.objects.get(username=username)
        return render(request, 'user_auth_app/dashboard_doctor.html', {'user': user})
    except UserProfile.DoesNotExist:
        return HttpResponse("User not found", status=404)


def view_blog(request):
    username = request.GET.get('username', None)
    posted_blogs = Blog.objects.filter(is_draft=False, author=username)
    draft_blogs = Blog.objects.filter(is_draft=True, author=username)
    return render(request, 'user_auth_app/blogs.html', {'posted_blogs': posted_blogs, 'draft_blogs': draft_blogs, 'username': username})


def patients_view_blog(request):
    username = request.GET.get('username', None)
    categories = Blog.objects.filter(is_draft=False).values_list(
        'category', flat=True).distinct()

    blog_categories = {}

    for category in categories:
        blogs_in_category = Blog.objects.filter(
            category=category, is_draft=False)
        blog_categories[category] = blogs_in_category

    return render(request, 'user_auth_app/patient_blogs.html', {'blog_categories': blog_categories, 'username': username})


def blog_details_1(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'user_auth_app/blog_details_1.html', {'blog': blog})


def blog_details_2(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'user_auth_app/blog_details_2.html', {'blog': blog})


def update_blog_draft_status(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)

    blog.is_draft = False
    blog.save()

    redirect_url = f'/doctor-dashboard/?username={blog.author}'
    return redirect(redirect_url)


def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    author = blog.author
    if request.method == "POST":
        blog.delete()

    redirect_url = f'/doctor-dashboard/?username={author}'
    return redirect(redirect_url)


def book_appointment(request):
    username = request.GET.get('username', None)
    doctor_info = UserProfile.objects.filter(user_type='doctor')

    if request.method == 'POST':
        doctor_username = request.POST.get('doctor-name')
        patient_username = request.POST.get('patient-name')
        specialization = request.POST.get('specialization')
        appointment_date = request.POST.get('appointment-date')
        start_time_str = request.POST.get('start-time')

        try:
            start_time = datetime.strptime(start_time_str, '%I:%M %p').time()
        except ValueError:
            return render(request, 'user_auth_app/book_appointment.html', {'doctor_info': doctor_info, 'username': username, 'error_message': 'Invalid time format'})

        end_time = calculate_end_time(start_time_str)
        appointments = Appointments(
            doctor=doctor_username,
            patient=patient_username,
            specialization=specialization,
            date=appointment_date,
            start_time=start_time,
            end_time=end_time
        )
        appointments.save()
        redirect_url = f'/patient-dashboard/appointment-list/?username={patient_username}'
        return redirect(redirect_url)

    return render(request, 'user_auth_app/book_appointment.html', {'doctor_info': doctor_info, 'username': username})


def calculate_end_time(start_time_str):
    start_hour, start_minute, period = re.match(
        r'(\d+):(\d+)\s*([APMapm]{0,2})', start_time_str).groups()
    start_hour, start_minute = int(start_hour), int(start_minute)

    if period and period.lower() == 'pm' and start_hour != 12:
        start_hour += 12

    total_minutes = start_hour * 60 + start_minute + 45

    end_hour = total_minutes // 60
    end_minute = total_minutes % 60

    end_time = time(end_hour, end_minute)

    return end_time


def appointment_list(request):
    patient_name = request.GET.get('username', None)
    appointments = Appointments.objects.filter(patient=patient_name)
    print(appointments)
    return render(request, 'user_auth_app/appointment_details.html', {'appointments': appointments, 'patient_name': patient_name})
