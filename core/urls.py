
from django.contrib import admin
from django.urls import path
from .views import contact_list, contact_detail

urlpatterns = [
    path("contacts/",contact_list, name="list" ),
    path("contact/<int:id>/",contact_detail, name="list" ),

]
