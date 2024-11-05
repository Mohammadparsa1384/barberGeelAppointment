from . import views
from django.urls import path

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("about-us/", views.AboutUsView.as_view(),name="about"),
    path("contact/", views.ContactView.as_view(), name="contact")
]
