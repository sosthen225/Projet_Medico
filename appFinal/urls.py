from django.urls import path
from appFinal.views import accueil_infirmier, accueil_medecin,  consultation_list, details_consultation, infirmier_signup, liste_patients, login, logout_view, medecin_signup, modifier_carnet, nouveau_carnet, nouveau_diagnostic, nouveau_patient, rechercher_patient, voir_carnet


urlpatterns=[
    path('',login, name="login"),
    path('signup/infirmier/', infirmier_signup, name='infirmier_signup'),
    path('signup/medecin/', medecin_signup, name='medecin_signup'),
    path('accueil/medecin',accueil_medecin,name= 'medecin_dashboard'),
    path('accueil/infirmier',accueil_infirmier,name= 'infirmier_dashboard'),
    path('nouveau_patient/', nouveau_patient, name='nouveau_patient'),
    path('nouveau_carnet/', nouveau_carnet, name='nouveau_carnet'),
    path('liste_patients/', liste_patients, name='liste_patients'),
    path('voir_carnet/<int:patient_id>/', voir_carnet, name='voir_carnet'),
    path('modifier_carnet/<int:patient_id>/', modifier_carnet, name='modifier_carnet'),
    path('rechercher_patient/', rechercher_patient, name='rechercher_patient'),
    #path('ajouter_diagnostic_traitement/',ajouter_diagnostic_traitement, name='ajouter_diagnostic_traitement'),
    #path('consulter/',register_consultation ,name='faire consultation'),
    path('consultation/<int:consultation_id>/',details_consultation, name='recap'),
    path('listeconsultation/',consultation_list, name='liste_consultation'),
    path('logout/',logout_view, name='logout'),
     path('medecin/patient/<int:patient_id>/',nouveau_diagnostic, name='nouveau_diagnostic'),
   # path('patient/<int:patient_id>/', add_consultation, name='add_consultation'),
   # path('consultation/<int:consultation_id>/', add_diagnostic, name='add_diagnostic'),
    #path('diagnostic/<int:diagnostic_id>/',add_traitement, name='add_traitement'),
]       
    

