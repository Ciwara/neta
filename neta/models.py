#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager, PermissionsMixin)

from django.db import models


class OwnerManager(BaseUserManager):

    def create_user(self, email, phone, full_name, date_of_birth=None,
                    password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError('Users must have an email address')

        user = self.model(
            # email=self.normalize_email(email),
            # date_of_birth=date_of_birth,
            phone=phone,
            full_name=full_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name, password,
                         email=None, date_of_birth=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            # date_of_birth=date_of_birth,
            phone=phone,
            full_name=full_name
        )
        user.is_admin = True
        user.is_active = True
        # user.has_perm = True
        user.save(using=self._db)
        return user


class Owner(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=True, verbose_name='email address',
                              max_length=255, unique=True, blank=True,)
    phone = models.IntegerField(unique=True)
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    localite = models.CharField(max_length=100, blank=True)

    objects = OwnerManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2

        if self.full_name:
            return self.full_name
        else:
            return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Made(models.Model):

    class Meta:
        verbose_name = "Marque"
    name = models.CharField(max_length=100, verbose_name="Nom")
    country = models.CharField(
        max_length=100, verbose_name="Pays de fabrication")

    def __str__(self):
        return "{name}/{country}".format(name=self.name, country=self.country)


class ModelVehicle(models.Model):

    class Meta:
        verbose_name = "Modele"
    name = models.CharField(max_length=100)
    made = models.ForeignKey(Made, verbose_name="Marque")

    def __str__(self):
        return "{} ({})".format(self.name, self.made)


class Vehicle(models.Model):

    class Meta:
        verbose_name = "Engin"

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    model_vehicle = models.ForeignKey(ModelVehicle, verbose_name="Modele")
    release_date = models.DateField()
    # num_stars = models.IntegerField()
    # year = models.DateField()
    number = models.CharField(max_length=100, unique=True)
    certify = models.BooleanField(default=False)
    lost = models.BooleanField(default=False)

    def __str__(self):
        return "{} {} {}".format(self.number, self.lost, self.certify)

    # def __str__(self):
    #     return "{owner}/{model_v}/{certify}/{lost}".format(
    #         owner=self.owner, model_v=self.model_vehicle, certify=self.certify,
    #         lost=self.lost)


class AttachedFile(models.Model):

    class Meta:
        verbose_name = "Fichier joint"

    DOC_TYPE = (
        ('V', 'Vignette'),
        ('F', 'Facture'),
    )
    doc_type = models.CharField(max_length=1, choices=DOC_TYPE)
    doc = models.FileField(upload_to='uploads/%Y/%m/%d/')
    vehicle = models.ForeignKey(Vehicle)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.doc_type
