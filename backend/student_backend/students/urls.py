from django.urls import path
from . import views


urlpatterns = [
    path('students/', views.get_students),
    path('students/add/', views.add_student),
    path('students/update/<int:id>/', views.update_student),
    path('students/delete/<int:id>/', views.delete_student),
    path('students/search/', views.search_students)
]