from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Route for course list
    path('', views.CourseListView.as_view(), name='index'),

    # Route for course detail
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),

    # Route for enrolling course
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),

    # <HINT> Route for submit view
    path('<int:course_id>/submit/', views.submit, name='submit'),

    # <HINT> Route for show_exam_result view
    path('<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
