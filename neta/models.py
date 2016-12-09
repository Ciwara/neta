from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class OwnerManager(BaseUserManager):

    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Owner(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    localite = models.CharField(max_length=100)

    objects = OwnerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

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


class ModelVehicle(models.Model):

    class Meta:
        verbose_name = "Modele"
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Made(models.Model):

    class Meta:
        verbose_name = "Marque"
    name = models.CharField(max_length=100, verbose_name="Nom")
    country = models.CharField(
        max_length=100, verbose_name="Pays de fabrication")

    def __str__(self):
        return "{name}/{country}".format(name=self.name, country=self.country)


class Vehicle(models.Model):

    class Meta:
        verbose_name = "Engin"

    owner = models.ForeignKey(UserSocialAuth, on_delete=models.CASCADE)
    model_vehicle = models.ForeignKey(ModelVehicle, verbose_name="Modele")
    made = models.ForeignKey(Made, verbose_name="Marque")
    release_date = models.DateField()
    # num_stars = models.IntegerField()
    # year = models.DateField()
    number = models.CharField(max_length=100)
    certify = models.BooleanField(default=False)
    lost = models.BooleanField(default=False)

    def __str__(self):
        return "{owner}/{model_v}/{certify}/{lost}".format(owner=self.owner,
                                                           model_v=self.model_vehicle, certify=self.certify, lost=self.lost)


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
