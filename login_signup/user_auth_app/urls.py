from django.urls import path
from .views import signup, login, index

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', index, name='index'),
    path('login/', login, name='login'),
]
