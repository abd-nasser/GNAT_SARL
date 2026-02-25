from django.db import models

# Create your models here.
class Vehicule(models.Model):
    proprietaire = models.OneToOneField('client_app.Client', on_delete=models.CASCADE, related_name='vehicules')
    immatriculation = models.CharField(max_length=20, unique=True)
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    annee = models.PositiveIntegerField()
    couleur = models.CharField(max_length=30)
    kilometrage = models.PositiveIntegerField()
    employe_affecte = models.ForeignKey('auth_app.Personnel', on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicules_affectes')
    
    def __str__(self):
        return f"{self.marque} {self.modele} ({self.immatriculation})"