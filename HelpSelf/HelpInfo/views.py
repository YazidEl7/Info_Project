from django.shortcuts import render
from django.http import HttpResponse
from .models import Info


# Create your views here.


def index(request):
    information = Info.objects.all()  # [:5]
    output = '<br>'.join([f"{i.comp.comp_name} {i.user.user} {i.status.status} {i.ip.ip}" for i in information])
    return HttpResponse(output)
