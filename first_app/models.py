from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime,date
import re

# Create your models here.
class UserManager(models.Manager):
    def create_validator(self,reqPost):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        email=User.objects.filter(email=reqPost['email'])
        if len(reqPost['first_name'])<2:
                errors['firstname']="firstname must be at least 2 characters"
        if len(reqPost['last_name'])<2:
                errors['lastname']="lastname must be at least 2 characters"
        if len(email)>=1:
            errors['unique_email']="email is already taken"
        if not EMAIL_REGEX.match(reqPost['email']):
            errors['email'] = "email not according to format [a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$"
        if len(reqPost['password'])<8:
                errors['password']="passwords must be at least 8 characters"
        return(errors)

class OrganizationManager(models.Manager):
    def create_validator(self,reqPost):
        errors={}
        if reqPost['name']=='':
            errors['empty_name']='Organization name cant be empty'
        else:
            if len(reqPost['name'])<5:
                errors['name_short']="Organization name should be more than 5 characters" 
        if reqPost['desc']=='':
            errors['empty_desc']='description cant be empty'
        else:
            if (len(reqPost['desc']))<10:
                errors['desc'] ="Desciption should be more than 10 characters" 
        return errors

class User(models.Model):
    first_name=models.TextField()
    last_name=models.TextField()
    email=models.TextField()
    password=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    @property
    def full_name(self):
        return(f"{self.first_name} {self.last_name}")

class Organization(models.Model):
    name=models.TextField()
    desc=models.TextField()
    creator=models.ForeignKey(User, related_name="org_created",on_delete=models.CASCADE)
    members=models.ManyToManyField(User, related_name="org_joined")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=OrganizationManager()

