from django.shortcuts import render, redirect, HttpResponse
from . import forms, level
from userK.models import CustomUser as User
from media import forms as media
from django.conf import settings
import os

# class account(FormView):
#     form_class = forms.EditUser
#     success_url = "/account/"
#     template_name = "userK/account.html"

# def account(request):
#     return HttpResponse('{{ forms.EditUser.as_p }}')


def account(request):
    if request.user.is_authenticated:
        uDir = str(settings.MEDIA_ROOT).replace('\\', '/') + 'user_' + str(request.user)
        ava = '/' +  uDir.split('/')[-3] + '/' + uDir.split('/')[-2] + '/' + uDir.split('/')[-1] + '/' + os.listdir(uDir)[0]
        userID = str(request.user.id).rjust(7, '0')
        u = User.objects.get(id=request.user.id)
        # firstName = str(User.objects.get(request.user)[0])
        if request.POST:
            form = forms.EditUser(initial={
                'birthday': request._post['birthday'], 'gender': request._post['gender'],
                'country': request._post['country'],'area': request._post['area'], 'city': request._post['city'],

            })
            for n, i in enumerate(request._post):
                if n == 3:
                    if i != 'hideMyName':
                        u.__dict__['hideMyName'] = False
                    else:
                        u.__dict__['hideMyName'] = True

                if n > 0:
                    if n != 3:
                        u.__dict__[i] = request._post[i]
            u.save()
            return redirect('account')
        else:
            form = forms.EditUser(initial={
                'birthday': u.__dict__['birthday'].__format__('%Y-%m-%d'), 'gender': u.gender, 'country': u.country,
                'area': u.__dict__['area'], 'city': u.__dict__['city'],
            })
            return render(
                request, 'userK/account.html',
                {
                    'userID': userID, 'gender': u.__dict__['gender'],
                    'form': form, 'req': request.POST, 'r': request.user,
                    'level': level.op(u), 'AvatarForm': media.AvatarForm(initial={'user': request.user, }),
                    'AvatarImage': ava,
                }
            )
    else:
        return redirect('login')