import time
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
from theme_pixel.models import *
from theme_pixel.forms import *
from django.http import JsonResponse
from theme_pixel.templatetags import *
from theme_pixel.views.views import user_is_authorized


@user_is_authorized('Amministratore','Staff','Visitatore')
def event(request):
  #
  context = {
    'events': Events.objects.all(),
  }
  return render(request, 'common/events.html', context)

@user_is_authorized('Amministratore')
def event_opened(request):
  #
  context = {
    'events': Events.objects.filter(state=1).all(),
  }
  return render(request, 'common/events.html', context)

@user_is_authorized('Amministratore')
def add_event(request):
    #
    view_errors = None
    # Recupera tutte le categorie dal database
    if request.method == 'POST':
      # Passa le categorie al form
      form = EventForm(request.POST, request.FILES)  

      if form.is_valid():
        # Elabora i dati del form
        name = form.cleaned_data['name']
        date = form.cleaned_data['date']
        description = form.cleaned_data['description'] or None
        photos = request.FILES.getlist('photos')  # Ottieni la lista dei file
        if request.user.groups.filter(name='Amministratore').exists() or request.user.is_superuser :
          state = form.cleaned_data['state'] or EventStatus.objects.get(pk=1)
        else:
          state = EventStatus.objects.get(pk=1)
        #
        EventRecord = Events(
          name=name,
          date=date,
          description=description,
          state=state,
        )   
        # Salva il nuovo oggetto
        EventRecord.save()
        #
        for photo in photos:
          photo_obj = Photos.objects.create(image=photo)  # Crea un nuovo oggetto photos
          photo_obj.save()
          EventRecord.photos.add(photo_obj)
        #
        return redirect(reverse_lazy('events'))
      else:
        # Se il form non è valido, mostra gli errori
        return JsonResponse({"form.errors":str(form.errors['__all__'])})
    else:
      # Passa le categorie al form per la visualizzazione iniziale
      form = EventForm()  
      return render(request, 'common/events_add_event.html', {'form': form, 'view_errors': view_errors })
    
@user_is_authorized('Amministratore')
def view_event(request, idEvent):
    #
    view_errors = None
    #
    if not(idEvent):
      #L'ID contiene un valore null
      return redirect(reverse_lazy('events'))
    #
    if (len(Events.objects.filter(id=idEvent))!=1):
      # Solo un record deve essere presente con lo stesso ID.
      return redirect(reverse_lazy('events'))
    #
    EventRecord = Events.objects.get(id=idEvent)
    #
    form = EventForm()
    form.id = idEvent
    #
    if request.user.groups.filter(name='Amministratore').exists() or request.user.is_superuser:
      #Form disabilitato solo per gli Amministratore
      form.disabled = False
      form.fields['state'].widget.attrs['required'] = True
    else:
      #Form disabilitato per tutti gli altri utenti
      form.disabled = True
      for field in form.fields:
        form.fields[field].widget.attrs['readonly'] = True
        form.fields[field].widget.attrs['disabled'] = True
        form.fields[field].widget.attrs['style'] = 'pointer-events: none;'
    #Imposto i valori del form
    form['name'].initial = EventRecord.name
    form['date'].initial = EventRecord.date
    form['description'].initial = EventRecord.description
    form['state'].initial = EventRecord.state
    #
    form['photos'].initial = EventRecord.photos.all()
    #
    for photo in form['photos'].initial:
       photo.name = str(photo.image).replace("photos/", "")
       photo.type = photo.name.split('.')[-1].lower()
       photo.size = photo.image.size
    #
    if request.method == 'POST':
      # Passa le categorie al form
      form = EventForm(request.POST, request.FILES)  

      if form.is_valid():
        # Elabora i dati del form
        name = form.cleaned_data['name']
        date = form.cleaned_data['date']
        description = form.cleaned_data['description'] or None
        state = form.cleaned_data['state'] or EventStatus.objects.get(pk=1)
        photos = request.FILES.getlist('photos')  # Ottieni la lista dei file
        #
        EventRecord.brand = name
        EventRecord.model = date
        EventRecord.description = description
        #
        if request.user.groups.filter(name='Amministratore').exists() or request.user.is_superuser:
          EventRecord.state = state
        #salvo il record
        EventRecord.save()
        # Salvo le foto da cancellare
        photos_to_delete = list(EventRecord.photos.all().values_list('id', flat=True))
        # Aggiungo le nuove foto
        for photo in photos:
            photos_obj = Photos.objects.create(image=photo)
            photos_obj.save()
            EventRecord.photos.add(photos_obj)
        # Cancella definitivamente le foto dal database dopo aver salvato le nuove
        Photos.objects.filter(id__in=photos_to_delete).delete()
        #
        # Reindirizza l'utente a una pagina di successo
        return redirect(reverse_lazy('events'))
      else:
        # Se il form non è valido, mostra gli errori
        return JsonResponse({"form.errors":str(form.errors['__all__'])})
    else: 
      return render(request, 'common/events_view_event.html', {'form': form, 'view_errors': view_errors })
    
@user_is_authorized('Amministratore')
def del_event(request, idEvent):
  #
  if not(idEvent):
    #L'ID evento contiene un valore null
    return redirect(reverse_lazy('evnets'))
  #
  if (len(Events.objects.filter(id=idEvent))!=1):
    # Solo un evento deve essere presente con lo stesso ID.
    return redirect(reverse_lazy('evnets'))
  #
  EventRecord = Events.objects.get(id=idEvent)
  #Cancella il veicolo 
  EventRecord.delete()

  # Reindirizza l'utente alla pagina degli eventi
  return redirect(reverse_lazy('events'))
 