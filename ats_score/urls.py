# ats_score/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.score, name='ats_score_generate'), 
    path('verify_api/',views.check,name="verify_api") 
]
