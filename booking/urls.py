from . import views
from django.urls import path

urlpatterns = [
    path("", views.book_appointment, name="book"),
    path("success/<int:appointment_id>", views.appointment_success, name="book_suc"),
    path("service-detail/<slug:slug>/", views.service_detail, name="service_detail"),
    path('payment/<int:appointment_id>/', views.payment_page, name='payment_page'),
    path('payment/verify/', views.payment_verify, name='verify_payment'),
]
