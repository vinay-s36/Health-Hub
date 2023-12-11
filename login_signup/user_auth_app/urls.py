from django.urls import path
from .views import signup, login, index, add_new_blog, view_blog, successpage

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('addblog/', add_new_blog, name='addblog'),
    path('blogs/', view_blog, name='blogs'),
    path('success/', successpage, name='success'),
]
