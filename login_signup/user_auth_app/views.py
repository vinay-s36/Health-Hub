from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from .models import UserProfile, Blog
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
                    doctor_info = user
                    return render(request, 'user_auth_app/dashboard_doctor.html', {'username': username, 'doctor_info': [doctor_info]})
                    # return redirect('/dashboard_doctor/')
                elif user.user_type == 'patient':
                    # patient_info = user
                    return render(request, 'user_auth_app/dashboard_patient.html', {'username': username})
                    # return redirect('/dashboard_patient/')
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
            return render(request, 'user_auth_app/addblog.html', {'username': username})
        else:
            return redirect('/success/')

    return render(request, 'user_auth_app/addblog.html', {'username': username})


def successpage(request):
    return render(request, 'user_auth_app/successful.html')


def view_blog(request):
    posted_blogs = Blog.objects.filter(is_draft=False)
    draft_blogs = Blog.objects.filter(is_draft=True)
    return render(request, 'user_auth_app/blogs.html', {'posted_blogs': posted_blogs, 'draft_blogs': draft_blogs})
