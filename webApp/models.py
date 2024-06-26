from django.db import models
import datetime
import os
from django.contrib.auth.models import User
from django.utils import timezone
import datetime 
from django.contrib.auth.models import AbstractUser

def get_file(request,filename):
    now=datetime.datetime.now().strftime('%Y%d%H:%M:%S')
    Nowfilename='%s%s'%(now,filename)
    return os.path.join('upload/',Nowfilename)


class Category(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    image=models.ImageField(upload_to=get_file,null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text='0-show , 1-hidden')
    
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=False,blank=False)
    image=models.ImageField(upload_to=get_file,null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text='0-show , 1-hidden')
    trending=models.BooleanField(default=False,help_text='0-show , 1-hidden')
    created_at=models.DateTimeField(auto_now_add=True)
    vendor = models.CharField(max_length=100,null=False,blank=False)
    quantity=models.IntegerField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_quantity=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

class Fav(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)



class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    name=models.CharField(null=False,blank=False,max_length=100)
    product_quantity=models.IntegerField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    total_amount=models.FloatField(null=False,blank=False)
    number= models.IntegerField(null=False,blank=False)
    alt_number= models.IntegerField(null=False,blank=False)
    address=models.TextField(max_length=500,null=False,blank=False)
    payment_type=models.CharField(max_length=100,null=False,blank=False)
    date=models.DateTimeField(default=timezone.now)
    


    
class Slider(models.Model):
    title=models.CharField(max_length=100,null=True,blank=True)
    image=models.ImageField(upload_to=get_file,null=False,blank=False)
    description=models.TextField(max_length=100,null=True,blank=True)
    duration=models.DateTimeField(verbose_name="Duration", null=False, default=datetime.datetime.now)
    status=models.BooleanField(default=False,help_text='0-show , 1-hidden')

