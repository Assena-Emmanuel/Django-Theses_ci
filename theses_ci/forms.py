from django import forms
from .models import Theses, Directeurs, Institutions, MembreJury, Domaines, Specialites
from django.forms import inlineformset_factory

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institutions
        fields = '__all__'
        widgets = {
            "nom":forms.TextInput(attrs={"class":"form-control form-control-sm", "id":"nom",}),
        }

class DomainesForm(forms.ModelForm):
    class Meta:
        model = Domaines
        fields = ['libelle']
        widgets = {
            "libelle":forms.TextInput(attrs={"class":"form-control form-control-sm", "id":"mot-cle",}),
        }
        


class SpecialiteForm(forms.ModelForm):
    class Meta:
        model = Specialites
        fields = ['libelle']
        widgets = {
            "libelle":forms.TextInput(attrs={"class":"form-control form-control-sm", "id":"mot-cle",}),
        }

class ThesesForm(forms.ModelForm):
    class Meta:
        model = Theses
        exclude = ['domaine', 'directeur', 'jury', 'specialite', 'institution']
        widgets = {
            "auteur_nom":forms.TextInput(attrs={"class":"form-control form-control-sm rounded-0", }),
            "auteur_prenom":forms.TextInput(attrs={"class":"form-control form-control-sm rounded-0", }),
            "auteur_email":forms.EmailInput(attrs={"class":"form-control form-control-sm rounded-0", }),
            "theme":forms.TextInput(attrs={"class":"form-control form-control-sm rounded-0", }),
            "resume":forms.Textarea(attrs={"class":"form-control form-control-sm rounded-0", }),
            "mot_cle":forms.Textarea(attrs={"class":"form-control form-control-sm rounded-0", 'rows':4}),
            "date_soutenance": forms.DateInput(attrs={"class": "form-control form-control-sm rounded-0", "type": "date"}),
            "specialite":forms.Select(attrs={"class":"form-select form-select-sm rounded-0", }),
            # "domaine":forms.Select(attrs={"class":"form-select form-select-sm rounded-0", }),
            "institution": forms.Select(attrs={"class": "form-control form-select-sm rounded-0"}),
        }


class DirecteurForm(forms.ModelForm):
    class Meta:
        model = Directeurs
        fields = '__all__'
        widgets = {
            "dr_nom_prenom":forms.TextInput(attrs={"name":"dr_nom_prenom[]", "class":"form-control form-control-sm rounded-0", "id":"nom", 'placeholder':'Nom et Prenom'}),
            "dr_email":forms.EmailInput(attrs={"name":"dr_email[]", "class":"form-control form-control-sm rounded-0 ", "id":"email" , 'placeholder':'Email'}),
            "dr_universite":forms.Select(attrs={"name":"dr_universite[]", "class":"form-select form-select-sm rounded-0 ", "id":"dr_universite"}),
        }


class MembrejuryForm(forms.ModelForm):
    class Meta:
        model = MembreJury
        fields = '__all__'
        widgets = {
            "nom_prenom":forms.TextInput(attrs={"name":"nom_prenom[]","class":"form-control form-control-sm rounded-0 ", "id":"nom",}),
            "email":forms.EmailInput(attrs={"name":"email[]", "class":"form-control form-control-sm rounded-0", "id":"email"}),
            "universite":forms.Select(attrs={"name":"universite[]", "class":"form-select form-select-sm rounded-0", "id":"email"}),
            "role":forms.Select(attrs={"name":"role[]", "class":"form-select form-select-sm rounded-0", "id":"email"}),

        }

