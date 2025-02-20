from django import template
from booking.models import Service

register = template.Library()

@register.inclusion_tag("booking/services_list.html")
def services_list():
    services = Service.objects.all()
    return {"services":services}

@register.inclusion_tag("booking/services_detail_list.html")
def services_detail_list():
    services = Service.objects.all()
    return {"services":services}
