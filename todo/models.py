from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#class User(models.Model):
 #   email = models.EmailField(max_length=254)
  #  pswd = models.CharField(max_length=200)
   # name_first = models.CharField(max_length=200)
    #name_last = models.CharField(max_length=200)
    #prof_img = models.ImageField(upload_to='images/')

    #def __str__(self):
     #   return self.name_first
    
class UserImg(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prof_img = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.user.username

class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=200)
    create_date = models.DateTimeField("Date Created")
    cover_img = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.list_name

class ListItem(models.Model):
    item_list = models.ForeignKey(List, on_delete=models.CASCADE)
    item_text = models.CharField(max_length=200)
    add_date = models.DateField("Date added")
    is_complete = models.BooleanField(default=False)
    complete_date = models.DateField("Date completed", blank=True, null=True)

    def __str__(self):
        return self.item_text
    
