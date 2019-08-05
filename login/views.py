from django.shortcuts import render
from .forms import UserRegistrationForm
from django.views.generic import DetailView
from chatting.models import Room


class DashboardView(DetailView):

    def get(self, request, *args, **kwargs):
        return render(request, 'chat/index.html', {})


class RegistrationView(DetailView):

    form = UserRegistrationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'account/dashboard.html', {})
        return render(request, 'account/register.html', {"user_form": self.form()})

    def post(self, request, *args, **kwargs):

        form = self.form(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password_first"])
            new_user.save()
            new_user.rooms.add(Room.get_default_chat())
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
