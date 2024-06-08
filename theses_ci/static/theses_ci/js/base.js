
// fonction qui reccupere un element puis l'ajoute une class
function get_add_class(element, classe){
    elt = document.querySelector("#"+element)
    elt.classList.add(classe)
}

// fonction pour retirer une class a un element
function retirer_class(element, classe){
    elt = document.querySelector("#"+element)
    elt.classList.remove(classe)
}



document.querySelector("#btn-person-search").addEventListener("click", function(){
    get_add_class('theses-form', 'visibilite')
    retirer_class('personne-form', 'visibilite')
})

document.querySelector("#btn-these-search").addEventListener("click", function(){
    get_add_class('personne-form', 'visibilite')
    retirer_class('theses-form', 'visibilite')
})



