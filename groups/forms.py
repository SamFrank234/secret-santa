from django import forms
from django.forms import SelectDateWidget, PasswordInput, EmailInput
from django.core.exceptions import ValidationError
from .models import *
from datetime import date

class CreatePartyForm(forms.ModelForm):
    
    class Meta:
        model = Party
        fields = '__all__'
        widgets = {
            'password': PasswordInput,
            'join_deadline': SelectDateWidget,
            'exchange_date': SelectDateWidget,
        }

    def clean(self):
        cleaned_data = super(CreatePartyForm, self).clean()
        join_deadline = cleaned_data['join_deadline']
        if join_deadline < date.today():
            raise ValidationError("Must Select a Join Deadline in the Future")
        exchange_date = cleaned_data['exchange_date']
        if exchange_date < join_deadline:
            raise ValidationError("Must Select an Exchange Date on or after the Join Deadline")
        return cleaned_data
    


class CreateSantaForm(forms.ModelForm):
    class Meta:
        model = Santa
        exclude = ['party', 'recipient']
        widgets = {
            'email_address': EmailInput,
        }

class PasswordForm(forms.Form):
    password = forms.CharField(max_length=30, widget=PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if not Party.objects.filter(password=data).exists():
            raise ValidationError("Your Password Does Not Match Any Secret Santa Parties")
        return data