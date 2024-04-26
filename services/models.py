from django.db import models
from django.contrib.auth.models import User

class Csv(models.Model):
    
    file_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='upload')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    

    def __str__(self) -> str:
        return self.file_name
