from django import forms
# from .models import Comanda
from romani.models import UserProfile, Comanda
from django.contrib.auth.models import  User

class ComandaForm(forms.ModelForm):
    class Meta:
        model = Comanda
        exclude = ("entregat","cancelat","data_comanda","data_entrega", "lloc_entrega", "franja_horaria", "client", "preu", "format", "producte", "cantitat", "primera_entrega", "data_entrega_txt")


class InfoForm(forms.ModelForm):
   class Meta:
        model = Comanda
        exclude = ("entregat","cancelat","data_comanda", "franja_horaria", "lloc_entrega", "client","preu", "format", "data_entrega_txt")


class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    email = forms.EmailField()
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = UserProfile
        exclude = ("user","invitacions", "bio","convidats")

    def save(self, *args, **kwargs):
      """
      Update the primary email address on the related User object as well.
      """
      u = self.instance.user
      u.email = self.cleaned_data['email']
      u.username = self.cleaned_data['username']
      u.first_name = self.cleaned_data['first_name']
      u.last_name = self.cleaned_data['last_name']
      u.save()
      profile = super(UserProfileForm, self).save(*args,**kwargs)
      return profile

