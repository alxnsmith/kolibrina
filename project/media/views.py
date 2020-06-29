from django.shortcuts import redirect
from .forms import AvatarForm


def avatarUpload(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
    return redirect('account')