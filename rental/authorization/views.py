from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth import login

from .forms import CustomUserCreationForm, CustomLoginUserForm


class CreateUserView(generic.CreateView):
    template_name = 'authentication/registration-page.html'
    form_class = CustomUserCreationForm
    context_object_name = 'form'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        url_to_redirect = reverse_lazy('login')
        return redirect(url_to_redirect)


def login_user_view(request):
    if request.method == 'POST':
        form = CustomLoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('account')
    else:
        form = CustomLoginUserForm()
    context = {
        'form': form,
    }
    return render(request, template_name='authentication/login-page.html', context=context)


