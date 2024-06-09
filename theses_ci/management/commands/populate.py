import random
from faker import Faker
from django.core.management.base import BaseCommand
from ...models import Directeurs, MembreJury, Theses, Institutions, Domaines, Specialites

class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Créer quelques institutions, domaines, et spécialités pour les relations
        institutions = [Institutions.objects.create(nom=fake.company()) for _ in range(5)]
        domaines = [Domaines.objects.create(libelle=fake.word()) for _ in range(5)]
        specialites = [Specialites.objects.create(libelle=fake.word()) for _ in range(5)]

        # Créer des directeurs
        directeurs = []
        for _ in range(30):
            directeur = Directeurs.objects.create(
                dr_nom_prenom=fake.name(),
                dr_email=fake.email(),
                dr_universite=random.choice(institutions)
            )
            directeurs.append(directeur)

        # Créer des thèses
        for _ in range(20):
            these = Theses.objects.create(
                auteur_nom=fake.last_name(),
                auteur_prenom=fake.first_name(),
                auteur_email=fake.email(),
                theme=fake.sentence(nb_words=15*random.randint(3, 9)),
                resume=fake.texts(nb_texts=20),
                domaine=random.choice(domaines),
                date_soutenance=fake.date_between(start_date='-5y', end_date='today'),
                specialite=random.choice(specialites),
                institution=random.choice(institutions),
                mot_cle=', '.join(fake.words(nb=5))
            )
            # Ajouter des directeurs
            these.directeur.set(random.sample(directeurs, k=random.randint(1, 3)))
            these.save()

            # Créer des membres de jury
            membres_jury = []
            roles = ["EXAMINATEUR", "RAPPORTEUR"]

            # Ajouter un président
            president = MembreJury.objects.create(
                nom_prenom=fake.name(),
                email=fake.unique.email(),
                role="PRESIDENT",
                universite=random.choice(institutions)
            )
            membres_jury.append(president)

            # Ajouter au moins un rapporteur
            rapporteur = MembreJury.objects.create(
                nom_prenom=fake.name(),
                email=fake.unique.email(),
                role="RAPPORTEUR",
                universite=random.choice(institutions)
            )
            membres_jury.append(rapporteur)

            # Ajouter au moins un examinateur
            examinateur = MembreJury.objects.create(
                nom_prenom=fake.name(),
                email=fake.unique.email(),
                role="EXAMINATEUR",
                universite=random.choice(institutions)
            )
            membres_jury.append(examinateur)

            # Ajouter d'autres membres
            for _ in range(random.randint(1, 3)):
                membre = MembreJury.objects.create(
                    nom_prenom=fake.name(),
                    email=fake.unique.email(),
                    role=random.choice(roles),
                    universite=random.choice(institutions)
                )
                membres_jury.append(membre)

            these.jury.set(membres_jury)
            these.save()

        # Message de succès
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake data'))
