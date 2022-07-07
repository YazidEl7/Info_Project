from django.shortcuts import render
from django.http import HttpResponse
from .models import Info
from django.utils.html import escape
from django.http import HttpResponseRedirect


# Create your views here.
def login(request):
    return HttpResponseRedirect('/login/')


def data(request):
    information = Info.objects.all()  # [:5]
    output = '<br>'.join([f"{i.comp.comp_name} {i.user.user} {i.status.status} {i.ip.ip}" for i in information])
    output1 = {'Computers': information}
    return render(request, 'HelpInfo/data.html', output1)


def logs(request):
    return render(request, 'HelpInfo/logs.html')


def users_history(request):
    return render(request, 'HelpInfo/users_history.html')
