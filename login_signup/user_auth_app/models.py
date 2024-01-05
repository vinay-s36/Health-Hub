from django.db import models


class UserProfile(models.Model):
    user_type_choices = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    user_type = models.CharField(max_length=10, choices=user_type_choices)
    specialization = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username


class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('Mental Health', 'Mental Health'),
        ('Heart Disease', 'Heart Disease'),
        ('Covid19', 'Covid19'),
        ('Immunization', 'Immunization'),
    ]

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    # author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={
    #                            'user_type': 'doctor'})
    content = models.TextField()
    summary = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField()
    is_draft = models.BooleanField(default=False)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title


class Appointments(models.Model):
    doctor = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50)
    patient = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.doctor + ' - ' + self.patient
