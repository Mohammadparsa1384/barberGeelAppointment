from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from home.models import Contact
from .forms import ContactForm
# Create your views here.

class IndexView(generic.TemplateView):
    template_name = "home/index.html"

class AboutUsView(generic.TemplateView):
    template_name = "home/about_us.html"


class ContactView(generic.CreateView):
    model = Contact
    template_name = "home/contact-us.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    

def not_found(request, exception):
     return render(request,'404.html',status=404)