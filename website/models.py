from django.db import models

# Create your models here.
class Record(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


