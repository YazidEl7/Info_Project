from django.shortcuts import render
from django.http import HttpResponse
from .models import Info
from django.utils.html import escape
from django.http import HttpResponseRedirect, HttpRequest


# Create your views here.
def login(request):
    return HttpResponseRedirect('/login/')


def data(request):
    information = Info.objects.all()  # [:5]
    # output = '<br>'.join([f"{i.comp.comp_name} {i.user.user} {i.status.status} {i.ip.ip}" for i in information])
    output1 = {'Computers': information}
    logged = request.META

    l_u = open("HelpInfo/Dynamic/logged_users.json", "r+")
    # read_l_u = l_u.read()
    occ_count = len(l_u.readlines()) - 2
    values = f'\"USERNAME\" : \"{logged["USERNAME"]}\", ' + f'\"IP\" : \"{logged["REMOTE_ADDR"]}\", ' \
             + f'\"Host\" : \"{logged["REMOTE_HOST"]}\", ' + f'\"USERDOMAIN\" : \"{logged["USERDOMAIN"]}\", ' \
             + f'\"COMPUTER\" : \"{logged["COMPUTERNAME"]}\", ' + f'\"OS\" : \"{logged["OS"]}\", ' \
             + f'\"AGENT\" : \"{logged["HTTP_USER_AGENT"]}\" '
    if occ_count == 0:
        logged_user = "\"count" + str(occ_count+1) + "\" :{ " + values + " }" + "\n }"
    else:
        logged_user = ", \"count" + str(occ_count+1) + "\" :{ " + values + " }" + "\n }"

    def get_size(fileobject):
        fileobject.seek(0, 2)  # move the cursor to the end of the file
        size = fileobject.tell()
        return size

    # and then
    fsize = get_size(l_u)
    l_u.truncate(fsize - 1)
    l_u.close()
    l_u = open("HelpInfo/Dynamic/logged_users.json", "a+")
    l_u.write(logged_user)
    l_u.close()

    return render(request, 'HelpInfo/data.html', output1)


def logs(request):
    return render(request, 'HelpInfo/logs.html')


def users_history(request):
    return render(request, 'HelpInfo/users_history.html')
