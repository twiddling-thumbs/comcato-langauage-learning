from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Material(models.Model):
    FREE_DOWNLOAD = 'free'
    PREMIUM = 'premium'

    TYPE_CHOICES = [
        (FREE_DOWNLOAD, 'Free Download'),
        (PREMIUM, 'Premium'),
    ]
    your_language = models.ForeignKey(Language, related_name='your_language_materials',on_delete=models.CASCADE)
    foreign_language = models.ForeignKey(Language, related_name='foreign_language_materials',on_delete=models.CASCADE)
    file = models.FileField(upload_to='material/')
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=FREE_DOWNLOAD)

    def __str__(self):
        return f"{self.type} - {self.your_language} - {self.foreign_language} - {self.file.name}"
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paymentsstatus = models.TextField(null=True, blank=True)
    
class Favouritetopic(models.Model):
    title = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.title
    
class Interest(models.Model):
    title = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.title   

class Userdetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    firstname = models.TextField(null=True, blank=True)
    lastname = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    Gender = models.TextField(null=True, blank=True)
    Country = models.TextField(null=True, blank=True)
    interests = models.ManyToManyField(Interest, blank=True)
    favourite_topics = models.ManyToManyField(Favouritetopic, blank=True)
    your_language = models.ManyToManyField(Language, blank=True)

    def __str__(self):
        return f"{self.firstname}'s Userdetails"
   

