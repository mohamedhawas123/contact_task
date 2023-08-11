from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Contact
from .serializers import ContactSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .task import update_contact
from django.core.cache import cache


#get all contacts with searrch and cache system
#post contact
@api_view(['GET', 'POST'])
def contact_list(request):

    if request.method == 'GET':
        search_query = request.query_params.get('q', '')
        
        if search_query:
            cache_key = 'seach_cacheKey'
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return Response(cached_data)
            contacts  = Contact.objects.filter(Q(contact_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(created_by__username__icontains=search_query) |
            Q(updated_by__username__icontains=search_query) |
            Q(created_at__icontains=search_query)
            )
        else:
            cache_key ='cache_list_key'
            cached_data = cache.get(cache_key)
            
            if cached_data is not None:
                return Response(cached_data)
            contacts = Contact.objects.all()




        serializers = ContactSerializer(contacts, many=True)
        cache.set(cache_key, serializers.data)
        return Response(serializers.data)
    

    elif request.method == 'POST':
        serializers = ContactSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

#get contact by id
#update contact by id
#delete contact by id
@api_view(['GET', 'PUT', 'DELETE'])
def contact_detail(request, id):
    try:
        contact = Contact.objects.get(id=id)

    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ContactSerializer(contact)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        update_contact.delay(id, request.data)
        serializers = ContactSerializer(contact, data=request.data,  partial=True)
        if serializers.is_valid():
            serializers.save()
        return Response(status=status.HTTP_202_ACCEPTED)
        
    
        

       
    elif request.method == 'DELETE':
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        





