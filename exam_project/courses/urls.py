from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/create/', views.course_create, name='course_create'),
    path('course/<int:pk>/edit/', views.course_update, name='course_update'),
    path('course/<int:pk>/delete/', views.course_delete, name='course_delete'),

    path('course/<int:course_id>/lesson/create/', views.lesson_create, name='lesson_create'),
    path('lesson/<int:pk>/edit/', views.lesson_update, name='lesson_update'),
    path('lesson/<int:pk>/delete/', views.lesson_delete, name='lesson_delete'),

    path('course/<int:course_id>/review/create/', views.review_create, name='review_create'),
]