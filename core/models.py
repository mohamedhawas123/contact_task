from django.db import models
from django.contrib.auth import get_user_model


user = get_user_model()



class Contact(models.Model):
    contact_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    created_by = models.ForeignKey(user, on_delete=models.CASCADE, related_name='created_contacts')
    updated_by = models.ForeignKey(user, on_delete=models.CASCADE, related_name='updated_contacts', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contact_name
    
