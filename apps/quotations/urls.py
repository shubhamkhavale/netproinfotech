from django.urls import path
from .views import create_quotation, quotation_detail
from .pdf import quotation_pdf
from .views import quotation_list

app_name = 'quotations'

urlpatterns = [
    path('', quotation_list, name='list'),
    path('create/', create_quotation, name='create'),
    path('<int:pk>/', quotation_detail, name='detail'),
    path('<int:pk>/pdf/', quotation_pdf, name='pdf'),
]
