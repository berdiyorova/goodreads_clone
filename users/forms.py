from django import forms

from users.models import CustomUser


class UserCreateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit)  # parent classni save() metodi bizga userni yaratib beradi.
        user.set_password(self.cleaned_data['password'])  # set_password() - parolni bazaga xeshlab keyin saqlaydi.

        user.save()
        return user



class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'photo')
