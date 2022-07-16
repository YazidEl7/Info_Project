import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import Info, Track
from django.utils.html import escape
from django.http import HttpResponseRedirect, HttpRequest
from datetime import datetime


# Create your views here.
def m(request):
    ret = True
    if not request.user.is_authenticated:
        ret = HttpResponseRedirect('/login/')
    if request.user.is_authenticated:
        ret = HttpResponseRedirect('/Home')
    return ret


def between(request):
    if request.user.is_authenticated:
        logged = request.META

        l_u = open("HelpInfo/static/Dynamic/logged_users.json", "r+")
        # read_l_u = l_u.read()
        occ_count = len(l_u.readlines()) - 2
        values = f'\"USERNAME\" : \"{logged["USERNAME"]}\", ' + f'\"IP\" : \"{logged["REMOTE_ADDR"]}\", ' \
                 + f'\"Host\" : \"{logged["REMOTE_HOST"]}\", ' + f'\"USERDOMAIN\" : \"{logged["USERDOMAIN"]}\", ' \
                 + f'\"COMPUTER\" : \"{logged["COMPUTERNAME"]}\", ' + f'\"OS\" : \"{logged["OS"]}\", ' \
                 + f'\"DATE\" : \"{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\", ' \
                 + f'\"AGENT\" : \"{logged["HTTP_USER_AGENT"]}\" '
        if occ_count == 0:
            logged_user = "{" + values + "}" + "\n]"
        else:
            logged_user = ",{" + values + "}" + " \n]"

        def get_size(fileobject):
            fileobject.seek(0, 2)  # move the cursor to the end of the file
            size = fileobject.tell()
            return size

        # and then
        fsize = get_size(l_u)
        l_u.truncate(fsize - 1)
        l_u.close()
        l_u = open("HelpInfo/static/Dynamic/logged_users.json", "a+")
        l_u.write(logged_user)
        l_u.close()

    return HttpResponseRedirect('/Home')


def data(request):
    if request.user.is_authenticated:
        information = Info.objects.all()  # [:5]
        # output = '<br>'.join([f"{i.comp.comp_name} {i.user.user} {i.status.status} {i.ip.ip}" for i in information])
        output1 = {'Computers': information}
        return render(request, 'HelpInfo/data.html', output1)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')


def logs(request):
    if request.user.is_authenticated:
        jopen = open("HelpInfo/static/Dynamic/logged_users.json", "r")
        jload = json.loads(jopen.read())
        obj = {'objet': jload}
        return render(request, 'HelpInfo/logs.html', obj)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')


def users_history(request):
    if request.user.is_authenticated:
        information = Track.objects.all()  # [:5]
        output2 = {'Computers': information}
        return render(request, 'HelpInfo/users_history.html', output2)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
