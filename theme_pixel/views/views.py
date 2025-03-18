import base64
from email.message import EmailMessage
from email.mime.image import MIMEImage
from io import BytesIO
from pyexpat.errors import messages
import traceback
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from theme_pixel.forms import RegistrationForm, UserLoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm
from django.contrib.auth import logout
from theme_pixel.models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.views import PasswordResetConfirmView
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from theme_pixel.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import qrcode





def user_is_authorized(*gruppi_autorizzati):
    """
    Decoratore per controllare l'accesso a una vista in base ai gruppi autorizzati.

    :param gruppi_autorizzati: elenco dei gruppi autorizzati a vedere la vista
    :param redirect_page: pagina di reindirizzamento per gli utenti non autorizzati (opzionale)
    """

    def has_required_group_permissions(user):
        # Verifica se l'utente è autenticato
        if user.is_authenticated:
            # Se l'utente è autenticato, verifica se appartiene a uno dei gruppi autorizzati o è un superuser
            if any(group.name in gruppi_autorizzati for group in user.groups.all()) or user.is_superuser:
                print("Utente autenticato con permessi")
                return True
            else:
                # Se l'utente è autenticato ma non autorizzato
                print("Utente autenticato senza permessi, reindirizzamento a pagina di errore")
                return False
        else:
            # Se l'utente non è autenticato
            print("Utente non autenticato, reindirizzamento a pagina di login")
            return False
        
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not has_required_group_permissions(request.user):
                if not request.user.is_authenticated:
                  return redirect(reverse_lazy('login') + '?next=' + request.path)
                else:
                  return redirect('/')
            return view_func(request, *args, **kwargs)
        return wrapper
    
    return decorator



# Create your views here.
def send_mail(request):
  subject="Test Email from Django" 
  message = 'This is a test email sent from Django using Gmail' 
  email_from = settings.EMAIL_HOST_USER 
  recipient_list = ['lucapalladino20@gmail.com'] 
  send_mail(subject, message, email_from, recipient_list) 
  return HttpResponse('Email sent')


# Pages
def index(request):
  return render(request, 'pages/index.html')

def my_account(request):
    if request.method == 'POST':
        if 'nome' in request.POST:
            try:
                user = request.user
                if not request.POST.get('nome') or not request.POST.get('cognome'):
                  messages.add_message(request, messages.ERROR, 'Tutti i campi sono obbligatori!', extra_tags='informazioni_personali')
                  return redirect('my_account')
                user.first_name = request.POST.get('nome')
                user.last_name = request.POST.get('cognome')
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Dati aggiornati con successo!', extra_tags='informazioni_personali')
                return redirect('my_account')
            except Exception as e:
                messages.add_message(request, messages.ERROR, 'Errore durante l\'aggiornamento dei dati', extra_tags='informazioni_personali')
                return redirect('my_account')
        elif 'old_password' in request.POST:
            try:
                user = request.user
                vecchia_password = request.POST.get('old_password')
                if not user.check_password(vecchia_password):
                    messages.add_message(request, messages.ERROR, 'La vecchia password non è corretta!', extra_tags='password')
                    return redirect('my_account')
                nuova_password = request.POST.get('new_password1')
                conferma_password = request.POST.get('new_password2')
                if nuova_password != conferma_password:
                    messages.add_message(request, messages.ERROR, 'Le password non corrispondono!', extra_tags='password')
                    return redirect('my_account')
                form = PasswordChangeForm(user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)
                    messages.add_message(request, messages.SUCCESS, 'Password aggiornata con successo!', extra_tags='password')
                    return redirect('my_account')
                else:
                    messages.add_message(request, messages.ERROR, 'Errore durante l\'aggiornamento della password', extra_tags='password')
                    return redirect('my_account')
            except Exception as e:
                messages.add_message(request, messages.ERROR, 'Errore durante l\'aggiornamento della password', extra_tags='password')
                return redirect('my_account')
    return render(request, 'pages/my_account.html')

def contact_us(request):
  if request.method == 'POST':

     mail_subject = "Notifica Form Contatto"
     message = render_to_string("email/template_contact_us.html", {
        'name': request.POST.get('name'),
        'email': request.POST.get('email'),
        'message': request.POST.get('message'),
     })

     email = EmailMessage(
      mail_subject,
      message,
      settings.EMAIL_HOST_USER,
      [settings.EMAIL_HOST_USER],
      []
     )

     try:
        email.send()
        messages.success(request, 'Email inviata con successo!')
     except Exception as e:
        messages.error(request, f'Errore nell\'invio dell\'email')

  return render(request, 'pages/contact.html')

def events(request):

  if request.method == 'POST':
    car_pk = request.POST.get('car_id')
    event_pk = request.POST.get('event_id')
    try:
      car = Cars.objects.get(pk=car_pk)
      event = Events.objects.get(pk=event_pk)
      if car.owner == request.user and car.get_state_display() == 'Idonea' and event.get_state_display() == 'Pubblicato':
        if not EventsAccess.objects.filter(car=car, event=event).exists():

          print(EventsAccess.objects.filter(event=event).count())
          print(event.max_access)

          if event.subscribe_close:
            message = f'L\'iscrizione è chiusa'
            print(message)
            messages.add_message(request, messages.ERROR, message, extra_tags='registrazione_accesso_auto_evento')
            return redirect('events')
          
          if EventsAccess.objects.filter(event=event).count() >= event.max_access:
            message = f'{car} non aggiunta all\'evento {event.name} perché non ci sono più posti disponibili'
            print(message)
            messages.add_message(request, messages.ERROR, message, extra_tags='registrazione_accesso_auto_evento')
            return redirect('events')

          access = EventsAccess.objects.create(car=car, event=event)

          qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
          )

          qr.add_data(access.code)
          qr.make(fit=True)
          img = qr.make_image(fill_color="black", back_color="white")
          buffer = BytesIO()
          img.save(buffer, format="PNG")

          mail_subject = "Codice QR"
          message = render_to_string("email/template_qr_code.html", {
             'car': car,
             'event': event,
          })

          email = EmailMessage(
            mail_subject,
            message,
            settings.EMAIL_HOST_USER,
            [request.user.email],
            []
          )

          email.content_subtype = 'html'
          #Inserisco l'immagine nel body          
          mime_image = MIMEImage(buffer.getvalue())
          mime_image.add_header('Content-ID', '<image>')
          email.attach(mime_image)

          email.send()

          message = f'{car} aggiunta all\'evento {event.name} con successo'
          print(message)
          messages.add_message(request, messages.SUCCESS, message, extra_tags='registrazione_accesso_auto_evento')
          return redirect('events')
        else:
          message = f'{car} già presente all\'evento {event.name}'
          print(message)
          messages.add_message(request, messages.ERROR, message, extra_tags='registrazione_accesso_auto_evento')
          return redirect('events')
      else:
        if car.owner != request.user:
          message = f'{request.user} Non sei il proprietario dell\'auto {car}'
          print(message)
          messages.add_message(request, messages.ERROR, message, extra_tags='registrazione_accesso_auto_evento')
          return redirect('events')
        elif car.get_state_display() != 'Idonea':
          message = f'{car} non idonea'
          print(message)
          messages.add_message(request, messages.ERROR, message, extra_tags='registrazione_accesso_auto_evento')
          return redirect('events')
        elif event.get_state_display() != 'Pubblicato':
          message = f'{event} iscrizione non valida per quest\'evento'
          print(message)
          messages.add_message(request, messages.ERROR, message, extra_tags='registrazione_accesso_auto_evento')
          return redirect('events')
    except (Cars.DoesNotExist, Events.DoesNotExist):
      message = f'Veicolo o evento non trovato'
      print(message)
      messages.add_message(request, messages.ERROR, message, extra_tags='registrazione_accesso_auto_evento')
      return redirect('events')
    except Exception as e:
      message = 'Errore durante l\'iscrizione all\'evento'
      print(message)
      traceback.print_exc()
      messages.add_message(request, messages.ERROR, message, extra_tags='registrazione_accesso_auto_evento')
      return redirect('events')

      
  if request.user.is_superuser:
    events = Events.objects.filter(state__in=[x[0] for x in Events.STATE_CHOICES if x[1] in ['Pubblicato', 'In corso', 'Annullato', 'Bozza']]).all()
  else:
    events = Events.objects.filter(state__in=[x[0] for x in Events.STATE_CHOICES if x[1] in ['Pubblicato', 'In corso', 'Annullato']]).all()

  if request.user.is_authenticated:
    cars = request.user.cars.all()
  else:
    cars = None

  context = {
    'events': events,
    'cars': cars
  }
  return render(request, 'pages/events.html', context)

# Authentication
class UserLoginView(LoginView):
  template_name = 'accounts/sign-in.html'
  form_class = UserLoginForm

  def get_success_url(self):
    next_url = self.request.GET.get('next')
    if next_url:
        return next_url
    return super().get_success_url()

def logout_view(request):
  logout(request)
  return redirect('/')

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      send_verification_email(request, user, user.email)
      print("Account created successfully!")
      return redirect(reverse_lazy('register_done'))
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()

  context = { 'form': form }
  return render(request, 'accounts/sign-up.html', context)

def resend_email_verify_account(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    if username:
      try:
        user = User.objects.get(username=username)
        send_verification_email(request, user, user.email)
        print('Email di verifica inviata con successo!')
        return redirect(reverse_lazy('register_done'))
      except User.DoesNotExist:
        print('Utente non trovato con l\'email specificata.')
        return render(request, 'accounts/sign-in.html')
    else:
      print('Username non esistente!')
    return render(request, 'accounts/sign-in.html')
  else:
    print('Richiesta non valida.')
    return render(request, 'accounts/sign-in.html')

def register_done(request):    
  return render(request, 'accounts/sign-up-done.html')

def send_verification_email(request, user, to_email):
    mail_subject = "Attiva il tuo account utente."
    message = render_to_string("email/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })

    email = EmailMessage(
      mail_subject,
      message,
      settings.EMAIL_HOST_USER,
      [to_email],
      []
    )

    try:
        email.send()
        #messages.success(request, f'Cara/o <b>{user}</b>, per favore vai alla tua email <b>{to_email}</b> e clicca sul link di attivazione ricevuto per confermare e completare la registrazione. <b>Nota:</b> Controlla la cartella spam.')
    except Exception as e:
        messages.error(request, f'Errore nell\'invio dell\'email: {str(e)}')

def verify_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and account_activation_token.check_token(user, token):
        group = Group.objects.get(name='Visitatore')
        user.groups.add(group)
        user.save()
        return redirect('verify_done')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('homepage')

def verify_done(request):
   return render(request, 'accounts/verify_done.html')


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            form.add_error('email', 'Nessun account registrato con questa email.')
            return self.form_invalid(form)

        # Invia la mail per il recupero della password
        return super().form_valid(form)
    

    def send_mail(self, subject, email_template_name, context, from_email, to_email):
        subject = 'Recupero password'
        email_template_name = 'accounts/password_reset_email.html'
        context = {
            'user': self.user,
            'token': self.token,
            'uid': self.uid,
        }
        from_email = settings.EMAIL_HOST_USER
        to_email = self.user.email

        email_body = render_to_string(email_template_name, context)
        send_mail(subject, email_body, from_email, [to_email])


class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

  def dispatch(self, request, *args, **kwargs):
        try:
            uidb64 = kwargs['uidb64']
            token = kwargs['token']
            user = self.get_user(uidb64)
            if not default_token_generator.check_token(user, token):
                # Se il token non è valido, visualizza una pagina di errore
                return render(request, 'accounts/password_reset_link_invalid.html', status=400)
            return super().dispatch(request, *args, **kwargs)
        except Http404:
          # Se il link è scaduto, visualizza una pagina di errore
          return render(request, 'accounts/password_reset_link_expired.html', status=400)
        except:
          # Se non si riesce a recuperare l'utente, visualizza una pagina di
          return render(request, 'accounts/password_reset_link_invalid.html', status=400)

        


class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm


# Components
def accordion(request):
  return render(request, 'components/accordions.html')

def alerts(request):
  return render(request, 'components/alerts.html')

def badges(request):
  return render(request, 'components/badges.html')

def bootstrap_carousels(request):
  return render(request, 'components/bootstrap-carousels.html')

def breadcrumbs(request):
  return render(request, 'components/breadcrumbs.html')

def buttons(request):
  return render(request, 'components/buttons.html')

def cards(request):
  return render(request, 'components/cards.html')

def dropdowns(request):
  return render(request, 'components/dropdowns.html')

def forms(request):
  return render(request, 'components/forms.html')

def modals(request):
  return render(request, 'components/modals.html')

def navs(request):
  return render(request, 'components/navs.html')

def pagination(request):
  return render(request, 'components/pagination.html')

def popovers(request):
  return render(request, 'components/popovers.html')

def progress_bars(request):
  return render(request, 'components/progress-bars.html')

def tables(request):
  return render(request, 'components/tables.html')

def tabs(request):
  return render(request, 'components/tabs.html')

def toasts(request):
  return render(request, 'components/toasts.html')

def tooltips(request):
  return render(request, 'components/tooltips.html')

def typography(request):
  return render(request, 'components/typography.html')