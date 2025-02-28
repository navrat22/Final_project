from django.urls import path
from .views import (
    medicine_list, add_medicine, edit_medicine, delete_medicine, take_dose,
    medicine_history, medicine_selection, add_new_medicine, medicine_detail, home_redirect
)

urlpatterns = [
    path('', home_redirect, name='home_redirect'),
    path('medicine-list/', medicine_list, name='medicine_list'),
    path('add-medicine/', add_medicine, name='add_medicine'),
    path('edit-medicine/<int:medicine_id>/', edit_medicine, name='edit_medicine'),
    path('delete-medicine/<int:medicine_id>/', delete_medicine, name='delete_medicine'),
    path('take-dose/<int:medicine_id>/', take_dose, name='take_dose'),
    path('medicine-history/', medicine_history, name='medicine_history'),
    path('medicine-selection/', medicine_selection, name='medicine_selection'),
    path('add-new-medicine/', add_new_medicine, name='add_new_medicine'),
    path('medicine-detail/<int:medicine_id>/', medicine_detail, name='medicine_detail'),


]
