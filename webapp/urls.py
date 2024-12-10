from django.urls import path  # Use path() instead of url()
from . import views

urlpatterns = [
    path('addition/', views.add, name='addition'),  # Use path() for routing
    path('addData/', views.addData, name='addData'),  
]
