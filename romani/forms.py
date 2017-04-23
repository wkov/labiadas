from django import forms
# from .models import Comanda
from romani.models import UserProfile, Comanda, Productor, Producte, DiaEntrega, Node, TipusProducte
from django.contrib.auth.models import  User
from django.forms.widgets import CheckboxSelectMultiple
import datetime

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
            # self.fields['email'].initial = self.instance.user.email
            # self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    # email = forms.EmailField()
    # username = forms.CharField(max_length=30)
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
      # u.email = self.cleaned_data['email']
      # u.username = self.cleaned_data['username']
      u.first_name = self.cleaned_data['first_name']
      u.last_name = self.cleaned_data['last_name']
      u.save()
      profile = super(UserProfileForm, self).save(*args,**kwargs)
      return profile



class ProductorForm(forms.ModelForm):

    class Meta:
        model = Productor
        fields = ("nom", "cuerpo", "adjunt")
        # exclude = ("")


class ProducteForm(forms.ModelForm):

    class Meta:
        model = Producte
        # fields = ("nom", "cuerpo", "adjunt", "responsable")
        exclude = ("productor", "karma_value", "datahora", "karma_date", "dies_entrega")

    def __init__(self, *args, **kwargs):

        super(ProducteForm, self).__init__(*args, **kwargs)

        self.fields["nodes"].widget = CheckboxSelectMultiple()
        self.fields["nodes"].queryset = Node.objects.all()
        self.fields["formats"].widget = CheckboxSelectMultiple()
        self.fields["formats"].queryset = TipusProducte.objects.filter(productor=self.instance.productor)



class ProducteDatesForm(forms.ModelForm):

    class Meta:
        model = Producte
        fields = ("nom", "dies_entrega", )
        # exclude = ("productor", "karma_value", "datahora", "karma_date")

    def __init__(self, *args, **kwargs):

        super(ProducteDatesForm, self).__init__(*args, **kwargs)

        self.fields["dies_entrega"].widget = CheckboxSelectMultiple()
        self.fields["dies_entrega"].queryset = DiaEntrega.objects.filter(date__gte=datetime.datetime.now())