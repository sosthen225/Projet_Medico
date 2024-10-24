// static/js/consultation.js

document.addEventListener('DOMContentLoaded', function () {
    const specialiteSelect = document.getElementById('id_specialite');
    const medecinSelect = document.getElementById('id_medecin');

    specialiteSelect.addEventListener('change', function () {
        const specialiteId = this.value;

        // Efface les options actuelles du champ medecin
        medecinSelect.innerHTML = '';

        if (specialiteId) {
            fetch(`/obtenir-medecins-par-specialite/?specialite_id=${specialiteId}`)
                .then(response => response.json())
                .then(data => {
                    // Ajoute une option vide
                    const emptyOption = document.createElement('option');
                    emptyOption.value = '';
                    emptyOption.textContent = 'Sélectionner un médecin';
                    medecinSelect.appendChild(emptyOption);

                    // Ajoute les nouvelles options
                    data.forEach(medecin => {
                        const option = document.createElement('option');
                        option.value = medecin.id;
                        option.textContent = `${medecin.nom} ${medecin.prenom}`;
                        medecinSelect.appendChild(option);
                    });
                    // Afficher le bouton pour soumission du formulaire
                    let btn = document.querySelector("#btnAttribuer")
                    btn.removeAttribute('hidden')
                })
                .catch(error => {
                    console.error('Error fetching medecins:', error);
                });
        }
    });
});
