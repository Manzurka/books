# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def validation(self, postData):
        errors={}
        if len(postData['name']) > 0:
            if len(postData['name']) < 3:
                errors['name']="Name should be at least 3 characters!"
        else: 
            errors['name']="Name is required!"

        if len(postData['username']) > 0:
            if len(postData['username']) < 3:
                errors['username']="Username should be at least 3 characters!"  
        else: 
            errors['username']="Username is required!"

        if len(postData['password']) > 0:
            if len(postData['password']) < 8:
                errors['password']="Password is less than 8 characters!"
        else: 
             errors['password']="Password is required!"
       
        if postData['pw_confirmation']!= postData['password']:
            errors['password']="Password should match!"
       
        return errors

    def login_validation(self, postData):
        errors={}
        if User.objects.filter(username=postData['username']):
            user=User.objects.filter(username=postData['username'])
            if (bcrypt.checkpw(postData['password'].encode(), user[0].password.encode())):
                errors['login'] = "Successfully logged in!"
            if not (bcrypt.checkpw(postData['password'].encode(), user[0].password.encode())):
               errors['login'] = "Invalid password!"
        if not User.objects.filter(username=postData['username']): 
                errors['login'] = "Please register first!"
        
        return errors

class User(models.Model):
    name=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=25)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    objects=UserManager()

class ItemManager(models.Manager):
    def item_validation(self, postData):
        errors={}
        if len(postData['item_name']) == 0:
            errors['item_name']="Item name cannot be empty!"
        if len(postData['item_name']) <= 3:
                errors['item_name']="Item name should be more than 3 characters!"
        if self.filter(item_name=postData['item_name']):
            errors['item_name']="This item is in our catalog!"
        
        return errors

class Item(models.Model):
    item_name=models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name = "created_items")
    users = models.ManyToManyField(User, related_name = "liked_items")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    objects=ItemManager()
