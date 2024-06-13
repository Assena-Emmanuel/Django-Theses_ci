# utils.py

from django.conf import settings
import os

def handle_uploaded_file(f):
    # Définir le chemin du sous-dossier 'theses' dans MEDIA_ROOT
    theses_directory = os.path.join(settings.MEDIA_ROOT, 'theses')
    # Assurer que le dossier 'theses' existe, s'il n'existe pas déjà
    os.makedirs(theses_directory, exist_ok=True)
    # Chemin complet où le fichier sera enregistré dans le sous-dossier 'theses'
    file_path = os.path.join(theses_directory, f.name)
    
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    return file_path
