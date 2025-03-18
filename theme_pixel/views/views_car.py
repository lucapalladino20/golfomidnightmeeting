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
def my_garage(request):
  #
  context = {
    'cars': request.user.cars.all(),
  }
  return render(request, 'pages/my_garage.html', context)

@user_is_authorized('Amministratore')
def cars(request):
  #
  context = {
    'cars': Cars.objects.all(),
    'url_view_car': 'cars/view_car',
  }
  return render(request, 'common/cars.html', context)

@user_is_authorized('Amministratore')
def cars_to_check(request):
  #
  context = {
    'cars': Cars.objects.filter(state=1).all(),
    'url_view_car': 'cars/to_check/view_car',
  }
  return render(request, 'common/cars.html', context)

@user_is_authorized('Amministratore')
def cars_approved(request):
  #
  context = {
    'cars': Cars.objects.filter(state=2).all(),
    'url_view_car': 'cars/approved/view_car',
  }
  return render(request, 'common/cars.html', context)

@user_is_authorized('Amministratore')
def cars_not_approved(request):
  #
  context = {
    'cars': Cars.objects.filter(state=3).all(),
    'url_view_car': 'cars/approved/view_car',
  }
  return render(request, 'common/cars.html', context)

@user_is_authorized('Amministratore','Staff','Visitatore')
def add_car(request):
    #
    view_errors = None
    # Recupera tutte le categorie dal database
    if request.method == 'POST':
      # Passa le categorie al form
      form = CarForm(request.POST, request.FILES)  

      if form.is_valid():
        # Elabora i dati del form
        brand = form.cleaned_data['brand']
        model = form.cleaned_data['model']
        year = form.cleaned_data['year']
        plate = form.cleaned_data['plate'] or None
        description = form.cleaned_data['description'] or None
        category = form.cleaned_data['category']
        photos = request.FILES.getlist('photos')  # Ottieni la lista dei file
          
        owner = request.user
        state = next((x[0] for x in Cars.STATE_CHOICES if x[1] == 'In attesa approvazione idonietà'), None)
  

        #
        CarRecord = Cars(
          brand=brand,
          model=model,
          year=year,
          category=category,
          plate=plate,
          description=description,
          owner=owner,
          state=state,
        )
        # Salva il nuovo oggetto
        CarRecord.save()
        #
        for photo in photos:
          photo_obj = Photos.objects.create(image=photo)  # Crea un nuovo oggetto photos
          photo_obj.save()
          CarRecord.photos.add(photo_obj)
        #
        # Reindirizza l'utente a una pagina di successo
        url = request.path
        try:
          url_modificata = url.split("/add_car")[0].lstrip("/")
          return redirect(reverse_lazy(url_modificata))
        except:
          return redirect(reverse_lazy('my_garage'))
      else:
        # Se il form non è valido, mostra gli errori
        print(form.errors)
        return JsonResponse({"form.errors":str(form.errors['__all__'])})
    else:
      # Passa le categorie al form per la visualizzazione iniziale
      form = CarForm()  
      form['owner'].initial = request.user
      return render(request, 'pages/my_garage_add_car.html', {'form': form, 'view_errors': view_errors })
    
@user_is_authorized('Amministratore','Staff','Visitatore')
def view_car(request, idCar):
    #
    view_errors = None
    #
    if not(idCar):
      #L'ID contiene un valore null
      return redirect(reverse_lazy('my_garage'))
    #
    if (len(Cars.objects.filter(id=idCar))!=1):
      # Solo un record deve essere presente con lo stesso ID.
      return redirect(reverse_lazy('my_garage'))
    #
    CarRecord = Cars.objects.get(id=idCar)
    #
    if not(CarRecord.owner == request.user) and not(request.user.groups.filter(name='Amministratore').exists() or request.user.is_superuser):
        #L'utente vorrebe visulizzare una macchina che non è sua
        return redirect(reverse_lazy('my_garage'))
    #
    form = CarForm()
    form.id = idCar
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
    form['brand'].initial = CarRecord.brand
    form['model'].initial = CarRecord.model
    form['year'].initial = CarRecord.year
    form['plate'].initial = CarRecord.plate
    form['description'].initial = CarRecord.description
    form['state'].initial = CarRecord.state
    form['owner'].initial = CarRecord.owner
    #
    form['photos'].initial = CarRecord.photos.all()
    #
    for photo in form['photos'].initial:
       photo.name = str(photo.image).replace("photos/", "")
       photo.type = photo.name.split('.')[-1].lower()
       photo.size = photo.image.size

    """
    #Recupero la category del veicolo
    #category_selezionata = CarCategory.objects.get(id=CarRecord.category.id)
    #Se e' coerente la category selezionata con quella del veicolo
    if category_selezionata:
      form['category'].initial = CarRecord.category.id
    else:
      #category non trovata
      print("categoria non trovata")
      view_errors = ['categoria non trovata']"
    """

    #
    if request.method == 'POST':
      # Passa le categorie al form
      form = CarForm(request.POST, request.FILES)  

      if form.is_valid():
        # Elabora i dati del form
        brand = form.cleaned_data['brand']
        model = form.cleaned_data['model']
        year = form.cleaned_data['year']
        plate = form.cleaned_data['plate'] or None
        description = form.cleaned_data['description'] or None
        category = form.cleaned_data['category']
        state = form.cleaned_data['state'] or CarStatus.objects.get(pk=1)
        owner = form.cleaned_data['owner']
        photos = request.FILES.getlist('photos')  # Ottieni la lista dei file
        #
        CarRecord.brand = brand
        CarRecord.model = model
        CarRecord.year = year
        CarRecord.plate = plate
        CarRecord.description = description
        CarRecord.category = category
        #
        if request.user.groups.filter(name='Amministratore').exists() or request.user.is_superuser:
          CarRecord.state = state
          CarRecord.owner = owner
        #salvo il record
        CarRecord.save()
        # Salvo le foto da cancellare
        photos_to_delete = list(CarRecord.photos.all().values_list('id', flat=True))
        # Aggiungo le nuove foto
        for photo in photos:
            photos_obj = Photos.objects.create(image=photo)
            photos_obj.save()
            CarRecord.photos.add(photos_obj)
        # Cancella definitivamente le foto dal database dopo aver salvato le nuove
        Photos.objects.filter(id__in=photos_to_delete).delete()
        #
        # Reindirizza l'utente a una pagina di successo
        url = request.path
        try:
          url_modificata = url.split("/view_car")[0].lstrip("/")
          return redirect(reverse_lazy(url_modificata))
        except:
          return redirect(reverse_lazy('my_garage'))
      else:
        # Se il form non è valido, mostra gli errori
        return JsonResponse({"form.errors":str(form.errors['__all__'])})
    else: 
      return render(request, 'pages/my_garage_view_car.html', {'form': form, 'view_errors': view_errors, 'car': Cars.objects.get(id=idCar) })
    
@user_is_authorized('Amministratore','Staff','Visitatore')
def del_car(request, idCar):
  #
  if not(idCar):
    #L'ID veicolo contiene un valore null
    return redirect(reverse_lazy('my_garage'))
  #
  if (len(Cars.objects.filter(id=idCar))!=1):
    # Solo un veicolo deve essere presente con lo stesso ID.
    return redirect(reverse_lazy('my_garage'))
  #
  CarRecord = Cars.objects.get(id=idCar)
  #
  if not(CarRecord.owner == request.user) and not(request.user.is_superuser) and not(request.user.groups.filter(name='Amministratore').exists()):
      #L'utente vorrebe visulizzare una macchina che non è sua
      return redirect(reverse_lazy('my_garage'))
  #Cancella il veicolo 
  CarRecord.delete()
  # Reindirizza l'utente alla pagina del garage
  url = request.path
  try:
    url_modificata = url.split("/del_car")[0].lstrip("/")
    return redirect(reverse_lazy(url_modificata))
  except:
    return redirect(reverse_lazy('my_garage'))
