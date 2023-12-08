from django.urls import path
from .views import signup, dashboard_patient, dashboard_doctor, login, index

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('dashboard_patient/', dashboard_patient, name='dashboard_patient'),
    path('dashboard_doctor/', dashboard_doctor, name='dashboard_doctor'),
]
