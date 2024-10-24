from datetime import timezone
from datetime import date
from django.db import IntegrityError
from django.utils import timezone
from django.contrib import messages
from django.forms import formset_factory, modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from appFinal.form import  ConsultationForm,ConstantesForm,DiagnosticForm, InfirmierLoginForm, InfirmierSignUpForm, MedecinLoginForm, MedecinSignUpForm, PatientForm, TraitementForm, SymptomeForm
from appFinal.models import *



#vue de connexion
def login(request):
    form_medecin = MedecinLoginForm()
    form_infirmier = InfirmierLoginForm()

    if request.method == 'POST':
        # Choisissez le formulaire en fonction du type d'utilisateur (médecin ou infirmier)
        if 'medecin_login' in request.POST:
            form_medecin = MedecinLoginForm(request.POST)
            form = form_medecin
        elif 'infirmier_login' in request.POST:
            form_infirmier = InfirmierLoginForm(request.POST)
            form = form_infirmier
        else:
            form = None

        if form and form.is_valid():
            user = form.get_user()
            if user is not None:
                auth_login(request, user)
                if 'medecin_login' in request.POST:
                    return redirect('medecin_dashboard')
                elif 'infirmier_login' in request.POST:
                    return redirect('infirmier_dashboard')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'login.html', {
        'form_medecin': form_medecin,
        'form_infirmier': form_infirmier
    })
 



def infirmier_signup(request):
   if request.method == 'POST':
        form = InfirmierSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inscription réussie ! Vous pouvez maintenant vous connecter.')
            return redirect('login')  # Rediriger vers la page de connexion après inscription
   else:
        form = InfirmierSignUpForm()
   return render(request, 'signup.html', {'form': form})




@login_required
def accueil_infirmier(request):

 infirmier = Infirmier.objects.get(user=request.user)
 return render(request, 'infirmier_dashboard.html', {'infirmier': infirmier})


@login_required
def nouveau_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.infirmier = request.user.infirmier
            patient.save()
            Carnet.objects.create(patient=patient) #creation du carnet du patient
            messages.success(request, 'Patient enregistré avec succès.')
            return redirect('liste_patients')  
    else:
        form = PatientForm()
    return render(request, 'nouveau_patient.html', {'form': form})


@login_required
def liste_patients(request):
    
    patients = Patient.objects.all()
    patients = Patient.objects.order_by('nom')
    return render(request, 'liste_patients.html', {'patients': patients})

from datetime import datetime
def ajouter_constantes(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    carnet= Carnet.objects.get(patient=patient)
    if request.method == "POST":
        form = ConstantesForm(request.POST)
        if form.is_valid():
            constantes = form.save(commit=False)
            # date = constantes.date
            constantes.carnet = carnet
            constantes.save() 

            elements = Constantes.objects.filter(date__date=datetime.today(),carnet=Carnet.objects.get(patient=patient_id))
            constantes = elements.order_by('date').first()
            print(f"_________________constante____________________: {constantes}")
            # recupération des medecin
            
            form = ConsultationForm()
            
            return render(request,'consult_attribution.html', {'form':form,'constantes':constantes, 'patient':patient})
         
    else:
        form = ConstantesForm(initial={'carnet': carnet.id})
    return render(request, 'ajouter_constantes.html', {'form': form, 'patient': patient})


def obtenir_medecins_par_specialite(request):
    specialite_id = request.GET.get('specialite_id')
    medecins = Medecin.objects.filter(specialite_id=specialite_id).values('id', 'nom', 'prenom')
    medecins_list = list(medecins)
    return JsonResponse(medecins_list, safe=False)

def attribuer_consultation(request):
    if request.method == "POST":
        
        donnees = dict(request.POST)
        medecin = get_object_or_404(Medecin, id=donnees['medecin'][0])
        patient = get_object_or_404(Patient, id=donnees['patient'][0])
        constantes = get_object_or_404(Constantes, id=donnees['constante'][0])
     
        if medecin and patient and constantes:

            # Création automatique de la consultation avec le statut "En attente"
            Consultation.objects.create(
                        patient=patient,
                        date_consultation=timezone.now().date(),
                        statut='En attente',
                        constantes=constantes,
                        medecin= medecin  # Vous pouvez attribuer un médecin si nécessaire
                    )
            messages.success(request, 'Constantes ajoutées avec succès, la consultation est en attente.')
            return redirect('statut_consultation')
        else:
            print(f"_____________erreur")
    return render(request)

def statut_consultation(request):
    aujourdhui = datetime.now().date()
    
    # Récupérer les consultations pour aujourd'hui, triées du plus ancien au plus récent
    consultations = Consultation.objects.filter(date_consultation__date=aujourdhui).order_by('date_consultation')

    # Créer une liste pour stocker les consultations terminées ou annulées
    consultations_termines_annules = []

    # Séparer les consultations en deux groupes : non terminées/annulées et terminées/annulées
    consultations_non_termines_annules = []
    for consultation in consultations:
        if consultation.statut in ['Terminée', 'Annulée']:
            consultations_termines_annules.append(consultation)
        else:
            consultations_non_termines_annules.append(consultation)

    # Concaténer les deux listes en plaçant les terminées/annulées à la fin
    consultations = consultations_non_termines_annules + consultations_termines_annules

    context = {
        'consultations': consultations,
        'date_aujourdhui': aujourdhui
    }

    return render(request, 'statut_consultation.html', context)




def toutes_consultations(request):
    consultations = Consultation.objects.all()

    context = {
        'consultations': consultations
    }

    return render(request, 'all_consultation.html', context)



@login_required
def voir_carnet(request, patient_id):
    try:
        
        carnet = Carnet.objects.get(patient_id=patient_id)
        constantes = Constantes.objects.filter(carnet=carnet).order_by('-date')
        p = get_object_or_404(Patient, id=patient_id)
        conslt = Consultation.objects.filter(patient=patient_id)
        ids = [c.id for c in conslt]
        diagno = Diagnostic.objects.filter(consultation__in=ids)
        print(f"_________18___ __188______{[d.consultation.date_consultation for d in diagno]}")
    except Carnet.DoesNotExist:
        messages.error(request, "Ce patient n'a pas encore de carnet.")
        return redirect('liste_patients')  # Redirigez vers la liste des patients

    return render(request, 'voir_carnet.html', {'diagnos':diagno, 'p':p,'carnet': carnet, 'constantes': constantes })







@login_required
def accueil_medecin(request):
 medecin = Medecin.objects.get(user=request.user)
 return render(request, 'medecin_dashboard.html', {'medecin': medecin})


     
 

##############""""""""""""VUES MEDECINS"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""




def medecin_signup(request):
    if request.method == 'POST':
        form = MedecinSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inscription réussie ! Vous pouvez maintenant vous connecter.')
            return redirect('login')  # Rediriger vers la page de connexion après inscription
    else:
        form = MedecinSignUpForm()
    return render(request, 'signup.html', {'form': form})



def consultations_en_attente(request):
    # Récupérer la date actuelle
    today = date.today()

    # Filtrer les consultations pour aujourd'hui avec le statut "En attente"
    consultations = Consultation.objects.filter(date_consultation__date=today, statut__in=('En attente','En cours') ).order_by('date_consultation')
    
    # Nombre de consultations en attente d'aujourd'hui
    nombre_consultations_en_attente = consultations.count()

    return render(request, 'consultations_en_attente.html', {
        'consultations': consultations,
        'nombre_consultations_en_attente': nombre_consultations_en_attente
    })


def info_patient(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    print(f"___________________: {consultation}")
    patient = get_object_or_404(Patient, id=consultation.patient.id)
    # consultations = Consultation.objects.filter(patient_id=patient.id, statut='Terminée')
    carnet = get_object_or_404(Carnet, patient=patient.id)
    constantes = Constantes.objects.filter(carnet=carnet.id)
    constante_actuelle = constantes.order_by('date').first()

    context = {
        'patient':patient,
        'consultations': consultation,
        'constantes': constantes,
        'constante_actuelle': constante_actuelle,
    }
    consultation.statut = 'En cours'
    consultation.save()
    
    

    return render(request, 'patient_trouvé.html', context)



def action_consultation(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'commencer':
            consultation.statut = 'En cours'
            consultation.save()
            return redirect('patient_trouvé')
        
        elif action == 'annuler':
            consultation.statut = 'Annulée'
            consultation.save()
            return redirect('liste_consultations')

    return render(request, 'detail_consultation.html', {'consultation': consultation})


from datetime import datetime 
def nouveau_diagnostic(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    symptome = Symptome.objects.filter(consultation=consultation_id)
    print(f"consul__________1:{consultation}")
    patient = get_object_or_404(Patient, id=consultation.patient.id)
    
    # Vérifiez si l'utilisateur a un médecin associé
    try:
        medecin = request.user.medecin
        
        if(symptome):
            for symp in symptome:
                symptome = symp.description.split(',')
        print(symptome)
    except Medecin.DoesNotExist:
        messages.error(request, "Vous n'êtes pas associé à un médecin.")
        return redirect('login.html')

    alert = ""
    

    if request.method == 'POST':
        symptomeForm = SymptomeForm(request.POST)

        if symptomeForm.is_valid():
            donnee = dict(request.POST)
            symptome = Symptome.objects.create(consultation=consultation, description=donnee['description'][0])

            symptome = symptome.description.split(',')
       

            symptomeForm = SymptomeForm()

            
            return render(request, 'symptome.html', {
                'symptomeForm': symptomeForm,
                'symptome': symptome,
                'consultation': consultation,
                })
        
    else:
        symptomeForm = SymptomeForm()
        
    return render(request, 'symptome.html', {
        'patient': patient,
        'symptomeForm': symptomeForm,
        'symptome': symptome,
        'consultation': consultation,
    })

from . import organiser_donnee as f
def diagnostique(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    patient = get_object_or_404(Patient, id=consultation.patient.id)
    
    # Vérifiez si l'utilisateur a un médecin associé
    try:
        medecin = request.user.medecin
       
    except Medecin.DoesNotExist:
        messages.error(request, "Vous n'êtes pas associé à un médecin.")
        return redirect('login.html')

    alert = ""
    

    if request.method == 'POST':

        # consultation = Consultation.objects.create(patient=patient , medecin=medecin)
        resultats = dict(request.POST)
        del resultats['csrfmiddlewaretoken']
        print(resultats)
        datas = f.data_organisees(resultats)
        print(datas)
        for maladie in datas.keys():
            d = datas[maladie]
            print(maladie,'____________________', len(d))
            for i in range(0, len(datas[maladie]), 4):
                
                print(i+3)
                medicament = Medicament.objects.create(
                    nom_medicament=resultats[d[i]][0],
                    forme=resultats[d[i+1]][0],
                    dosage=resultats[d[i+2]][0],
                    posologie=resultats[d[i+3]][0],
                )
                maladie_obj = Maladie.objects.create(
                    medicament=medicament,
                    nom=maladie
                )
                

                diagnostic =Diagnostic.objects.create(consultation=consultation, maladie=maladie_obj)
                i+=3

                cons=consultation
                consultation.statut = 'Terminée'
                consultation.save()

        return redirect('recap', id=cons.id)
        return render(request, 'recap.html',{'consultation': consultation})
    
    else:
        # consultation_form = ConsultationForm(initial={'patient': patient, 'medecin': medecin})
        diagnostic_formset = DiagnosticForm()
        traitement_formset = TraitementForm()


    return render(request, 'diagno.html', {
        'patient': patient,
        'alert': alert,
        'diagnostic_formset': diagnostic_formset,
        'traitement_formset': traitement_formset,
        
    })

def recap(request, id):
    consultations = get_object_or_404(Consultation, id=id )
    diagnostique = Diagnostic.objects.filter( consultation=consultations.id)
    for d in diagnostique:
        
        print(f"________________:{d.maladie.medicament}")
    
    
    return render(request, 'recap.html', {
        'diagnostiques':diagnostique,
        'consultation':consultations,
            })



def details_consultation(request, consultation_id):
    print(f"_____________________{consultation_id}")
    consultation = get_object_or_404(Consultation, id=consultation_id)
    
    diagnostics = Diagnostic.objects.filter(consultation=consultation)
    
    
    return render(request, 'recap.html', {
        'patient': consultation.patient,
        'alert': alert,
        'date_consultation': consultation.date_consultation,
        'diagnostics': diagnostics,
        
            })







    

@login_required
def consultation_list(request):
      # Récupérer l'utilisateur connecté
    utilisateur = request.user

    # Vérifier si l'utilisateur est authentifié et s'il est un médecin
    if not utilisateur.is_authenticated or not hasattr(utilisateur, 'medecin'):
        return render(request, 'login.html')  # Redirection vers une page non autorisée

    # Récupérer l'objet médecin
    medecin = utilisateur.medecin

    # Filtrer les consultations en fonction du médecin
    consultations = Consultation.objects.filter(medecin=medecin)

    # Obtenir les patients associés
    patients = []
    for consultation in consultations:
        patient = consultation.patient
        if patient not in patients:
            patients.append(patient)

    # Rendre le template avec la liste des patients et les informations du médecin
    contexte = {
        'patients': patients,
        'medecin': medecin,
    }
    return render(request, 'consultation_list.html', contexte)







def rechercher_patient(request):
    code_patient = request.GET.get('code_patient')

    if not code_patient:
        messages.error(request, "Veuillez saisir un code patient pour effectuer la recherche.")
        return render(request, 'entrez_code.html')

    try:
        patient = Patient.objects.get(code_patient=code_patient)
    except Patient.DoesNotExist:
        messages.error(request, "Aucun patient trouvé avec le code fourni.")
        return render(request, 'entrez_code.html')

    return render(request, 'recherche.html', {'patient': patient})
  

# def rech(request):
#     Patient
#     consultation = consultation.objects.all()
#     return render (request, consultation)

    


def logout_view(request):
    request.session.flush()
    return redirect('login')