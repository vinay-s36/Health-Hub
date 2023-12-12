from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
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
                    # doctor_info = user
                    # return render(request, 'user_auth_app/dashboard_doctor.html', {'username': username, 'doctor_info': [doctor_info]})
                    redirect_url = f'/doctor-dashboard/?username={username}'
                    return redirect(redirect_url)

                elif user.user_type == 'patient':
                    # patient_info = user
                    # return render(request, 'user_auth_app/dashboard_patient.html', {'username': username, 'pateint_info': [patient_info]})
                    return redirect('/patient-dashboard/')

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
    return render(request, 'user_auth_app/dashboard_patient.html')


def doctor_dashboard(request):
    username = request.GET.get('username', None)
    return render(request, 'user_auth_app/dashboard_doctor.html', {'username': username})


def view_blog(request):
    username = request.GET.get('username', None)
    posted_blogs = Blog.objects.filter(is_draft=False, author=username)
    draft_blogs = Blog.objects.filter(is_draft=True, author=username)
    return render(request, 'user_auth_app/blogs.html', {'posted_blogs': posted_blogs, 'draft_blogs': draft_blogs, 'username': username})


def patients_view_blog(request):
    categories = Blog.objects.filter(is_draft=False).values_list(
        'category', flat=True).distinct()

    blog_categories = {}

    for category in categories:
        blogs_in_category = Blog.objects.filter(
            category=category, is_draft=False)
        blog_categories[category] = blogs_in_category

    return render(request, 'user_auth_app/patient_blogs.html', {'blog_categories': blog_categories})


def blog_details_1(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'user_auth_app/blog_details_1.html', {'blog': blog})


def blog_details_2(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'user_auth_app/blog_details_2.html', {'blog': blog})


def update_blog_draft_status(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)

    # Update the is_draft value
    blog.is_draft = False
    blog.save()

    redirect_url = f'/doctor-dashboard/?username={blog.author}'
    return redirect(redirect_url)
