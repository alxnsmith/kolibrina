from django.shortcuts import redirect
from .forms import AvatarForm


def avatarUpload(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        form.instance.user = request.user
        try:
            if form.is_valid():
                form.save()
        except: pass
    return redirect('account')