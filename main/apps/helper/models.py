from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
import bcrypt
import re

#**************************Handy Helper***********************

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        # CHECKING IF FNAME AND LNAME ARE AT LEAST 2 CHARACTERS
        if len(postData['fname'])<2: 
            errors['fname'] = "First Name should be at least 2 characters."
        if len(postData['lname'])<2: 
            errors['lname'] = "Last Name should be at least 2 characters."
        # CHECKING PASSWORD TO BE 8 CHARACTERS, A NUMBER, CAPITAL, LOWERCASE, AND MATCH
        if len(postData['password'])<8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['checkpassword']:
            errors['nomatch'] = "Passwords must match."
        if not re.match('.*[0-9]', postData['password']):
            errors['pwnumber'] = "Your password must contain a number"
        if not re.match('.*[A-Z]', postData['password']):
            errors['pwupper'] = "Your password must contain at least 1 upper case character."
        if not re.match('.*[a-z]', postData['password']):
            errors['pwlower'] = "Your password must contain at least 1 lower case character." 
        # CHECKING EMAIL VALID FORMAT AND IN DATABASE
        if not EMAIL_REGEX.match(postData['email']):
            errors['format'] = "Invalid email address."
        if len(User.objects.filter(email=postData['email']))>0:
            errors['inuse'] = "Email in use."
        return errors

    def login_validator(self, postData):
        errors={}
        cemail = postData['email']
        user=User.objects.filter(email=cemail)
        print(user)
        # CHECKING EMAIL IN DATABASE
        if not EMAIL_REGEX.match(postData['email']):
            errors['emailformat'] = "Invalid login."
        if len(user)<1:
            errors['emailnot'] = "Invalid login."
        # CHECKING PASSWORD TO BE 8 CHARACTERS, A NUMBER, CAPITAL, LOWERCASE, AND MATCH
        elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['pwfail'] = "Invalid login."
        return errors

class JobManager(models.Manager):
    def job_validator(self, postData):
        errors={}
        # CHECKING JOB, DESCRIPTION, AND LOCATION NOT EMPTY AND AT LEAST 3 CHARACTERS
        if len(postData['job'])<3:
            errors["job"]= "Job title must be at least 3 characters!"
        if len(postData['description'])<3:
            errors["description"]= "Description must be at least 3 characters!"
        if len(postData['location'])<3:
            errors["location"]= "Location must be at least 3 characters!"
        # must submit or choose at least one category
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name =models.CharField(max_length=255)
    email =models.CharField(max_length=255)
    password =models.CharField(max_length=255)
    created_at =models.DateField(auto_now_add=True)
    updated_at =models.DateField(auto_now=True)
    objects =UserManager()

class Category(models.Model):
    name=models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
class Job(models.Model):
    job = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='my_jobs')
    helper = models.ManyToManyField(User,related_name="jobs")
    category= models.ManyToManyField(Category, related_name="jobs")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects =JobManager()


# Create your models here.
