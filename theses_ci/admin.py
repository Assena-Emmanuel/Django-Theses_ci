from django.contrib import admin
from .models import Directeurs, MembreJury, Domaines, Specialites, Institutions, Theses

@admin.register(Domaines)
class AuteursAdmin(admin.ModelAdmin):
    list_display = ['libelle',]

@admin.register(Specialites)
class UniversitesAdmin(admin.ModelAdmin):
    list_display = ['libelle',]

@admin.register(Directeurs)
class DirecteursAdmin(admin.ModelAdmin):
    list_display = ['dr_nom_prenom', 'dr_email', 'dr_universite']

@admin.register(MembreJury)
class ExaminateursAdmin(admin.ModelAdmin):
    list_display = ['nom_prenom', 'email', 'universite', 'role']

@admin.register(Institutions)
class InstitutionsAdmin(admin.ModelAdmin):
    list_display = ['nom',]


@admin.register(Theses)
class ThesesAdmin(admin.ModelAdmin):
    list_display = ['auteur_nom','auteur_prenom','theme', 'resume', 'mot_cle', 'specialite', 'domaine',]
    list_filter = ['date_soutenance', 'specialite', 'domaine', 'institution', 'domaine']
    search_fields = ['theme', 'auteur_nom', 'auteur_prenom', 'universite__nom']

