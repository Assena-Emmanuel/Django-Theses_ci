from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import ThesesForm , DirecteurForm, MembrejuryForm 
from .models import Domaines, Specialites, Institutions, Theses, Directeurs, MembreJury
from django.core.paginator import Paginator
from django.db.models import Count
from .utils import handle_uploaded_file
import os
from django.conf import settings

    
  

def index(request):
    context = {}
    nb_these = Theses.objects.count()
    nb_auteur = len(set(Theses.objects.values_list('auteur_email', flat=True)))
    nb_directeur = len(set(Directeurs.objects.values_list('dr_email', flat=True)))
    nb_membrejury = len(set(MembreJury.objects.values_list('email', flat=True)))
    
    context["personne_liees_aux_theses"] = nb_auteur + nb_directeur + nb_membrejury
    context["nb_these"] = nb_these
    # Récupérer tous les mots clés de la table These
    terme_recherche =[]
    mots_cles = Theses.objects.values_list('mot_cle', flat=True)
    domaines = list(set(list(Domaines.objects.values_list('libelle', flat=True))))
    specialites = list(set(list(Specialites.objects.values_list('libelle', flat=True))))
    
    # decouper tous les mots clés par la virgule
    tous_mots_cles = []
    for mc in mots_cles:
        if mc:
            tous_mots_cles.extend(mc.split(','))
    mots_cles = list(set([mot.strip() for mot in tous_mots_cles]))
    terme_recherche.extend(domaines)
    terme_recherche.extend(specialites)
    terme_recherche.extend(mots_cles)
    # Enlever les éventuels espaces et nettoyer les mots clés
    context["mots_cles"] = terme_recherche

    # Récupérer le nombre de thèses par année
    theses_par_annee = Theses.objects.values('date_soutenance').annotate(count=Count('id')).order_by('date_soutenance')
    context['theses_par_annee'] = theses_par_annee
    

    return render(request, "theses_ci/contenu/index.html", context)


def recherche_avancee(request):
    print('____________________________________')
    return render(request, 'theses_ci/contenu/recherche_avancee.html')

def recherche_simple(request):
    return render(request, 'theses_ci/contenu/recherche_simple.html')

def resultat(request):
    context = {}
    etablissement = Institutions.objects.all()
    domaines = Domaines.objects.all()
    specialites = Specialites.objects.all()

    # Extraire les dates de soutenance
    dates = list(Theses.objects.values_list('date_soutenance', flat=True))
    
    if (len(dates) != 0):
        # Extraire les années des dates
        annees = list(set([date.year for date in dates if date is not None]))

        context["dates"] = range(min(annees), max(annees) + 1, 3)
        context["date_min"] = min(annees)
        context["date_max"] = max(annees)
        context["specialites"] = specialites
        context["domaines"] = domaines
        context["etablissements"] = etablissement

    # Récupérer tous les mots clés de la table Theses
    terme_recherche = []
    mots_cles = Theses.objects.values_list('mot_cle', flat=True)
    domaines = list(set(list(Domaines.objects.values_list('libelle', flat=True))))
    specialites = list(set(list(Specialites.objects.values_list('libelle', flat=True))))

    if(len(mots_cles)!= 0):
        # Découper tous les mots clés par la virgule
        tous_mots_cles = []
        for mc in mots_cles:
            if mc:
                tous_mots_cles.extend(mc.split(','))
        mots_cles = list(set([mot.strip() for mot in tous_mots_cles]))
        terme_recherche.extend(domaines)
        terme_recherche.extend(specialites)
        terme_recherche.extend(mots_cles)

        # Enlever les éventuels espaces et nettoyer les mots clés
        context["mots_cles"] = terme_recherche

    list_theses = []
    if request.method == 'GET':
        if request.GET.get('all') == "*":
            context["terme"] = request.GET.get('all')
            theses = Theses.objects.all()
            list_theses.extend(theses)
    
            # Pagination
            paginator = Paginator(list_theses, 10)  # 10 thèses par page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['nb'] = theses.count() 
            context['page_obj'] = page_obj
    
            return render(request, "theses_ci/contenu/resultat.html", context)
        else:
            return redirect('index')
    
    if request.method == "POST":
        terme = request.POST["mot_cle"]
        context["terme"] = terme
        theses = Theses.objects.select_related('domaine', 'specialite', 'institution').prefetch_related('directeur').filter(mot_cle__icontains=terme)

        # Effectuer la recherche sur les mots clés, les domaines et les spécialités
        domaine_theses = list(Theses.objects.select_related('domaine', 'specialite', 'institution').prefetch_related('directeur').filter(domaine__libelle__contains=terme))
        specialite_theses = list(Theses.objects.select_related('domaine', 'specialite', 'institution').prefetch_related('directeur').filter(specialite__libelle__contains=terme))
    
        # Regrouper tous les résultats en un seul résultat
        list_theses.extend(domaine_theses)
        list_theses.extend(specialite_theses)
        list_theses.extend(theses)

        # Pagination
        paginator = Paginator(list_theses, 10)  # 10 thèses par page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['nb'] = len(list_theses)
        context['page_obj'] = page_obj

    

    return render(request, "theses_ci/contenu/resultat.html", context)







def detail(request, these_id):

    theses = get_object_or_404(Theses.objects.select_related('domaine', 'specialite', 'institution').prefetch_related('directeur', 'jury'), id=these_id)
    directeurs = theses.directeur.all()
    jurys = theses.jury.all()
    mots_cles = theses.mot_cle.split(',')
    if theses.fichier:
        fichier = '/'.join(theses.fichier.url.split('/')[-2:])
    else:
       fichier = None 


    return render(request, 'theses_ci/contenu/detail.html',{'theses':theses, 'directeurs':directeurs, 'jurys':jurys, 'mots_cles':mots_cles, 'fichier':fichier})



def succes(request):
    return render(request, 'theses_ci/contenu/succes.html')

# retourne la valeur non nulle dans une liste de deux valeurs
def non_null(listes):
    new = []
    for liste in listes:
        if liste != '' and liste not in new:
            new.append(liste)
    return new[0]

def these_etape1(request):
    d = Domaines.objects.all()
    specialite = Specialites.objects.all()
    univ =Institutions.objects.all()

    if request.method == 'POST':

            

        these_form = ThesesForm(request.POST, request.FILES)
        

        if these_form.is_valid():
             # Sauvegarde du fichier et récupération du chemin
            uploaded_file = request.FILES['fichier']
            file_path = handle_uploaded_file(uploaded_file)

            # Sauvegarde du chemin dans la session
            request.session['file_path'] = file_path
            request.session['etape1'] = request.POST


            sess = dict(request.session.get('etape1'))
            request.session['etape1_saisie'] = {
                'domaine': non_null(sess['domaine']),
                'specialite': non_null(sess['specialite']),
                'universite': non_null(sess['universite']),
            }

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
  
    these_form = ThesesForm(initial=request.session.get('etape1_saisie', {}))
    d = Domaines.objects.all()
    specialite = Specialites.objects.all()
    univ =Institutions.objects.all()

    session_valeur = dict(request.session.get('etape1_saisie'))
    

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
        infos = dict(request.POST)
        
        directeur_noms = infos['dr_nom_prenom']
        directeur_emails = infos['dr_email']
        directeur_universite = infos['dr_universite[]']

        jury_nom_prenom = infos['nom_prenom']
        jury_email = infos['email']
        jury_universite = infos['universite[]']
        jury_roles = infos['role']
        
        if  len(jury_universite)!= 0 and len(directeur_universite) != 0:
            
            session = dict(request.session.get('etape1'))
            session_file = request.session.get('file_path')
            session_valeur = dict(request.session.get('etape1_saisie'))

            # verification de l'existance  
            domaine, _ = Domaines.objects.get_or_create(libelle=session_valeur['domaine'])
            specialite, _ = Specialites.objects.get_or_create(libelle=session_valeur['specialite'])
            universite, _ = Institutions.objects.get_or_create(nom=session_valeur['universite'])

    

            # Enregistrer la these
            these, _ = Theses.objects.get_or_create(
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
                    'fichier': session_file
                }
            )


  
            # Enregistrer le(s) directeur(s) de these
            nombre_docteur = len(directeur_universite)
            directeurs = []
            for i in range(nombre_docteur):
                universite = Institutions.objects.get(pk=directeur_universite[i])
                directeur, _ = Directeurs.objects.get_or_create(dr_nom_prenom = directeur_noms[i],dr_email=directeur_emails[i],dr_universite=universite) 
                directeurs.append(directeur)


            # Enregistrer le jury
            nombre_jury = len(jury_universite)
            membreJurys = []
            for i in range(nombre_jury):
                universite = Institutions.objects.get(pk=jury_universite[i])
                jury, _ = MembreJury.objects.get_or_create(nom_prenom = jury_nom_prenom[i],email=jury_email[i],role=jury_roles[i],universite=universite) 
                membreJurys.append(jury)

            # lier directeur et les membre du jury a la these

            these.directeur.add(*directeurs)
            these.jury.add(*membreJurys)

            # Suppression des variables de session
            if 'etape1' in request.session:
                del request.session['etape1']

            if 'etape2' in request.session:
                del request.session['etape2']

            if 'file_path' in request.session:
                del request.session['file_path']
     
            # rediriger sur une autre page avec un message
            return render(request, "theses_ci/contenu/succes.html", {"message":"Thèse ajoutée avec succès !"})
            


        else:
            print(f"Quelque chose c'est male passée")
    else:
        membrejury_form = MembrejuryForm()
        directeur_form = DirecteurForm()

    context.update({
        'membrejury': membrejury_form,
        'directeur':directeur_form,
        'range': range(3),
    })
    return render(request, 'theses_ci/contenu/jury.html', context)



def telecharger(request):
    file_path = os.path.join(settings.MEDIA_ROOT, request.GET.get("path", ""))
    file_path = "/".join("media".join(file_path.split("media")[1:]).split("/"))[1:]
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return HttpResponse(404)