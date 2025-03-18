import uuid
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError  
from colorfield.fields import ColorField



# Create your models here.
class Photos(models.Model):
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption if self.caption else f"Photo {self.id}"
    
    class Meta:
        verbose_name_plural = "Foto" 

class CarCategory(models.Model):
    # Informazioni della categoria
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Categorie" 

"""
class CarStatus(models.Model):
    # Informazioni della categoria
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Stato Veicolo" 
"""        

class Cars(models.Model):
    # Informazioni del veicolo
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    plate = models.CharField(max_length=20, unique=True, null=True, blank=True)
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE, related_name='cars', null=True, blank=True)

    MIN_FOTO = 3
    MAX_FOTO = 5
    photos = models.ManyToManyField(Photos, related_name='cars', blank=True)

    description = models.TextField(blank=True, null=True)


    STATE_CHOICES = [
        ('?', 'In attesa approvazione idonietà'),
        ('G', 'Idonea'),
        ('B', 'Non idonea'),
    ]    
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='W')

    # Chiave esterna verso il modello User
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')

    class Meta:
        verbose_name_plural = "Auto" 

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"

    def clean(self):
        super().clean()
       #if self.foto.count() < self.MIN_FOTO:
       #    raise ValidationError({'foto': f"Devi selezionare almeno {self.MIN_FOTO} foto."})
       #if self.foto.count() > self.MAX_FOTO:
       #    raise ValidationError({'foto': f"Puoi selezionare al massimo {self.MAX_FOTO} foto."})

"""     
class EventStatus(models.Model):
    # Informazioni della categoria
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Stato Evento" 
"""
        

class Events(models.Model):
    # Informazioni del veicolo
    name = models.CharField(max_length=100)
    sub_name = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    style_background_color = ColorField(default='#DB0808')
    style_text_color = ColorField(default='#FFFFFF')

    style_card_header_backgroud = ColorField(default='#000000')
    style_card_header_text = ColorField(default='#FFFFFF')
    style_card_body_backgroud = ColorField(default='#000000')
    style_card_body_text = ColorField(default='#FFFFFF')
    style_card_body_btn_confirm_background = ColorField(default='#DB0808')      
    style_card_body_btn_confirm_text = ColorField(default='#FFFFFF')  

    uploaded_at = models.DateTimeField(auto_now_add=True)

    photo = models.ImageField(upload_to='events_photo/')

    map_url = models.TextField(blank=True, null=True)
    map_url_to_share = models.TextField(blank=True, null=True)

    STATE_CHOICES = [
        ('P', 'Pubblicato'),
        ('B', 'Bozza'),
        ('I', 'In corso'),
        ('C', 'Concluso'),
        ('A', 'Annullato'),
    ]    
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='B')

    access = models.ManyToManyField('EventsAccess', related_name='Events', null=True, blank=True)
    max_access = models.IntegerField(default=2000)
    subscribe_close = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Eventi" 

    def __str__(self):
        return f"{self.name} - {self.date}"

    def clean(self):
        if EventsAccess.objects.filter(event=self).count() >= self.max_access:
            self.subscribe_close = True
        super().clean()

        
class EventsAccess(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='EventAccess')
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='EventAccess')
    code = models.CharField(max_length=255, default=uuid.uuid4)
    present = models.BooleanField(default=False)
    time_registration = models.DateTimeField(auto_now_add=True)
    time_access = models.DateTimeField(null=True, blank=True)


    def validate(self):
        if self.event:
            if self.event.subscribe_close:
                raise ValidationError("L'evento è chiuso")
            if (EventsAccess.objects.filter(event=self.event).count()) >= self.event.max_access-1:
                self.event.subscribe_close = True
                self.event.save()
                if (EventsAccess.objects.filter(event=self.event).count()) > self.event.max_access-1:
                    raise ValidationError("Il numero massimo di partecipanti è stato raggiunto")
         
    def post_save(self):
        if EventsAccess.objects.filter(event=self.event).count() >= self.event.max_access:
            self.event.subscribe_close = True
            self.event.save()
        
    def save(self, *args, **kwargs):
        self.validate()
        if not self.code:
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event.name}: {self.car}"
    class Meta:
        verbose_name_plural = " Eventi Accessi" 



        
