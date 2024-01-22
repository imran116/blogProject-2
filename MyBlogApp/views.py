from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import HttpResponseRedirect, HttpResponse, render
from django.urls import reverse


def Index(request):
    return HttpResponseRedirect(reverse('blog_app:blog_home'))


@login_required
def password_change(request,id):
    current_user = request.user
    pass_change = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            pass_change = True

    context = {
        'form': form,
        'pass_change': pass_change,
    }
    return render(request, 'loginApp/password_change.html', context=context)
