from django.shortcuts import render, redirect, get_object_or_404
from .forms import ThesesForm , DirecteurForm, MembrejuryForm 
from .models import Domaines, Specialites, Institutions, Theses, Directeurs, MembreJury
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import ExtractYear

    
  

def index(request):
    context = {}
    nb_these = Theses.objects.count()
    nb_auteur = len(set(Theses.objects.values_list('auteur_email', flat=True)))
    nb_directeur = len(set(Directeurs.objects.values_list('dr_email', flat=True)))
    nb_membrejury = len(set(MembreJury.objects.values_list('email', flat=True)))
    
    context["personne_liees_aux_theses"] = nb_auteur + nb_directeur + nb_membrejury
    context["nb_these"] = nb_these
    # Récupérer tous les mots clés de la table These
    mots_cles = Theses.objects.values_list('mot_cle', flat=True)

    # Si les mots clés sont stockés comme une chaîne de caractères séparés par des virgules
    tous_mots_cles = []
    for mc in mots_cles:
        if mc:
            tous_mots_cles.extend(mc.split(','))

    # Enlever les éventuels espaces et nettoyer les mots clés
    context["mots_cles"] = list(set([mot.strip() for mot in tous_mots_cles]))

    # Récupérer le nombre de thèses par année
    theses_par_annee = Theses.objects.values('date_soutenance').annotate(count=Count('id')).order_by('date_soutenance')
    context['theses_par_annee'] = theses_par_annee
     

    return render(request, "theses_ci/contenu/index.html", context)

def resultat(request):
    context = {}
    etablissement = Institutions.objects.all()
    domaines = Domaines.objects.all()
    specialites = Specialites.objects.all()
    dates = Theses.objects.values_list('date_soutenance', flat=True)
    
    context["specialites"] = specialites
    context["domaines"] = domaines
    context["etablissements"] = etablissement
    # Récupérer tous les mots clés de la table These
    mots_cles = Theses.objects.values_list('mot_cle', flat=True)

    # Si les mots clés sont stockés comme une chaîne de caractères séparés par des virgules
    tous_mots_cles = []
    for mc in mots_cles:
        if mc:
            tous_mots_cles.extend(mc.split(','))

    # Enlever les éventuels espaces et nettoyer les mots clés
    context["mots_cles"] = list(set([mot.strip() for mot in tous_mots_cles]))
     
    if request.method == "POST":
        terme = request.POST["mot_cle"]
        context["terme"] = terme
        theses = Theses.objects.select_related('domaine', 'specialite', 'institution').prefetch_related('directeur').filter(mot_cle__icontains=terme)
        context["theses"] = theses
                                        

    return render(request, "theses_ci/contenu/resultat.html", context)



def detail(request, these_id):

    theses = get_object_or_404(Theses.objects.select_related('domaine', 'specialite', 'institution').prefetch_related('directeur', 'jury'), id=these_id)
    directeurs = theses.directeur.all()
    jurys = theses.jury.all()
    mots_cles = theses.mot_cle.split(',')
    print("-----------------",mots_cles)

    return render(request, 'theses_ci/contenu/detail.html',{'theses':theses, 'directeurs':directeurs, 'jurys':jurys, 'mots_cles':mots_cles})



def succes(request):
    return render(request, 'theses_ci/contenu/succes.html')

# retourne la valeur non nulle dans une liste de deux valeurs
def non_null(liste):
    if len(liste)==2:
        if liste[0] != liste[-1]:
            nonnul =list(filter(lambda x: x != '', liste))
            return ''.join(nonnul)
        else:
            return liste[0]

def these_etape1(request):
    d = Domaines.objects.all()
    specialite = Specialites.objects.all()
    univ =Institutions.objects.all()

    if request.method == 'POST':
        these_form = ThesesForm(request.POST)
        
        if these_form.is_valid():
            request.session['etape1'] = request.POST
            sess = dict(request.session.get('etape1'))
            print(f"<<<<: {sess['domaine']}")
            request.session['etape1_saisie'] = {
                'domaine': non_null(sess['domaine']),
                'specialite': non_null(sess['specialite']),
                'universite': non_null(sess['universite']),
            }

            print(f"ok etape 1--> {request.POST.get('domaine')}")
            r = dict(request.session.get('etape1'))
            print(f"-----> session: {r}")
            return redirect('theses_ci:these_etape2')
    
        else:
            print(f"--------> {these_form.errors}")
        
    else:
        these_form = ThesesForm()

    context = {
        'these': these_form,
        'domaines_values': d,
        'specialites': specialite,
        'universite': univ,

    }
    return render(request, 'theses_ci/contenu/create_these.html', context)

def precedent(request):
    these_form = ThesesForm(initial=request.session.get('etape1', {}))
    d = Domaines.objects.all()
    specialite = Specialites.objects.all()
    univ =Institutions.objects.all()

    session_valeur = dict(request.session.get('etape1_saisie'))
    print(f"->: {session_valeur}")
    

    d_saisie = session_valeur['domaine']
    specialite_saisie= session_valeur['specialite']
    universite_saise = session_valeur['universite']

    context = {
        'these': these_form,
        'domaines_values': d,
        'specialites': specialite,
        'universite': univ,
        'd_saisie':d_saisie,
        'specialite_saisie':specialite_saisie,
        'universite_saise':universite_saise,


    }
    return render(request, 'theses_ci/contenu/create_these.html', context)

def these_etape2(request):
    univ =Institutions.objects.all()
    context = {'universites':univ}
    if request.method == 'POST':
        membrejury_form = MembrejuryForm(request.POST)
        directeur_form = DirecteurForm(request.POST)
        
        if  membrejury_form.is_valid() and directeur_form.is_valid():
            
            session = dict(request.session.get('etape1'))
            session_valeur = dict(request.session.get('etape1_saisie'))

            # verification de l'existance  
            domaine, _ = Domaines.objects.get_or_create(libelle=session_valeur['domaine'])
            specialite, _ = Specialites.objects.get_or_create(libelle=session_valeur['specialite'])
            universite, _ = Institutions.objects.get_or_create(nom=session_valeur['universite'])


            
            these, created = Theses.objects.get_or_create(
                theme=session['theme'],
                defaults={
                    'auteur_nom': session['auteur_nom'],
                    'auteur_prenom': session['auteur_prenom'],
                    'auteur_email': session['auteur_email'],
                    'resume': session['resume'],
                    'domaine': domaine,
                    'date_soutenance': session['date_soutenance'],
                    'specialite': specialite,
                    'institution': universite,
                    'mot_cle': session['mot_cle'],
                }
            )


            # Ajouter les membres du jury 
            donnees_etape2 = dict(request.POST)

            # Enregistrer le(s) directeur(s) de these
            nombre_docteur = len(donnees_etape2['dr_nom_prenom'])
            directeurs = []
            for i in range(nombre_docteur):
                universite = Institutions.objects.get(pk=donnees_etape2['dr_universite'][i])
                directeur = Directeurs.objects.get_or_create(dr_nom_prenom = donnees_etape2['dr_nom_prenom'][i],dr_email=donnees_etape2['dr_email'][i],dr_universite=universite) 
                directeurs.append(directeur)

            # directeur_save =  Directeurs.objects.bulk_create(directeurs)

            # Enregistrer le jury
            nombre_jury = len(donnees_etape2['nom_prenom'])
            membreJurys = []
            for i in range(nombre_jury):
                universite = Institutions.objects.get(pk=donnees_etape2['universite'][i])
                jury = MembreJury.objects.get_or_create(nom_prenom = donnees_etape2['nom_prenom'][i],email=donnees_etape2['email'][i],role=donnees_etape2['role'][i],universite=universite) 
                jury.save()  # Enregistrer d'abord le membre du jury pour obtenir un ID
                membreJurys.append(jury)

            # membrejury_save =  MembreJury.objects.bulk_create(membreJurys)

            # lier directeur et les membre du jury a la these
            
            these.directeur.add(*directeurs)
            these.jury.add(*membreJurys)

            print("----> icic")
            # rediriger sur une autre page avec un message
            messages.success(request, "Thèse ajoutée avec succès !")
            return render(request, "theses_ci/contenu/succes.html")
            


        else:
            print(f"---->: {directeur_form.errors}")
            print(f"---->: {membrejury_form.errors}")
    else:
        if request.session.get('etape2'):
            context['session'] = dict(request.session.get('etape2'))
            d = dict(request.session.get('etape2'))

        if 'etape2' in request.session:
            del request.session['etape2']

        membrejury_form = MembrejuryForm(initial=request.session.get('etape2', {}))
        directeur_form = DirecteurForm(initial=request.session.get('etape2', {}))

    context.update({
        'membrejury': membrejury_form,
        'directeur':directeur_form,
        'range': range(3),
    })
    return render(request, 'theses_ci/contenu/jury.html', context)
