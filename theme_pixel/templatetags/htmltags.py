from django import template
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from theme_pixel.models import *

register = template.Library()

@register.filter(name='is_in_group')
def is_in_group(user, group_name):
    """
    Verifica se l'utente appartiene a un gruppo specifico.
    """
    return user.groups.filter(name=group_name).exists()


@register.filter(name='car_already_existent_at_event')
def car_already_existent_at_event(car, event):
    return EventsAccess.objects.filter(event=event, car=car).exists()

@register.filter(name='get_name')
def get_name(location):
    breadcrumb_map = {
        'my_garage/add_car':        f"""
                                    <li class="breadcrumb-item">
                                        <a href="{reverse_lazy('my_garage')}">Il mio garage</a>
                                    </li>
                                    <li class="breadcrumb-item active">Aggiungi veicolo</li>
                                    """,
        'my_garage/view_car':       f"""
                                    <li class="breadcrumb-item">
                                        <a href="{reverse_lazy('my_garage')}">Il mio garage</a>
                                    </li>
                                    <li class="breadcrumb-item active">Visualizza veicolo</li>
                                    """,
        'cars/add_car':             f""" 
                                    <li class="breadcrumb-item">
                                        <a href="{reverse_lazy('cars')}">Tutti i veicoli</a>
                                    </li>
                                    <li class="breadcrumb-item active">Aggiungi veicolo</li>
                                    """,
        'cars/view_car':            f"""
                                    <li class="breadcrumb-item">
                                        <a href="{reverse_lazy('cars')}">Tutti i veicoli</a>
                                    </li>
                                    <li class="breadcrumb-item active">Visualizza veicolo</li>
                                    """,
        'cars/to_check/add_car':    f"""
                                    <li class="breadcrumb-item">
                                        <a href="{reverse_lazy('cars/to_check')}">Veicoli da verificare</a>
                                    </li>
                                    <li class="breadcrumb-item active">Aggiungi veicolo</li>
                                    """,
        'cars/to_check/view_car':   f"""
                                    <li class="breadcrumb-item">
                                        <a href="{reverse_lazy('cars/to_check')}">Veicoli da verificare</a>
                                    </li>
                                    <li class="breadcrumb-item active">Visualizza veicolo</li>
                                    """,
        'cars/approved/add_car':    f"""
                                    <li class="breadcrumb-item">
                                        <a href="{reverse_lazy('cars/approved')}">Veicoli approvati</a>
                                    </li>
                                    <li class="breadcrumb-item active">Aggiungi veicolo</li>
                                    """,
        'cars/approved/view_car':   f"""
                                    <li class="breadcrumb-item">
                                        <a href="{reverse_lazy('cars/approved')}">Veicoli approvati</a>
                                    </li>
                                    <li class="breadcrumb-item active">Visualizza veicolo</li>
                                    """,
        'cars/not_approved/add_car':    f"""
                                    <li class="breadcrumb-item">
                                        <a href="{reverse_lazy('cars/not_approved')}">Veicoli non approvati</a>
                                    </li>
                                    <li class="breadcrumb-item active">Aggiungi veicolo</li>
                                    """,
        'cars/not_approved/view_car':   f"""
                                    <li class="breadcrumb-item">
                                        <a href="{reverse_lazy('cars/not_approved')}">Veicoli non approvati</a>
                                    </li>
                                    <li class="breadcrumb-item active">Visualizza veicolo</li>
                                    """,
        'events/view_event':        f"""
                                    <li class="breadcrumb-item">
                                        <a href="{reverse_lazy('events')}">Eventi</a>
                                    </li>
                                    <li class="breadcrumb-item active">Visualizza evento</li>
                                    """,
        'events/add_event':         f"""
                                    <li class="breadcrumb-item">
                                        <a href="{reverse_lazy('events')}">Eventi</a>
                                    </li>
                                    <li class="breadcrumb-item active">Aggiungi evento</li>
                                    """,
        # aggiungi altri casi qui
    }
    return breadcrumb_map.get(location, '')

@register.filter(name='get_title')
def get_title(location):
    breadcrumb_map = {
        'my_garage': 'Il mio garage',
        'my_garage/add_car': 'Aggiungi veicolo',
        'my_garage/view_car': 'Visualizza veicolo',

        'cars': 'Tutti i veicoli',
        'cars/add_car': 'Aggiungi veicolo',
        'cars/view_car': 'Visualizza veicolo',

        'cars/to_check': 'Tutti i veicoli da verificare',
        'cars/to_check/add_car': 'Aggiungi veicolo',
        'cars/to_check/view_car': 'Visualizza veicolo',

        'cars/approved': 'Tutti i veicoli approvati',
        'cars/approved/add_car': 'Aggiungi veicolo',
        'cars/approved/view_car': 'Visualizza veicolo',

        'cars/not_approved': 'Tutti i veicoli non approvati',
        'cars/not_approved/add_car': 'Aggiungi veicolo',
        'cars/not_approved/view_car': 'Visualizza veicolo',

        'events': 'Eventi',
        'events/add_event': 'Aggiungi evento',
        'events/view_event': 'Visualizza evento',
        # aggiungi altri casi qui
    }
    return breadcrumb_map.get(location, '')

@register.filter(name='get_header_button')
def get_header_button(location):
    breadcrumb_map = {
        'cars':             f"""
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/not_approved')}" class="btn btn-sm btn-outline-gray-600 btn-danger">
                                    <i class="fas fa-times-circle"></i>
                                    Veicoli non approvati
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/approved')}" class="btn btn-sm btn-outline-gray-600 btn-secondary">
                                    <i class="fas fa-check-circle"></i>
                                    Veicoli approvati
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/to_check')}" class="btn btn-sm btn-outline-gray-600 btn-primary">
                                    <i class="fas fa-tasks"></i>
                                    Veicoli da Verificare
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars')}" disabled class="btn btn-sm btn-outline-gray-600 btn-primary">
                                    <i class="fas fa-car"></i>
                                    Tutti i veicoli
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/add_car')}" class="btn btn-sm btn-outline-gray-600 btn-success">
                                    <i class="fas fa-plus-circle"></i>
                                    Aggiungi veicolo
                                </a>
                            </div>
                            """,
        'cars/to_check':    f"""
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/not_approved')}" class="btn btn-sm btn-outline-gray-600 btn-danger">
                                    <i class="fas fa-times-circle"></i>
                                    Veicoli non approvati
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/approved')}" class="btn btn-sm btn-outline-gray-600 btn-secondary">
                                    <i class="fas fa-check-circle"></i>
                                    Veicoli approvati
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/to_check')}" class="btn btn-sm btn-outline-gray-600 btn-primary">
                                    <i class="fas fa-tasks"></i>
                                    Veicoli da Verificare
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars')}" class="btn btn-sm btn-outline-gray-600 btn-primary">
                                    <i class="fas fa-car"></i>
                                    Tutti i veicoli
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/to_check/add_car')}" class="btn btn-sm btn-outline-gray-600 btn-success">
                                    <i class="fas fa-plus-circle"></i>
                                    Aggiungi veicolo
                                </a>
                            </div> 
                            """,
        'cars/approved':    f"""
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/not_approved')}" class="btn btn-sm btn-outline-gray-600 btn-danger">
                                    <i class="fas fa-times-circle"></i>
                                    Veicoli non approvati
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/approved')}" class="btn btn-sm btn-outline-gray-600 btn-secondary">
                                    <i class="fas fa-check-circle"></i>
                                    Veicoli approvati
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/to_check')}" class="btn btn-sm btn-outline-gray-600 btn-primary">
                                    <i class="fas fa-tasks"></i>
                                    Veicoli da Verificare
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars')}" class="btn btn-sm btn-outline-gray-600 btn-primary">
                                    <i class="fas fa-car"></i>
                                    Tutti i veicoli
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/approved/add_car')}" class="btn btn-sm btn-outline-gray-600 btn-success">
                                    <i class="fas fa-plus-circle"></i>
                                    Aggiungi veicolo
                                </a>
                            </div> 
                            """,
        'cars/not_approved':    f"""
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/not_approved')}" class="btn btn-sm btn-outline-gray-600 btn-danger">
                                    <i class="fas fa-times-circle"></i>
                                    Veicoli non approvati
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/approved')}" class="btn btn-sm btn-outline-gray-600 btn-secondary">
                                    <i class="fas fa-check-circle"></i>
                                    Veicoli approvati
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/to_check')}" class="btn btn-sm btn-outline-gray-600 btn-primary">
                                    <i class="fas fa-tasks"></i>
                                    Veicoli da Verificare
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars')}" class="btn btn-sm btn-outline-gray-600 btn-primary">
                                    <i class="fas fa-car"></i>
                                    Tutti i veicoli
                                </a>
                            </div>
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('cars/not_approved/add_car')}" class="btn btn-sm btn-outline-gray-600 btn-success">
                                    <i class="fas fa-plus-circle"></i>
                                    Aggiungi veicolo
                                </a>
                            </div> 
                            """,
        'events':           f"""
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('events/add_event')}" class="btn btn-sm btn-outline-gray-600 btn-success">
                                    <i class="fas fa-plus-circle"></i>
                                    Aggiungi evento
                                </a>
                            </div>
                            """,
        'my_garage':        f"""
                            <div class="btn-group mr-2">
                                <a href="{reverse_lazy('my_garage/add_car')}" class="btn btn-sm btn-outline-gray-600 btn-success">
                                    <i class="fas fa-plus-circle"></i>
                                    Aggiungi veicolo
                                </a>
                            </div>
                            """,
        # aggiungi altri casi qui
    }
    return breadcrumb_map.get(location, '')

@register.filter(name='get_footer_button')
def get_footer_button(location):
    breadcrumb_map = {
        # aggiungi altri casi qui
    }
    return breadcrumb_map.get(location, '')


@register.filter(name='makeid')
def makeid(value):
    return value[0]