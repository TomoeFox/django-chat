from django import forms
from chatting.models import ChatUser


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password_first = forms.CharField(label='Password',
                                     widget=forms.PasswordInput)
    password_second = forms.CharField(label='Repeat password',
                                      widget=forms.PasswordInput)

    class Meta:
        model = ChatUser
        fields = ('username',)

    def clean_password_second(self):
        data = self.cleaned_data
        if data['password_first'] != data['password_second']:
            raise forms.ValidationError('Passwords don\'t match.')
        return data['password_first']
