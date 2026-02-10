from django.urls import path
from . import views

app_name = 'terms'

urlpatterns = [
    path('', views.term_list, name='list'),
]
