import datetime
import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import  Constantes, Medicament, Symptome,genre, Carnet,Specialite, Consultation, Diagnostic, Patient, Traitement, User,Medecin, Infirmier
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from appFinal import models



class ConsultationForm(forms.Form):
    specialite = forms.ModelChoiceField(queryset=Specialite.objects.all(), label="Spécialité")
    medecin = forms.ModelChoiceField(queryset=Medecin.objects.none(), label="Médecin")

    class Media:
        js = ('js/consult.js',)  # Inclure votre fichier JS ici


class MedecinSignUpForm(UserCreationForm):
    nom = forms.CharField(max_length=100)
    prenom = forms.CharField(max_length=100)
    genre = forms.ChoiceField(choices= genre)
    specialite = forms.ModelChoiceField(queryset=Specialite.objects.all())
    telephone = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = [ 'nom', 'prenom', 'genre', 'specialite', 'telephone','username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nom']
        user.last_name = self.cleaned_data['prenom']
        if commit:
            user.save()
            medecin = Medecin.objects.create(
                user=user,
                nom=self.cleaned_data['nom'],
                prenom=self.cleaned_data['prenom'],
                genre=self.cleaned_data['genre'],
                specialite=self.cleaned_data['specialite'],
                telephone=self.cleaned_data['telephone']
            )
        return user

class InfirmierSignUpForm(UserCreationForm):
    nom = forms.CharField(max_length=100)
    prenom = forms.CharField(max_length=100)
    genre = forms.ChoiceField(choices=genre)
    telephone = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['nom', 'prenom', 'genre', 'telephone','username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nom']
        user.last_name = self.cleaned_data['prenom']
        if commit:
            user.save()
            infirmier = Infirmier.objects.create(
                user=user,
                nom=self.cleaned_data['nom'],
                prenom=self.cleaned_data['prenom'],
                genre=self.cleaned_data['genre'],
                telephone=self.cleaned_data['telephone']
            )
        return user
    



class MedecinLoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label="Nom d'utilisateur ou numéro de téléphone")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Mot de passe')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            # Check if the username is a phone number or a username
            if username.isdigit():
                # If it's a phone number, try to find the corresponding doctor
                try:
                    medecin = Medecin.objects.get(telephone=username)
                    self.user_cache = medecin.user
                except Medecin.DoesNotExist:
                    raise forms.ValidationError("")
            else:
                # If it's a username, try to find the corresponding doctor
                try:
                    medecin = Medecin.objects.get(user__username=username)
                    self.user_cache = medecin.user
                except Medecin.DoesNotExist:
                    raise forms.ValidationError("")

            if not self.user_cache.check_password(password):
                raise forms.ValidationError("")
        return cleaned_data

    def get_user(self):
        return self.user_cache

class InfirmierLoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label="Nom d'utilisateur ou numéro de téléphone")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Mot de passe')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            # Check if the username is a phone number or a username
            if username.isdigit():
                # If it's a phone number, try to find the corresponding nurse
                try:
                    infirmier = Infirmier.objects.get(telephone=username)
                    self.user_cache = infirmier.user
                except Infirmier.DoesNotExist:
                    raise forms.ValidationError("")
            else:
                # If it's a username, try to find the corresponding nurse
                try:
                    infirmier = Infirmier.objects.get(user__username=username)
                    self.user_cache = infirmier.user
                except Infirmier.DoesNotExist:
                    raise forms.ValidationError("")

            if not self.user_cache.check_password(password):
                raise forms.ValidationError("")
        return cleaned_data

    def get_user(self):
        return self.user_cache


    
    


class PatientForm(forms.ModelForm):
    current_year = datetime.datetime.now().year
    years = list(range(1924, current_year + 1))

    date_naissance = forms.DateField(widget=forms.SelectDateWidget(years=years))

    class Meta:
        model = Patient
        fields = ["nom","prenom","date_naissance","genre", 'groupe_sanguin',"adresse","telephone"]
        exclude = ['code_patient']  # Exclure le champ non éditable
        





class TemperatureField(forms.FloatField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['placeholder'] = '°C'

class PulseField(forms.IntegerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['placeholder'] = 'bpm'

class PoidsField(forms.FloatField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['placeholder'] = 'kg'

class tensionSystoliqueField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['placeholder'] = 'mmHg'
class tensionDiastoliqueField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['placeholder'] = 'mmHg'

OUI_NON_CHOICES = [
        (True, 'Oui'),
        (False, 'Non')
    ]

fumeur = forms.ChoiceField(choices=OUI_NON_CHOICES, widget=forms.Select)
alcool = forms.ChoiceField(choices=OUI_NON_CHOICES, widget=forms.Select)


class ConstantesForm(forms.ModelForm):

    '''def __init__(self, *args, **kwargs):
        super(ConstantesForm,self).__init__(*args, **kwargs)
        carnets = [c.patient.code_patient for c in Constantes.objects.all()]
        patients = Patient.objects.filter(~Q(code_patient__in=carnets))
        self.fields['patient'].queryset = patients'''

    temperature = TemperatureField(label=("Température"))
    pouls = PulseField(label=("Pouls"))
    masse= PoidsField(label=("masse"))
    tension_systolique=tensionSystoliqueField(label=("tension arterielle"))
    tension_diastolique=tensionDiastoliqueField(label=("tension arterielle"))
    
    class Meta:
        model = Constantes
        fields = ['masse','tension_systolique','tension_diastolique','temperature','pouls','antecedents_medicaux','allergies_et_intolerance','fumeur','alcool']

    widgets = {
            'masse': forms.NumberInput(attrs={'min': 0.5}),
            'temperature': forms.NumberInput(attrs={'min': 32}),
            'tension_systolique': forms.NumberInput(attrs={'min': 50}),
            'tension_diastolique': forms.NumberInput(attrs={'min': 30}),
            'pouls': forms.NumberInput(attrs={'min': 50}),
             'carnet': forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['masse'].widget.attrs.update({'min': 0.5})
        self.fields['tension_systolique'].widget.attrs.update({'min': 50})
        self.fields['tension_diastolique'].widget.attrs.update({'min': 30})
        self.fields['temperature'].widget.attrs.update({'min': 32})
        self.fields['pouls'].widget.attrs.update({'min': 50})




class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostic
        fields = ['maladie']




class TraitementForm(forms.ModelForm):
    class Meta:
        model = Traitement
        fields = ['date_debut', 'date_fin']



class MedicamentForm(forms.ModelForm):
    class Meta:
        model = Medicament
        fields = ['nom_medicament', 'dosage', 'forme']











class SymptomeForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'required':'required'}))

    class Meta:
        model = Symptome
        fields = ['description']
        
















