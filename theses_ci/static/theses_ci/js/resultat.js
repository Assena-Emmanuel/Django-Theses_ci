function toggleDropdownDate(contentId, iconId) {
    var dropdownContent = document.getElementById(contentId);
    var dropdownIcon = document.getElementById(iconId);
    var searchFiltre = dropdownContent.previousElementSibling;

    if (dropdownContent.style.display === "block") {
        dropdownContent.style.display = "none";
        if (searchFiltre && searchFiltre.tagName === 'DIV') {
            searchFiltre.style.display = "none";
        }
        dropdownIcon.classList.remove("fa-chevron-up");
        dropdownIcon.classList.add("fa-chevron-down");
        setTimeout(() => dropdownContent.classList.remove("show"), 10); // Pour forcer le recalcul de la mise en page
    } else {
        if (searchFiltre && searchFiltre.tagName === 'DIV') {
            searchFiltre.style.display = "block";
        }
        dropdownContent.style.display = "block";
        dropdownIcon.classList.remove("fa-chevron-down");
        dropdownIcon.classList.add("fa-chevron-up");
        setTimeout(() => dropdownContent.classList.add("show"), 10); // Pour forcer le recalcul de la mise en page
    }
}

function toggleDropdown(contentId, iconId) {
    var dropdownContent = document.getElementById(contentId);
    var dropdownIcon = document.getElementById(iconId);
    var searchFiltre = dropdownContent.previousElementSibling;

    if (dropdownContent.style.display === "block") {
        dropdownContent.style.display = "none";
        if (searchFiltre && searchFiltre.tagName === 'DIV') {
            searchFiltre.style.display = "none";
        }
        dropdownIcon.classList.remove("fa-chevron-up");
        dropdownIcon.classList.add("fa-chevron-down");
        setTimeout(() => dropdownContent.classList.remove("show"), 10); // Pour forcer le recalcul de la mise en page
    } else {
        if (searchFiltre && searchFiltre.tagName === 'DIV') {
            searchFiltre.style.display = "block";
        }
        dropdownContent.style.display = "block";
        dropdownIcon.classList.remove("fa-chevron-down");
        dropdownIcon.classList.add("fa-chevron-up");
        setTimeout(() => dropdownContent.classList.add("show"), 10); // Pour forcer le recalcul de la mise en page
    }
}

function filterFunction(contentId, inputId) {
    var input = document.getElementById(inputId);
    var filter = input.value.toUpperCase();
    var div = document.getElementById(contentId);
    var labels = div.getElementsByTagName("label");
    for (var i = 0; i < labels.length; i++) {
        var txtValue = labels[i].textContent || labels[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            labels[i].style.display = "";
        } else {
            labels[i].style.display = "none";
        }
    }
}

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
document.querySelectorAll('input[name="etablissement[]"], input[name="domaine[]"], input[name="specialite[]"]').forEach(function(checkbox) {
    checkbox.addEventListener('change', updateTheses);
});

// Affichez toutes les thèses initialement
document.addEventListener('DOMContentLoaded', function() {
    updateTheses();
});


// date
document.addEventListener("DOMContentLoaded", function() {
    var dropdownContent = document.getElementById("dropdownContent3");
    var dateDebutInput = document.getElementById("datedebut");
    var dateFinInput = document.getElementById("datefin");

    dateDebutInput.addEventListener("focus", function() {
        dropdownContent.style.display = "block";
    });

    dateFinInput.addEventListener("focus", function() {
        dropdownContent.style.display = "block";
    });

    // Masquer le yearList lorsque l'utilisateur clique en dehors des champs de saisie
    // window.addEventListener("click", function(event) {
    //     if (event.target !== dateDebutInput && event.target !== dateFinInput) {
    //         dropdownContent.style.display = "none";
    //     }
    // });
});
document.addEventListener("DOMContentLoaded", function() {
    var yearList = document.getElementById("yearList");
    var dropdownContent = document.getElementById("dropdownContent3");
    // Sélectionnez tous les éléments de date dans la yearList
    var dateElements = yearList.querySelectorAll(".date-element");

    // Ajoutez un gestionnaire d'événements à chaque élément de date
    dateElements.forEach(function(element) {
        element.addEventListener("click", function() {
            var selectedDate = element.textContent.trim(); // Récupérez la date sélectionnée
             // Affichez la date sélectionnée dans la console (à adapter selon vos besoins)
            dropdownContent.style.display = "none";
            // Vous pouvez maintenant utiliser la date sélectionnée comme vous le souhaitez
        });
    });
});
