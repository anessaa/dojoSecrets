# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def validate(self,request):
        errors = []
        if len(request.POST['first_name']) < 2:
            errors.append('First name must be more than two letters long.')
        if not request.POST['first_name'].isalpha():
            errors.append('First name can only contain letters.')
        if len(request.POST['last_name']) < 2:
            errors.append('Last name must be more than two letters long.')
        if not request.POST['last_name'].isalpha():
            errors.append('Last name can only contain letters.')
        if not EMAIL_REGEX.match(request.POST['email']):
            errors.append('Invalid email address.')
        if len(request.POST['password']) < 8:
            errors.append('Password must be at least 8 charachters.')
        if not request.POST['password'] == request.POST['confirm_pw']:
            errors.append('Password and confirmation password do not match')
        if User.objects.filter(email=request.POST['email']):
            errors.append('Email is registered')
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Secret(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    

class Like(models.Model):
    user = models.ForeignKey(User)
    secret = models.ForeignKey(Secret)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
