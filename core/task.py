from celery import Celery
from .serializers import ContactSerializer
from pickle import loads
from rest_framework import status
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from .models import Contact
from pythonTask.celery import app
from rest_framework.response import Response
from django.db import transaction



@app.task(name='update_contact')
def update_contact(contact_id, data):
    
    try:
        contact = Contact.objects.get(id=contact_id)
    except ObjectDoesNotExist:
        return {'status': 'Contact not found'}

    serializer = ContactSerializer(contact, data=data, partial=True)
    if serializer.is_valid():
        with transaction.atomic():
            serializer.save()
        transaction.commit()

        
        return {'status': 'Contact updated', 'data': serializer.data}
    return serializer.errors