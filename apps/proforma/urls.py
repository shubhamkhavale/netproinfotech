from django.urls import path
from . import views

app_name = 'proforma'

urlpatterns = [
    path('', views.proforma_list, name='list'),
]
