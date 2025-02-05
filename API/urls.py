from django.urls import path
from . import views

urlpatterns=[
    path("API/",views.EndPointListCreate.as_view(),name="ats-score-check"),
    path(
        "API/<int:pk>",
        views.EndPointRetriveUpdateDestroy.as_view(),name='update'

         )
]