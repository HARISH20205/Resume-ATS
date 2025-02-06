from django.urls import path
from . import views

urlpatterns = [
    path('process_resume/', views.process_resume, name='handle_request'),
    path('verify_api/', views.verify_api, name='verify_api'),
]
