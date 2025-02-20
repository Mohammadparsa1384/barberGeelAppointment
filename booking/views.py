import requests
import threading
from datetime import datetime , timedelta


from django.urls import reverse
from django.shortcuts import  render ,get_object_or_404, redirect
from .forms import AppointMentForm
from .models import Service, Appointment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from jalali_date import date2jalali
from django.core.mail import send_mail

# Create your views here.

# use active timers  to disallow send email reminder when reservation delete by user
active_timers = {}

# send reminder email
def send_reminder_email(appointment_id):
    # get reminder with id 

    try:
        appointment = Appointment.objects.get(id=appointment_id)

    except Appointment.DoesNotExist:
        # If the appointment does not exist (deleted or invalid id), exit the function without any action
        return 

    jalali_date = date2jalali(appointment.date).strftime('%Y/%m/%d')
    subject = "یادآوری نوبت"
    message = f"یادآوری: نوبت شما برای تاریخ {jalali_date} و ساعت {appointment.time} است."
    recipient_list = [appointment.customer.email]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )


def schedule_reminder(appointment):
    # Get the current time
    now = timezone.now()
    # Extract the date and time from the appointment instance

    appointment_date = appointment.date 
    appointment_time = appointment.time

     # Combine date and time into a single datetime object
    appointment_time = datetime.combine(appointment_date , appointment_time)

    # Make the datetime object timezone-aware to match the current timezone
    appointment_time = timezone.make_aware(appointment_time, timezone.get_current_timezone())

    # Set the reminder time to 5 minutes before the actual appointment time
    reminder_time = appointment_time - timedelta(hours=2)

    # Calculate the delay (in seconds) until the reminder should be sent
    delay = (reminder_time - now).total_seconds()   

    # If the delay is positive (the reminder time is in the future), 
    # start a timer to send the reminder email after the specified delay
    if delay > 0:
        timer = threading.Timer(delay, send_reminder_email, [appointment.id])
        timer.start()


def cancel_appointment(appointment_id):
    # Check if the appointment has an active timer and cancel it if found
    if appointment_id in active_timers:
        timer = active_timers.pop(appointment_id)
        timer.cancel()
    
    try:
        # Attempt to retrieve the appointment from the database
        appointment = Appointment.objects.get(id=appointment_id)
        # Delete the appointment if it exists
        appointment.delete()

    except Appointment.DoesNotExist:
        # Handle the case where the appointment does not exist (do nothing)
        pass

@login_required
def book_appointment(request):
    if request.method == "POST":
        # Initialize the appointment form with the submitted data
        form = AppointMentForm(request.POST)
        if form.is_valid():
            # Create an appointment instance but do not save it yet
            appointment = form.save(commit=False)
            appointment.customer = request.user 
            appointment.save()
            # Save many-to-many relationships if any
            form.save_m2m()

            # Store the appointment ID in the session
            request.session['appointment_id'] = appointment.id
            # Update the user's first and last name with form data
            request.user.first_name = form.cleaned_data.get("first_name")
            request.user.last_name = form.cleaned_data.get("last_name")
            request.user.save()

            return redirect('book_suc', appointment_id=appointment.id)
    else:
        # If the request method is not POST, initialize an empty form
        form = AppointMentForm()

    return render(request, 'booking/appointment.html', {'form': form})


def appointment_success(request, appointment_id):
    # Retrieve the appointment for the logged-in user or return a 404 error if not found
    appointment = get_object_or_404(Appointment, id=appointment_id, customer=request.user)
    
    # Calculate the total price of the appointment
    total_price = appointment.calculate_total_price()

    
    return render(request, 'booking/appointment_success.html', {
        'appointment': appointment,
        'total_price': total_price,
    })



@login_required
def payment_page(request, appointment_id):
    
    appointment = get_object_or_404(Appointment, id=appointment_id, customer=request.user)
    total_price = appointment.calculate_total_price() * 10  

    
    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
    callback_url = request.build_absolute_uri(reverse('verify_payment')) 

    
    data = {
        'merchant_id': settings.ZARINPAL_MERCAHNTID,  
        'amount': total_price,
        'description': 'پرداخت نوبت آرایشگاه',
        'callback_url': callback_url,
    }
    headers = {'Content-Type': 'application/json'}
    
    # Send a request to Zarinpal for payment initiation
    response = requests.post(zarinpal_request_url, json=data, headers=headers)
    result = response.json()

    # If payment request is successful, redirect to the payment gateway
    if result['data']['code'] == 100:
      
        return redirect(f'https://www.zarinpal.com/pg/StartPay/{result["data"]["authority"]}')
    else:
        # If payment request fails, show an error message
        messages.error(request, "مشکلی در پرداخت به وجود آمد، لطفاً مجدداً تلاش کنید.")
        return redirect('appointment_success', appointment_id=appointment.id)


@login_required
def payment_verify(request):
    # Get payment authority and status from the request
    authority = request.GET.get('Authority')
    status = request.GET.get("Status")
    appointment_id = request.session.get('appointment_id')

    # Retrieve the appointment for the logged-in user
    appointment = get_object_or_404(Appointment, id=appointment_id, customer=request.user)
    
    # Convert the total price from Tomans to Rials
    total_price_toman = appointment.calculate_total_price()
    total_price_rial = total_price_toman * 10  

    zarinpal_verify_url = 'https://api.zarinpal.com/pg/v4/payment/verify.json'

    data = {
        'merchant_id': settings.ZARINPAL_MERCAHNTID,
        'amount': total_price_rial,
        'authority': authority
    }
    headers = {'Content-Type': 'application/json'}

    # Send a request to Zarinpal to verify the payment
    response = requests.post(zarinpal_verify_url, json=data, headers=headers)
    result = response.json()

    # Check if the payment was successful
    if status == 'OK' and result['data']['code'] == 100:
        # Mark the appointment as paid
        appointment.is_paid = True
        appointment.save()
        # Schedule a reminder for the appointment
        schedule_reminder(appointment)
        return render(request, 'booking/payment_verify.html', {'is_paid': True,'total_price':total_price_toman})
    
    else:
        # If payment verification fails, show the failure page
        return render(request, 'booking/payment_verify.html', {'is_paid': False})

def service_detail(request,slug):
    service =  get_object_or_404(Service, slug=slug)
    return render(request, 'booking/service_detail.html', {'service': service})