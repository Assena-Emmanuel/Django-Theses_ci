// Fonction pour afficher ou masquer le contenu de la liste déroulante
function toggleDropdown(contentId, iconId) {
    var dropdownContent = document.getElementById(contentId);
    var dropdownIcon = document.getElementById(iconId);
    var searchFiltre = dropdownContent.previousElementSibling;

    if (dropdownContent.style.display === "block" && searchFiltre.style.display === "block") {
        dropdownContent.style.display = "none";
        searchFiltre.style.display = "none";
        dropdownIcon.classList.remove("fa-chevron-up");
        dropdownIcon.classList.add("fa-chevron-down");
        setTimeout(() => dropdownContent.classList.remove("show"), 10); // Pour forcer le recalcul de la mise en page
    } else {
        searchFiltre.style.display = "block";
        dropdownContent.style.display = "block";
        dropdownIcon.classList.remove("fa-chevron-down");
        dropdownIcon.classList.add("fa-chevron-up");
        setTimeout(() => dropdownContent.classList.add("show"), 10); // Pour forcer le recalcul de la mise en page
    }
}

// Fonction pour filtrer les options
function filterFunction(contentId, inputId) {
    var input, filter, div, labels, i;
    input = document.getElementById(inputId);
    filter = input.value.toUpperCase();
    div = document.getElementById(contentId);
    labels = div.getElementsByTagName("label");
    for (i = 0; i < labels.length; i++) {
        var txtValue = labels[i].textContent || labels[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            labels[i].style.display = "";
        } else {
            labels[i].style.display = "none";
        }
    }
}

// Fonction pour mettre à jour les thèses affichées en fonction des filtres sélectionnés
function updateTheses() {
    var selectedEtablissements = Array.from(document.querySelectorAll('input[name="etablissement[]"]:checked')).map(cb => cb.value);
    var selectedDomaines = Array.from(document.querySelectorAll('input[name="domaine[]"]:checked')).map(cb => cb.value);
    var selectedSpecialites = Array.from(document.querySelectorAll('input[name="specialite[]"]:checked')).map(cb => cb.value);

    var theses = document.querySelectorAll('.these');
    theses.forEach(function(these) {
        var institution = these.querySelector('.institution').innerText.trim();
        var domaine = these.querySelector('.domaine').innerText.trim();
        var specialite = these.querySelector('.specialite').innerText.trim();
        var show = true;

        if (selectedEtablissements.length > 0 && !selectedEtablissements.includes(institution)) {
            show = false;
        }

        if (selectedDomaines.length > 0 && !selectedDomaines.includes(domaine)) {
            show = false;
        }
        if (selectedSpecialites.length > 0 && !selectedSpecialites.includes(specialite)) {
            show = false;
        }

        these.style.display = show ? 'block' : 'none';
    });
}

// Ajoutez un gestionnaire d'événements pour les changements de case à cocher
document.querySelectorAll('input[name="etablissement[]"], input[name="domaine[]"]').forEach(function(checkbox) {
    checkbox.addEventListener('change', updateTheses);
});

// Affichez toutes les thèses initialement
document.addEventListener('DOMContentLoaded', function() {
    updateTheses();
});



