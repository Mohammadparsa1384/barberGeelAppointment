from .models import Appointment
from django.dispatch import receiver
from django.db.models.signals import post_save
from jalali_date import date2jalali
from django.core.mail import send_mail
from django.conf import settings
@receiver(post_save, sender=Appointment)
def send_payment_success_email(sender, instance, created, *args, **kwargs):
    if instance.is_paid:
        jalali_date = date2jalali(instance.date).strftime("%Y/%m/%d")

        subject = "تأیید پرداخت نوبت"
        message = f"کاربر گرامی {instance.customer.first_name} عزیز،\n\nپرداخت شما برای نوبت در تاریخ {jalali_date} و ساعت {instance.time} با موفقیت انجام شد.\n\nبا تشکر از انتخاب شما."

        recipient_email = instance.customer.email

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )
