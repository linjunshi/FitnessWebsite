#coding: utf-8

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

def user_directory_path (instance, filename):
    return 'uploads/user_{0}/filename'.format(instance.user_id, filename)

# Create your models here.
# USERS
# only password, email(unique), email_registered, and username are not null,
# we allow username to not be unique
class UserAccounts (models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=64)
    email_verified = models.BooleanField(default=False)
    # email_registered = models.IntegerField(default=0)
    secure_token = models.CharField(max_length=50, null=True, blank=True)
    forgotten_token = models.CharField(max_length=50, null=True, blank=True)
    forgotten_token_created = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    last_location_lat = models.DecimalField(max_digits=10, decimal_places=7, default=0.000000, null=True, blank=True)
    last_location_long = models.DecimalField(max_digits=10, decimal_places=7, default=0.000000, null=True, blank=True)
    user_avatar_dir = models.CharField(max_length=50, null=True, blank=True, default='/img/avatar1.jpg')
    age = models.IntegerField(null=True, blank=True)
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    # kg
    weight = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    # cm
    height = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    blood_pressure_systolic = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blood_pressure_diastolic = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    athlete = models.BooleanField(default=False)
    heart_disease = models.BooleanField(default=False)
    smoking = models.BooleanField(default=False)
    medical_implant = models.BooleanField(default=False)
    attendence = models.IntegerField(default = 0)
    last_attend_date = models.CharField(max_length=30, null=True, blank=True)
    training_target = models.CharField(max_length=20, null=True, blank=True)
    classification = models.IntegerField(default = 0)

    def my_property(self):
        return self.username + ' ' + ' registered email: ' + self.email_registered
    my_property.short_description = "Brief information of the user"

    brief_info = property(my_property)


    def __str__(self):
        return "%s -- %s" % (self.username, self.email)


class Chat(models.Model):
    date = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(UserAccounts,related_name='chatting_user', on_delete=models.CASCADE )
    message = models.CharField(max_length=200)


class FriendsList (models.Model):
    friend1 = models.ForeignKey(UserAccounts, related_name='friendList_1', on_delete=models.CASCADE)
    friend2 = models.ForeignKey(UserAccounts, related_name='friendList_2', on_delete=models.CASCADE)


#FOOD
class FoodClasses (models.Model):
    name = models.CharField(max_length=20)

class FoodDetail (models.Model):
    classes = models.ManyToManyField(FoodClasses, related_name='foodDetail_class')
    name = models.CharField(max_length=50)
    energy = models.DecimalField(max_digits=6, decimal_places=3)
    carbohydrates = models.DecimalField(max_digits=6, decimal_places=3)
    saturated_fat = models.DecimalField(max_digits=6, decimal_places=3)
    polyunsaturated_fat = models.DecimalField(max_digits=6, decimal_places=3)
    monounsaturated_fat = models.DecimalField(max_digits=6, decimal_places=3)
    trans_fat = models.DecimalField(max_digits=6, decimal_places=3)
    gluten = models.BooleanField(default=False)
    cholesterol = models.DecimalField(max_digits=6, decimal_places=3)
    protein = models.DecimalField(max_digits=6, decimal_places=3)

class FoodSubClass (models.Model):
    parent = models.ForeignKey(FoodClasses, related_name='foodSubClass_parent', on_delete=models.CASCADE)
    child = models.ForeignKey(FoodClasses, related_name='foodSubClass_child', on_delete=models.CASCADE)

#FITNESS
class FitnessCategories (models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return "%s" % (self.name )

# Fitness videos upload
# @author John/Egbert
class FitnessVideo (models.Model):
    uploaded_by = models.ForeignKey(UserAccounts, related_name='fitnessVideo_uploadedBy', on_delete=models.CASCADE)
    category = models.ForeignKey(FitnessCategories, related_name='fitnessVideo_category', on_delete=models.CASCADE)
    link = models.CharField(max_length=200, unique=True)

    name = models.CharField(u'Video Name' ,max_length=200)
    description = models.CharField(u'Description',max_length=200, null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)

    #uploaded date and update_date
    uploaded_date = models.DateTimeField(u'Published on', auto_now_add=True, editable = True, null=True, blank=True)
    update_date = models.DateTimeField(u'Updated On', auto_now=True, null=True, blank=True)

    likes = models.PositiveIntegerField(default = 0)
    dislikes = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.name



class FitnessSubCategories (models.Model):
    parent = models.ForeignKey(FitnessCategories, related_name='fitnessSubCat_parent', on_delete=models.CASCADE)
    child = models.ForeignKey(FitnessCategories, related_name='fitnessSubCat_child', on_delete=models.CASCADE)

class FitnessEquipment (models.Model):
    cat = models.ManyToManyField(FitnessCategories, related_name='fitnessEquipment_cat')
    name = models.CharField(max_length=20)

#RECIPES
class Ingredients (models.Model):
    food = models.ForeignKey(FoodDetail, related_name='ingredients_food', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=5)
    amount_units = models.CharField(max_length=5)

    def __str__(self):
        return self.food.food_name


class Recipe (models.Model):
    name = models.CharField(max_length=20)
    ingredients = models.ManyToManyField(Ingredients, related_name='recipe_ingredients')
    description = models.CharField(max_length=255)


class VideosReview (models.Model):
    user = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)
    video = models.ForeignKey(FitnessVideo, on_delete=models.CASCADE)
    target = models.CharField(null=True, blank=True, max_length=50)
    review = models.IntegerField(null=True, blank=True, default=0)
