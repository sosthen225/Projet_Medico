import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# Create your models here.

choix_communes = [
    ('Aboisso', 'Aboisso'),
    ('Adzopé', 'Adzopé'),
    ('Afféry', 'Afféry'),
    ('Agou', 'Agou'),
    ('Akoupé', 'Akoupé'),
    ('Abobo', 'Abobo'),
    ('Adjamé', 'Adjamé'),
    ('Attécoubé', 'Attécoubé'),
    ('Bingerville', 'Bingerville'),
    ('Cocody', 'Cocody'),
    ('Koumassi', 'Koumassi'),
    ('Marcory', 'Marcory'),
    ('Plateau', 'Plateau'),
    ('Port-Bouët', 'Port-Bouët'),
    ('Songon', 'Songon'),
    ('Treichville', 'Treichville'),
    ('Anyama', 'Anyama'),
    ('Yopougon', 'Yopougon'),
    ('Alépé', 'Alépé'),
    ('Arrah', 'Arrah'),
    ('Assinie', 'Assinie'),
    ('Attiégbé', 'Attiégbé'),
    ('Badikaha', 'Badikaha'),
    ('Bangolo', 'Bangolo'),
    ('Biankouma', 'Biankouma'),
    ('Bloléquin', 'Bloléquin'),
    ('Bodoukou', 'Bodoukou'),
    ('Bouaflé', 'Bouaflé'),
    ('Bouna', 'Bouna'),
    ('Boundiali', 'Boundiali'),
    ('Brignan', 'Brignan'),
    ('Broukro', 'Broukro'),
    ('Dabakala', 'Dabakala'),
    ('Divo', 'Divo'),
    ('Dimbokro', 'Dimbokro'),
    ('Duékoué', 'Duékoué'),
    ('Ferkéssedougou', 'Ferkéssedougou'),
    ('Gagnoa', 'Gagnoa'),
    ('Guéyo', 'Guéyo'),
    ('Guingré', 'Guingré'),
    ('Issia', 'Issia'),
    ('Jacqueville', 'Jacqueville'),
    ('Jérenou', 'Jérenou'),
    ('Kani', 'Kani'),
    ('Katié', 'Katié'),
    ('Katiola', 'Katiola'),
    ('Kong', 'Kong'),
    ('Kouassi-Kouassikro', 'Kouassi-Kouassikro'),
    ('Kouibly', 'Kouibly'),
    ('Kouto', 'Kouto'),
    ('Kpédékou', 'Kpédékou'),
    ('Kranou', 'Kranou'),
    ('Lakota', 'Lakota'),
    ('Man', 'Man'),
    ('Mankono', 'Mankono'),
    ('Méagui', 'Méagui'),
    ('Mégué', 'Mégué'),
    ('Odienné', 'Odienné'),
    ('Oumé', 'Oumé'),
    ('Péhé', 'Péhé'),
    ('Raviart', 'Raviart'),
    ('Saboudougou', 'Saboudougou'),
    ('Sassandra', 'Sassandra'),
    ('Séguéla', 'Séguéla'),
    ('Séguélon', 'Séguélon'),
    ('Sikensi', 'Sikensi'),
    ('Sipilou', 'Sipilou'),
    ('Soubré', 'Soubré'),
    ('Tabou', 'Tabou'),
    ('Taï', 'Taï'),
    ('Tafiré', 'Tafiré'),
    ('Tiassalé', 'Tiassalé'),
    ('Tiebissou', 'Tiebissou'),
    ('Tiémé', 'Tiémé'),
    ('Tingrela', 'Tingrela'),
    ('Touba', 'Touba'),
    ('Toumodi', 'Toumodi'),
    ('Vavoua', 'Vavoua'),
    ('yakassé-Attobrou', 'yakassé-Attobrou'),
    ('Yamoussoukro', 'Yamoussoukro'),
    ('Zaranou', 'Zaranou'),
    ('Zatié', 'Zatié'),
    ('Zinguinéo', 'Zinguinéo')
]
choix_communes= sorted(choix_communes, key=lambda x: x[1])

CHOIX_SPECIALITES = [
    ('cardiologue', 'Cardiologue'),
    ('dentiste', 'Dentiste'),
    ('dermatologue', 'Dermatologue'),
    ('généraliste', 'Généraliste'),
    ('gynécologue', 'Gynécologue'),
    ('neurologue', 'Neurologue'),
    ('pediatre', 'Pédiatre'),
    ('psychiatre', 'Psychiatre'),
    ('psychologue', 'Psychologue'),
    ('ophtamologue', 'Ophtamologue'),
]

CHOIX_SPECIALITES = sorted(CHOIX_SPECIALITES, key=lambda x: x[1])
genre=[('M', 'Masculin'), ('F', 'Féminin')]


# voici mes models
  

  # Modèle Medecin

class Medecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    genre = models.CharField(max_length=1, choices=genre )
    specialite = models.CharField(max_length=100, choices=CHOIX_SPECIALITES)
    telephone = models.CharField(max_length=10, unique=True)
    

    def __str__(self):
        return f"{self.nom} {self.prenom}"


     # Modèle infirmier

class Infirmier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    genre = models.CharField(max_length=1, choices=genre)
    telephone = models.CharField(max_length=10, unique=True)
    

    def __str__(self):
        return f"{self.nom} {self.prenom}"



     # Modèle Patient

class Patient(models.Model):
    code_patient = models.CharField(max_length=10, unique=True, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    genre = models.CharField(max_length=1, choices=genre)
    adresse = models.CharField(max_length=200 , choices=choix_communes)
    telephone = models.CharField(max_length=10, unique=True)
    infirmier =models.ForeignKey(Infirmier, on_delete=models.CASCADE)

    def nom_upper(self):
        return self.nom.upper()

    def prenom_lower(self):
        return self.prenom.lower()

    def __str__(self):
        return f'{self.nom} {self.prenom} ({self.code_patient})'
    
    def save(self, *args, **kwargs):
        if not self.code_patient:  # Générer le code uniquement si ce n'est pas déjà fait
            # Extraire les premières lettres du nom (jusqu'à 2 lettres pour chaque mot)
            nom_initials = ''.join(word[:2].upper() for word in self.nom.split())

            # Extraire le jour de la date de naissance
            jour_naissance = str(self.date_naissance.day).zfill(2)

            # Extraire les deux derniers chiffres de l'année de naissance
            annee_naissance = str(self.date_naissance.year)[-2:]

            # Concaténer les valeurs pour former le code patient initial
            base_code = f"{nom_initials}{jour_naissance}{annee_naissance}"

            # Vérifier l'unicité du code et générer un nouveau code si nécessaire
            code_exists = Patient.objects.filter(code_patient=base_code).exists()
            suffix = 1
            while code_exists:
                # Générer un nouveau code en ajoutant un suffixe numérique
                new_code = f"{base_code}{suffix}"
                code_exists = Patient.objects.filter(code_patient=new_code).exists()
                if not code_exists:
                    base_code = new_code
                suffix += 1

            self.code_patient = base_code

        super().save(*args, **kwargs)




  # Modèle Carnet
BLOOD_TYPE_CHOICES = [
    ('A+', 'A positif'),
    ('A-', 'A négatif'),
    ('B+', 'B positif'),
    ('B-', 'B négatif'),
    ('AB+', 'AB positif'),
    ('AB-', 'AB négatif'),
    ('O+', 'O positif'),
    ('O-', 'O négatif'),
]
class Carnet(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    masse = models.FloatField(verbose_name="masse (kg)" , validators=[MinValueValidator(+0.5)])
    tension_systolique = models.IntegerField(verbose_name="Tension systolique (mmHg)",validators=[MinValueValidator(50)])
    tension_diastolique = models.IntegerField(verbose_name="Tension diastolique (mmHg)",validators=[MinValueValidator(30)])
    temperature = models.DecimalField(max_digits=5,decimal_places=2,verbose_name="Température (°C)",validators=[MinValueValidator(32)])
    pouls = models.IntegerField(verbose_name="Pouls (bpm)", validators=[MinValueValidator(+50)] )
    antecedents_medicaux = models.TextField(blank=True, null=True)
    allergies_et_intolerance = models.TextField(blank=True, null=True)
    groupe_sanguin=models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    fumeur = models.CharField(max_length=3,choices=[('OUI','Oui'), ('NON', 'Non')])
    alcool = models.CharField(max_length=3,choices=[('OUI','Oui'), ('NON', 'Non')])
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carnet de {self.patient}'
    


    # Modèle Consultation

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin =models.ForeignKey(Medecin, on_delete=models.CASCADE)
    date_consultation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Consultation de {self.patient} par {self.medecin} le {self.date_consultation}'




  # Modèle Diagnostic

class Diagnostic(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    maladie = models.CharField(max_length=255)

    def __str__(self):
        return f'Diagnostic de {self.consultation.patient}: {self.maladie}'
    


    # Modèle Traitement
  
class Traitement(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    medicament = models.CharField(max_length=255)
    posologie = models.CharField(max_length=255)
    date_debut = models.DateField(default=datetime.date.today)
    date_fin = models.DateField()

    def __str__(self):
        return f'Traitement: {self.medicament} ({self.date_debut} - {self.date_fin})'

