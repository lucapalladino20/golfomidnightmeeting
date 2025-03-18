from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [


    path('example/', lambda request: render(request, 'pages/example.html'), name='example'),

    
    path('my_account/', views.my_account, name='my_account'),


    path('my_garage/', views_car.my_garage, name='my_garage'),
    path('my_garage/add_car', views_car.add_car, name='my_garage/add_car'),
    path('my_garage/view_car/<int:idCar>/', views_car.view_car, name='my_garage/view_car'),
    path('my_garage/del_car/<int:idCar>/', views_car.del_car, name='my_garage/del_car'),
    
    path('cars/', views_car.cars, name='cars'),
    path('cars/add_car', views_car.add_car, name='cars/add_car'),
    path('cars/view_car/<int:idCar>/', views_car.view_car, name='cars/view_car'),
    path('cars/del_car/<int:idCar>/', views_car.del_car, name='cars/del_car'),

    path('cars/to_check', views_car.cars_to_check, name='cars/to_check'),
    path('cars/to_check/add_car', views_car.add_car, name='cars/to_check/add_car'),
    path('cars/to_check/view_car/<int:idCar>/', views_car.view_car, name='cars/to_check/view_car'),
    path('cars/to_check/del_car/<int:idCar>/', views_car.del_car, name='cars/to_check/del_car'),

    path('cars/approved', views_car.cars_approved, name='cars/approved'),
    path('cars/approved/add_car', views_car.add_car, name='cars/approved/add_car'),
    path('cars/approved/view_car/<int:idCar>/', views_car.view_car, name='cars/approved/view_car'),
    path('cars/approved/del_car/<int:idCar>/', views_car.del_car, name='cars/approved/del_car'),

    path('cars/not_approved', views_car.cars_not_approved, name='cars/not_approved'),
    path('cars/not_approved/add_car', views_car.add_car, name='cars/not_approved/add_car'),
    path('cars/not_approved/view_car/<int:idCar>/', views_car.view_car, name='cars/not_approved/view_car'),
    path('cars/not_approved/del_car/<int:idCar>/', views_car.del_car, name='cars/not_approved/del_car'),
    
    path('manage/events/', views_event.event, name='events'),
    path('manage/events/add_event', views_event.add_event, name='events/add_event'),
    path('manage/events/view_event/<int:idEvent>/', views_event.view_event, name='events/view_event'),
    path('manage/events/del_event/<int:idEvent>/', views_event.del_event, name='events/del_event'),

    # Pages
    path('', views.index, name='home'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('events/', views.events, name='events'),
        
    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/register_done/', views.register_done, name='register_done'),
    path('accounts/resend_email_verify_account/', views.resend_email_verify_account, name='resend_email_verify_account'),
    path('accounts/verify_done',views.verify_done, name='verify_done'),
    path('accounts/verify_account/<uidb64>/<token>', views.verify_account, name='verify_account'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name = 'accounts/password_change_done.html'), name='password_change_done'),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),


    # Components
    path('accordion/', views.accordion, name='accordion'),
    path('alerts/', views.alerts, name='alerts'),
    path('badges/', views.badges, name='badges'),
    path('bootstrap-carousels/', views.bootstrap_carousels, name='carousels'),
    path('breadcrumbs/', views.breadcrumbs, name='breadcrumbs'),
    path('buttons/', views.buttons, name='buttons'),
    path('cards/', views.cards, name='cards'),
    path('dropdowns/', views.dropdowns, name='dropdowns'),
    path('forms/', views.forms, name='forms'),
    path('modals/', views.modals, name='modals'),
    path('navs/', views.navs, name='navs'),
    path('pagination/', views.pagination, name='pagination'),
    path('popovers/', views.popovers, name='popovers'),
    path('progress-bars/', views.progress_bars, name='progress_bars'),
    path('tables/', views.tables, name='tables'),
    path('tabs/', views.tabs, name='tabs'),
    path('toasts/', views.toasts, name='toasts'),
    path('tooltips/', views.tooltips, name='tooltips'),
    path('typography/', views.typography, name='typography'),
]
