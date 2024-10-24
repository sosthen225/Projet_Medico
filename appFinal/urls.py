from django.urls import path
from appFinal.views import  recap ,attribuer_consultation, obtenir_medecins_par_specialite, accueil_infirmier, info_patient,diagnostique, accueil_medecin, ajouter_constantes,  consultation_list, consultations_en_attente, details_consultation, infirmier_signup, liste_patients, login, logout_view, medecin_signup, nouveau_diagnostic, nouveau_patient, rechercher_patient, statut_consultation, toutes_consultations, voir_carnet


urlpatterns=[
    path('',login, name="login"),
    path('signup/infirmier/', infirmier_signup, name='infirmier_signup'),
    path('signup/medecin/', medecin_signup, name='medecin_signup'),

    path('accueil/medecin',accueil_medecin,name= 'medecin_dashboard'),
    path('accueil/infirmier',accueil_infirmier,name= 'infirmier_dashboard'),
     
     # lien pour infirmier
    path('nouveau_patient/', nouveau_patient, name='nouveau_patient'),
    path('liste_patients/', liste_patients, name='liste_patients'),
    path('ajouter_constantes/<int:patient_id>/', ajouter_constantes, name='ajouter_constantes'),
    

    #path('nouveau_carnet/', nouveau_carnet, name='nouveau_carnet'),
    path('statut_consultation/', statut_consultation, name='statut_consultation'),
    path('toutes_consultations/', toutes_consultations, name='toutes_consultations'),
    
    path('voir_carnet/<int:patient_id>/', voir_carnet, name='voir_carnet'),


    path('consultations_en_attente/',consultations_en_attente, name='consultations en attente'),
    #path('modifier_carnet/<int:patient_id>/', modifier_carnet, name='modifier_carnet'),
    path('rechercher_patient/', rechercher_patient, name='rechercher_patient'),
    #path('ajouter_diagnostic_traitement/',ajouter_diagnostic_traitement, name='ajouter_diagnostic_traitement'),
    #path('consulter/',register_consultation ,name='faire consultation'),
    path('consultation/<int:consultation_id>/',details_consultation, name='recap'),
    path('listeconsultation/',consultation_list, name='liste_consultation'),
    path('logout/',logout_view, name='logout'),
    path('medecin/patient/<int:consultation_id>/',nouveau_diagnostic, name='nouveau_diagnostic'),
   # path('patient/<int:patient_id>/', add_consultation, name='add_consultation'),
   # path('consultation/<int:consultation_id>/', add_diagnostic, name='add_diagnostic'),
    path('diagnostic/<int:consultation_id>/',diagnostique, name='diagnostique'),
    path('consultation/patient/<int:consultation_id>/',info_patient, name='info_patient'),
    path('obtenir-medecins-par-specialite/', obtenir_medecins_par_specialite, name='obtenir_medecins_par_specialite'),
    path('attribuer-medecins-par-specialite/', attribuer_consultation, name='attribuer_consultation'),
    path('recapitulatif/patient/<int:id>', recap, name='recap'),
]       
    

