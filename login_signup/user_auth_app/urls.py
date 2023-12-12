from django.urls import path
from .views import signup, login, index, add_new_blog, view_blog, successpage, patients_view_blog, patient_dashboard, doctor_dashboard

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('patient-dashboard/', patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', doctor_dashboard, name='patient_dashboard'),
    path('addblog/', add_new_blog, name='addblog'),
    path('blogs/', view_blog, name='blogs'),
    path('success/', successpage, name='success'),
    path('view-blogs/', patients_view_blog, name='patient_blogs'),
]
