from django.db import models

# Create your models here.
class TypeReparation(models.Model):
    CATEFORIE_CHOICES = [
        ('Mécanique', 'Mécanique'),
        ('Électrique', 'Électrique'),
        ('Carrosserie', 'Carrosserie'),
        ('Peinture', 'Peinture'),
        ('Pneumatique', 'Pneumatique'),
        ('Entretien', 'Entretien'),
        ('Diagnostic', 'Diagnostic'),
        ("climatisation", "climatisation"),
        ("lavage", "lavage"),
        ('Autre', 'Autre'),
    ]
    nom = models.CharField(max_length=100, choices=CATEFORIE_CHOICES)
    description = models.TextField()
    
    def __str__(self):
        return self.nom
    


class ReparationOrdre(models.Model):
    reference = models.CharField(max_length=20, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    vehicule = models.ForeignKey('vehicul_app.Vehicule', on_delete=models.CASCADE, related_name='ordres_de_reparation')
    type_reparation = models.ForeignKey(TypeReparation, on_delete=models.SET_NULL, null=True, related_name='ordres_de_reparation')
    description = models.TextField()    