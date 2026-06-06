document.addEventListener("DOMContentLoaded", function() {
    console.log("JS chargé");
    const form = document.querySelector("form");
    if (!form) return;
    const champPseudo = document.querySelector("input[name='utilisateur']");
    const champMotDePasse = document.querySelector("input[name='mot_de_passe']");
    const champConfirmMotDePasse = document.querySelector("input[name='confirm_mot_de_passe']");
})

//validation
function validateChamp(champ, condition, message) {
    let erreur = champ.parentElement.querySelector(".message-erreur");

    if (!condition) {
        if (!erreur) {
            erreur = document.createElement("p");
            erreur.classList.add("message-erreur");
            champ.parentElement.appendChild(erreur);
        }

        erreur.textContent = message;
        champ.classList.add("champ-invalide");
        return false;
    } else {
        if (erreur) erreur.remove{};
        champ.classList.remove("champ-invalide");
        return true;
    }};

//temps réel
champPseudo.addEventListener("input", function() {
    validerchamp(champPseudo, 
        champPseudo.value.trim().length >= 4,
        "Le pseudo doit comporter au moins 4 caractères");
});
champMotDePasse.addEventListener("input", function() {
    validerchamp(champMotDePasse,
        champMotDePasse.value.trim().length >= 10,
        "Le mot de passe doit comporter au moins 10 caractères"
    );
});
champConfirmMotDePasse.addEventListener("input", function() {
    validerchamp(champConfirmMotDePasse,
        champConfirmMotDePasse.value === champMotDePasse.value,
        "Les mots de passe ne correspondent pas");
});

//submit
form.addEventListener("submit", function(evenement) {
    const PseudoOk = Validerchamp(
        champPseudo,
        champPseudo.value.trim().length >= 4,
        "Le pseudo doit comporter au moins 4 caractères"
    );
    const MotDePasseOk = Validerchamp(
        champMotDePasse,
        champMotDePasse.value.trim().length >= 10,
        "Le mot de passe doit comporter au moins 10 caractères"
    );
    const ConfirmMotDePasseOk = Validerchamp(
        champConfirmMotDePasse,
        champConfirmMotDePasse.value === champMotDePasse.value,
        "Les mots de passe ne correspondent pas");

    if (!PseudoOk || !MotDePasseOk || !ConfirmMotDePasseOk) {
        evenement.preventDefault();
        return;
    }

});
