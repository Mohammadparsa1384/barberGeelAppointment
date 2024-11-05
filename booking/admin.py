from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from . import models
from jalali_date.admin import ModelAdminJalaliMixin
from django.contrib import messages
# Register your models here.

admin.site.site_title = "پنل مدیریت وبسایت آرایشی جیل"
admin.site.site_header = "پنل مدیریت وبسایت آرایشی جیل"
admin.site.site_url = "پنل ادمین"

@admin.register(models.Service)
class ServiceInline(admin.ModelAdmin):
    list_display = ["title","price"]

@admin.register(models.Appointment)
class AppointmentAdmin(ModelAdminJalaliMixin ,admin.ModelAdmin):

    def delete_button(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label,  obj._meta.model_name),  args=[obj.id])
        return format_html('<a class="btn" href="{}">حذف</a>', delete_url)
        
    delete_button.short_description = "حذف"
    
    def get_services(self, obj):
        return "--".join([p.title for p in obj.services.all()])
    
    get_services.short_description = "سرویس ها"

    list_display = ["customer","get_services","date","first_name","last_name","phone_number","time","created","is_paid","delete_button"]

    