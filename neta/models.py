from django.db import models


class Owner(models.Model):

    class Meta:
        verbose_name = "Propriétaire"

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.IntegerField(verbose_name="Téléphone")
    localite = models.CharField(max_length=100)

    def __str__(self):
        return "{}{}".format(self.first_name, self.last_name)


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

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    model_vehicle = models.ForeignKey(ModelVehicle, verbose_name="Modele")
    made = models.ForeignKey(Made, verbose_name="Marque")
    release_date = models.DateField()
    # num_stars = models.IntegerField()
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
