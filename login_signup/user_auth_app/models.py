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

    def __str__(self):
        return self.username
