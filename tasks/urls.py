from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('new_task/', views.new_task, name = "new_task"),
    path('update_task/', views.update_task, name = "update_task"),
    path('delete_task/', views.delete_task, name="delete_task"),
]