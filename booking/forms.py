from django import forms 
from .models import Appointment, Service
from jalali_date.fields import JalaliDateField 
from jalali_date import date2jalali
from jalali_date.widgets import AdminJalaliDateWidget 
from django.forms.widgets import TimeInput
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import time
class AppointMentForm(forms.ModelForm):

    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.SelectMultiple(attrs={
            "class":"select2",
            }),
        label="سرویس ها"
    )
    class Meta:
        model = Appointment
        fields = ['services', 'phone_number' ,'first_name','last_name','date', 'time']

    def __init__(self, *args, **kwargs):

        

        super(AppointMentForm, self).__init__(*args, **kwargs)

        self.fields['date'] = JalaliDateField(label=('تاریخ'), 
            widget=AdminJalaliDateWidget() 
        )

        self.fields['time'].widget = TimeInput(
            attrs= {"class":"form-control","type":"time"}
        )

        self.fields['date'].widget.attrs.update({'class': 'jalali_date-date form-control'})

        

        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control'  
        })

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control'  
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control'  
        })
    

    def clean(self):
        cd_data = super().clean()
        date = self.cleaned_data.get("date")
        time_input = self.cleaned_data.get("time")

        

        if date and date < timezone.now().date():
            raise ValidationError("تاریخ نمی‌تواند قبل از تاریخ امروز باشد.")
        
        if date == timezone.now().date() and time_input <= timezone.now().time():
            raise ValidationError("نمی‌توانید برای ساعت‌های گذشته در امروز نوبت بگیرید.")

        start_time = time(9,0)
        end_time = time(22, 0 )

        if time_input and (time_input < start_time or time_input > end_time):
            raise ValidationError("ساعت انتخابی باید بین 9 صبح تا 10 شب باشد.")
              

        jalali_date = date2jalali(date).strftime('%Y/%m/%d')

        appointment_count = Appointment.objects.filter(date=date).count()

        if Appointment.objects.filter(date=date,time=time_input).exists():
            raise ValidationError(f"تاریخ {jalali_date} و زمان {time_input} قبلاً رزرو شده است. لطفاً زمان دیگری انتخاب کنید.")
        

        if appointment_count >= 7 :
            raise ValidationError(f"در تاریخ {date}، ظرفیت نوبت‌دهی تکمیل است. لطفاً تاریخ دیگری انتخاب کنید.")
        
        return cd_data   



    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        if not phone_number.isdigit():
            raise ValidationError("شماره تلفن باید عدد باشد")

        if len(phone_number) != 11:
            raise ValidationError("شماره تماس باید 11 رقم باشد")
        
         
        if not phone_number.startswith("09"):
            raise ValidationError("شماره تلفن باید با 09 شروع شود")

        
        return phone_number