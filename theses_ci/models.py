from django.db import models
from django.utils.translation import gettext_lazy as _

class Institutions(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom
    
class Specialites(models.Model):
    libelle = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.libelle}"


class Domaines(models.Model):
    libelle = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.libelle}"

class Directeurs(models.Model):
    dr_nom_prenom = models.CharField(max_length=150)
    dr_email = models.EmailField()
    dr_universite = models.ForeignKey(Institutions, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dr_nom_prenom}"
    



class MembreJury(models.Model):
    Choix = [
        ("", "Role..."),
        ("PRESIDENT", "PRESIDENT"),
        ("EXAMINATEUR", "EXAMINATEUR"),
        ("RAPPORTEUR", "RAPPORTEUR"),
        ]
        
    nom_prenom = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=Choix)
    universite = models.ForeignKey(Institutions, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom_prenom}"


class Theses(models.Model):
    auteur_nom = models.CharField(max_length=105, verbose_name="Nom")
    auteur_prenom = models.CharField(max_length=150)
    auteur_email = models.EmailField(max_length=100, )
    theme = models.CharField(max_length=255, unique=True)
    resume = models.TextField()
    domaine = models.ForeignKey(Domaines, on_delete=models.CASCADE)
    date_soutenance = models.DateField()
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institutions, on_delete=models.CASCADE)
    directeur = models.ManyToManyField(Directeurs)
    jury = models.ManyToManyField(MembreJury)
    mot_cle = models.TextField()

    def __str__(self):
        return self.theme
    

