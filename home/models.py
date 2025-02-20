from django.db import models

# Create your models here.

class Contact(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="نام و نام خاندوادگی")
    email = models.EmailField(verbose_name="ایمیل")
    phone_number = models.CharField(max_length=15,verbose_name="شماره تلفن")
    subject = models.CharField(max_length=20,verbose_name="موضوع")
    msg = models.TextField(verbose_name="پیام")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "تماس"
        verbose_name_plural = "تماس ها"