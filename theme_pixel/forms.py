from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UsernameField
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from theme_pixel.models import *
from django.forms import widgets
from .models import *
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

class RegistrationForm(UserCreationForm):
  password1 = forms.CharField(
      label=_("Password"),
      required=True,
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'icon': 'fa-lock',}),
  )
  password2 = forms.CharField(
      label=_("Ripeti Password"),
      required=True,
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ripeti Password', 'icon': 'fa-lock',}),
  )

  accept_terms = forms.BooleanField(
      label=_("Accetto i termini e le condizioni"), 
      required=True,
      widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
  )

  def clean_first_name(self):
    first_name = self.cleaned_data['first_name']
    if not first_name:
        self.add_error('first_name', _("Il nome è obbligatorio"))
    return first_name

  def clean_last_name(self):
    last_name = self.cleaned_data['last_name']
    if not last_name:
        self.add_error('last_name', _("Il cognome è obbligatorio"))
    return last_name

  def clean_email(self):
    email = self.cleaned_data['email']

    if not email:
        self.add_error('email', _("L\'email è obbligatoria"))

    if email:
        if User.objects.filter(email=email).exists():
            password_reset_url = reverse_lazy('password_reset')
            error_message = _("L'email è già in uso. Hai dimenticato la password? <a href='{}' class='fw-bold text-underline'>Resetta la password</a>.".format(password_reset_url))
            self.add_error('email', mark_safe(error_message))
    return email

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    labels = {
      'email': _('Email'),
      'first_name': _('Nome'),
      'last_name': _('Cognome'),
      
    }
    widgets = {
      'email': forms.EmailInput(attrs={
          'class': 'form-control',
          'placeholder': 'mario.rossi@gmail.com',
          'icon': 'fa-envelope',
      }),
      'first_name': forms.TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'Nome',
          'icon': 'fa-user',
      }),
      'last_name': forms.TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'Cognome',
          'icon': 'fa-user',
      }),
    }

  def save(self, commit=True):
        user = super().save(commit=False)
        if not User.objects.filter(email=user.email).exists():
            user.username = user.email
            if commit:
                user.save()
            return user

class UserLoginForm(AuthenticationForm):
  username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
  password = forms.CharField(
      label=_("Password"),
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
  )

  def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:

                if not self.user_cache.groups.exists():
                    register_done_url = reverse_lazy('resend_email_verify_account')
                    error_message = _("L'account non è stato ancora attivato!. controlla la tua mail e verifica il tuo account "
                                      "<a onclick=\"inviaForm('{}');\" class='fw-bold text-underline'>Clicca qui, per ricevere una nuova email</a>"
                                        .format(register_done_url))
                    raise forms.ValidationError(mark_safe(error_message))
                
                else:

                    self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }), label=_("Email"))
  
class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Nuova Password'
    }), label=_("Nuova Password"))
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Conferma Nuova Password'
    }), label=_("Conferma Nuova Password"))

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Vecchia Password'
    }), label=_("Vecchia Password"))
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Nuova Password'
    }), label=_("Nuova Password"))
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Conferma Nuova Password'
    }), label=_("Conferma Nuova Password"))

class CarForm(forms.Form):
    brand = forms.CharField(max_length=100, required=True)
    brand.widget.attrs['class'] = 'form-control'
    brand.widget.attrs['placeholder'] = 'marca'

    model = forms.CharField(max_length=100, required=True)
    model.widget.attrs['class'] = 'form-control'
    model.widget.attrs['placeholder'] = 'modello'

    year = forms.CharField(max_length=4, required=True)
    year.widget.attrs['class'] = 'form-control'
    year.widget.attrs['placeholder'] = 'anno di immatricolazione'

    plate = forms.CharField(max_length=10, required=False)
    plate.widget.attrs['class'] = 'form-control'
    plate.widget.attrs['placeholder'] = 'targa'

    category = forms.ModelChoiceField(queryset=CarCategory.objects.all(),required=False)
    category.widget.attrs['class'] = 'custom-select form-control'

    photos = forms.FileField(required=False)
    photos.widget.attrs['multiple'] = True
 
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        required=False  # Opzionale: rende il campo non obbligatorio
    )
    description.widget.attrs['class'] = 'form-control'
    description.widget.attrs['placeholder'] = 'descrivi il tuo veicolo in 4 righe'

    state = forms.ChoiceField(choices=Cars.STATE_CHOICES, required=False)
    state.widget.attrs['class'] = 'custom-select form-control-border'

    owner = forms.ModelChoiceField(queryset=User.objects.all(),required=False)
    owner.widget.attrs['class'] = 'custom-select form-control-border'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].initial = None

    def clean(self):
        photos = self.files.getlist('photos')

        # Controlla che siano state caricate almeno 2 foto
        if len(photos) < 2:
            raise forms.ValidationError("Devi caricare almeno 2 foto.")
        
        if len(photos) > 5:
           raise forms.ValidationError("Puoi caricare massimo 5 foto.")
        
class EventForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    name.widget.attrs['class'] = 'form-control'
    name.widget.attrs['placeholder'] = 'nome del evento'

    date = forms.DateField(widget=widgets.DateInput(attrs={'type': 'date', 'format': '%Y-%m-%d'}))
    date.widget.attrs['class'] = 'form-control'
    date.widget.attrs['type'] = 'date'
    date.widget.attrs['placeholder'] = 'inserisci la data del evento'

    photos = forms.FileField(required=False)

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        required=False  # Opzionale: rende il campo non obbligatorio
    )
    description.widget.attrs['class'] = 'form-control'
    description.widget.attrs['placeholder'] = 'descrizione del evento'

    state = forms.ChoiceField(choices=Events.STATE_CHOICES, required=False)
    state.widget.attrs['class'] = 'custom-select form-control-border'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        photos = self.files.getlist('photos')
        
        # Controlla che siano state caricate almeno 1 foto
        if len(photos) < 1:
            raise forms.ValidationError("Devi caricare almeno 1 foto.")
        
        if len(photos) > 10:
           raise forms.ValidationError("Puoi caricare massimo 10 foto.")
        