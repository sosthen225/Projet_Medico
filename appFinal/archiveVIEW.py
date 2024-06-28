patient = get_object_or_404(Patient, id=patient_id)
    
    # Vérifiez si l'utilisateur a un médecin associé
    try:
        medecin = request.user.medecin
    except Medecin.DoesNotExist:
        messages.error(request, "Vous n'êtes pas associé à un médecin.")
        return redirect('login.html')

    DiagnosticFormSet = formset_factory(DiagnosticForm, extra=1)
    TraitementFormSet = formset_factory(TraitementForm, extra=1)

    if request.method == 'POST':
        consultation_form = ConsultationForm(request.POST, initial={'patient': patient, 'medecin': medecin})
        diagnostic_formset = DiagnosticFormSet(request.POST, prefix='diagnostic')
        traitement_formset = TraitementFormSet(request.POST, prefix='traitement')

        if consultation_form.is_valid() and diagnostic_formset.is_valid() and traitement_formset.is_valid():
            today = timezone.now().date()
            consultation = Consultation.objects.filter(
                patient=patient,
                medecin=medecin,
                date_consultation__date=today
            ).first()
    
            if not consultation:
                consultation = consultation_form.save(commit=False)
                consultation.patient = patient
                consultation.medecin = medecin
                consultation.save()
            
            for diagnostic_form in diagnostic_formset:
                if diagnostic_form.is_valid() and diagnostic_form.cleaned_data.get('maladie'):
                    diagnostic = diagnostic_form.save(commit=False)
                    diagnostic.consultation = consultation
                    diagnostic.save()

                    # Récupérer le traitement correspondant à ce diagnostic
                    index = diagnostic_form.prefix[-1]  # Récupérer l'index du formulaire diagnostic
                    traitement_form = traitement_formset[int(index)]
                    if traitement_form.is_valid() and traitement_form.cleaned_data.get('medicament'):
                        traitement = traitement_form.save(commit=False)
                        traitement.diagnostic = diagnostic
                        traitement.save()



            
             


            return redirect('recap.html', consultation_id=consultation.id)

    else:
        consultation_form = ConsultationForm(initial={'patient': patient, 'medecin': medecin})
        diagnostic_formset = DiagnosticFormSet(prefix='diagnostic')
        traitement_formset = TraitementFormSet(prefix='traitement')

    return render(request, 'diagno.html', {
        'patient': patient,
        'consultation_form': consultation_form,
        'diagnostic_formset': diagnostic_formset,
        'traitement_formset': traitement_formset
    })