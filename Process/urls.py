from django.urls import path
from . import views
from .change import process_change

urlpatterns = [
    path("",views.home,name="welcome"),
    path('process_resume/', views.process_resume, name='handle_request'),
    path('process_change/', process_change, name="handle_change"), 
    path('verify_api/', views.verify_api, name='verify_api'),
]

