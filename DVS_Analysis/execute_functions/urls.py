from django.urls import path, include
from . import views


app_name = 'execute_functions'

urlpatterns = [
    path('', views.execute, name='execute'),
]
