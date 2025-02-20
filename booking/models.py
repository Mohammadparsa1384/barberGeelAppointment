from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Service(models.Model):
    title = models.CharField(max_length=100,verbose_name="عنوان")
    desc = models.TextField(verbose_name="توضیحات")
    price = models.PositiveBigIntegerField(verbose_name="قیمت")
    slug = models.SlugField(verbose_name="اسلاگ",blank=True, null=True)
    image = models.ImageField(upload_to="services_image",blank=True,null=True, verbose_name="عکس")

    
    class Meta:
        verbose_name = "سرویس"
        verbose_name_plural = "سرویس ها"

    def get_absolute_url(self):
        return reverse("service_detail", args=[self.slug])
    

    def __str__(self):
        format_price = f"{self.price:,}"
        return f"{self.title} - {format_price} تومان "

class Appointment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE,related_name="appointments", verbose_name="مشتری")
    services = models.ManyToManyField(Service,verbose_name="خدمات")
    phone_number = models.CharField(max_length=11, verbose_name="شماره تلفن")
    first_name = models.CharField(max_length=30,null=True,verbose_name="نام")
    last_name = models.CharField(max_length=30,null=True,verbose_name="نام خانوادگی")
    is_paid = models.BooleanField(default=False,verbose_name="وضعیت پرداخت")
    date = models.DateField(verbose_name="تاریخ رزرو")
    time = models.TimeField(verbose_name="زمان رزرو")
    created = models.DateTimeField(auto_now_add=True,verbose_name="زمان ایجاد")

    class Meta:
        ordering = ["-is_paid"]
        verbose_name = "نوبت"
        verbose_name_plural = "نوبت ها"

    def calculate_total_price(self):
        total_price = sum(service.price for service in self.services.all())
        return total_price

    def __str__(self):
        return f'{self.customer} - {self.date} {self.time}'
    