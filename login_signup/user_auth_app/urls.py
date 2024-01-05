from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import appointment_list, signup, login, index, add_new_blog, view_blog, patients_view_blog, patient_dashboard, doctor_dashboard, blog_details_1, blog_details_2, update_blog_draft_status, delete_blog, book_appointment

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('patient-dashboard/', patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', doctor_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/addblog/', add_new_blog, name='addblog'),
    path('doctor-dashboard/blogs/', view_blog, name='blogs'),
    path('doctor-dashboard/blogs/blog-details-1/<int:id>/',
         blog_details_1, name='blog_details_1'),
    path('patient-dashboard/blogs/blog-details-2/<int:id>/',
         blog_details_2, name='blog_details_2'),
    path('patient-dashboard/view-blogs/',
         patients_view_blog, name='patient_blogs'),
    path('update-draft-status/<int:blog_id>/', update_blog_draft_status,
         name='update_blog_draft_status'),
    path('delete-blog/<int:blog_id>/', delete_blog,
         name='delete_blog'),
    path('patient-dashboard/book-appointment/',
         book_appointment, name='book_appointment'),
    path('patient-dashboard/appointment-list/',
         appointment_list, name='appointment_list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
