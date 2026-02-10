from django.urls import path
from . import views

app_name = 'delivery_notes'

urlpatterns = [
    path('', views.delivery_note_list, name='list'),
]
