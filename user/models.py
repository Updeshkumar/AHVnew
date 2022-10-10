from django.db import models
from rest_framework import status
from config.configConstants import UserType

# Create your models here.

# This class is used to create the User model
class MasterContents(models.Model):
    Id = models.AutoField(primary_key=True)
    key = models.CharField(max_length = 200)
    value = models.CharField(max_length = 200)
    relate_to = models.IntegerField()
    class Meta:
        db_table = 'user_mastercontents'

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    country_code = models.IntegerField(91, null=True,blank=True)
    mobile_number = models.IntegerField(blank=True, null=True)
    otp = models.CharField(max_length=4,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(default=False, null=True)
    email_id = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=20,null=False,blank=False, default="USER")
    profile_pic = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=1,null=False)
    is_delete = models.BooleanField(default=0,null=False)
    gender = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'user'

#  This class is use for create the preference model
class Device(models.Model):

    device_id = models.AutoField(primary_key=True)
    refresh_token = models.CharField(max_length=500,default=False, null=True)
    device_type = models.CharField(max_length=20)
    device_token = models.CharField(max_length=255,default=False, null=True)
    aws_arn = models.CharField(max_length=255, null=True)
    created_by =  models.ForeignKey(User, db_column = 'created_by',related_name='device_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1,null=False)
    
    class Meta:
        db_table = 'device'


# create models heavey vehical registrations details #

# vehical Basic details

class vehicalbasicdetail(models.Model):
    vehical_name = models.CharField(max_length=200)
    vehical_number = models.CharField(max_length=500)
    model_number = models.CharField(max_length=500)
    ownername = models.CharField(max_length=300)
    Aadhar_number = models.CharField(max_length=20)
    class Meta:
        db_table = 'vehicalbasicdetail'
