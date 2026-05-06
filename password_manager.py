"""
 Enrick Password 
"""

import random
import re
import string


#  CONSTANTES

MINUSCULES  = string.ascii_lowercase          # a-z
MAJUSCULES  = string.ascii_uppercase          # A-Z
CHIFFRES    = string.digits                   # 0-9
SYMBOLES    = "!@#$%^&*()-_=+[]{}|;:,.<>?"   # caractères spéciaux

MOTS_PASSE_COURANTS = {
    "123456", "password", "azerty", "qwerty", "111111",
    "123456789", "iloveyou", "admin", "letmein", "welcome",
    "monkey", "dragon", "master", "abc123", "passw0rd",
}


#  ANALYSE DE ROBUSTESSE

def analyser_mot_de_passe(mdp: str) -> dict:
    """
    Analyse un mot de passe et retourne un rapport complet.

    Retourne un dict avec :
      - score       : int (0-100)
      - niveau      : str ('Très faible' → 'Excellent')
      - criteres    : dict des critères vérifiés
      - suggestions : list de conseils d'amélioration
    """
    criteres = {
        "longueur_ok":       len(mdp) >= 8,
        "longueur_forte":    len(mdp) >= 12,
        "longueur_excellente": len(mdp) >= 16,
        "a_minuscule":       bool(re.search(r"[a-z]", mdp)),
        "a_majuscule":       bool(re.search(r"[A-Z]", mdp)),
        "a_chiffre":         bool(re.search(r"\d", mdp)),
        "a_symbole":         bool(re.search(r"[!@#$%^&*()\-_=+\[\]{}|;:,.<>?]", mdp)),
        "pas_repetitions":   not bool(re.search(r"(.)\1{2,}", mdp)),
        "pas_sequences":     not _contient_sequence(mdp),
        "pas_commun":        mdp.lower() not in MOTS_PASSE_COURANTS,
    }

    # Calcul du score pondéré
    score = 0
    if criteres["longueur_ok"]:        score += 10
    if criteres["longueur_forte"]:     score += 15
    if criteres["longueur_excellente"]: score += 10
    if criteres["a_minuscule"]:        score += 10
    if criteres["a_majuscule"]:        score += 15
    if criteres["a_chiffre"]:          score += 15
    if criteres["a_symbole"]:          score += 20
    if criteres["pas_repetitions"]:    score +=  5
    if criteres["pas_sequences"]:      score +=  5
    if criteres["pas_commun"]:         score += 10  # malus si commun : -10 implicite

    # Pénalités
    if not criteres["pas_commun"]:
        score = min(score, 10)   # mot de passe commun → bloqué à 10
    if len(mdp) < 6:
        score = min(score, 20)

    score = max(0, min(score, 100))

    # Niveau qualitatif
    if score <= 20:
        niveau = "Très faible 🔴"
    elif score <= 40:
        niveau = "Faible 🟠"
    elif score <= 60:
        niveau = "Moyen 🟡"
    elif score <= 80:
        niveau = "Fort 🟢"
    else:
        niveau = "Excellent 🔵"

    # Suggestions
    suggestions = _generer_suggestions(criteres, mdp)

    return {
        "score":       score,
        "niveau":      niveau,
        "criteres":    criteres,
        "suggestions": suggestions,
    }


def _contient_sequence(mdp: str) -> bool:
    """Détecte les séquences évidentes (abc, 123, qwerty…)."""
    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "qwertyuiop",
        "azerty",
    ]
    mdp_lower = mdp.lower()
    for seq in sequences:
        for i in range(len(seq) - 2):
            if seq[i:i+3] in mdp_lower:
                return True
    return False


def _generer_suggestions(criteres: dict, mdp: str) -> list:
    """Génère des conseils personnalisés selon les critères manquants."""
    conseils = []
    if not criteres["longueur_ok"]:
        conseils.append("Utilisez au moins 8 caractères.")
    elif not criteres["longueur_forte"]:
        conseils.append("Visez 12 caractères ou plus pour un mot de passe fort.")
    if not criteres["a_minuscule"]:
        conseils.append("Ajoutez des lettres minuscules (a-z).")
    if not criteres["a_majuscule"]:
        conseils.append("Ajoutez des lettres majuscules (A-Z).")
    if not criteres["a_chiffre"]:
        conseils.append("Intégrez des chiffres (0-9).")
    if not criteres["a_symbole"]:
        conseils.append("Utilisez des symboles (!@#$%…) pour renforcer le mot de passe.")
    if not criteres["pas_repetitions"]:
        conseils.append("Évitez les répétitions de caractères (ex: aaa, 111).")
    if not criteres["pas_sequences"]:
        conseils.append("Évitez les séquences évidentes (abc, 123, azerty…).")
    if not criteres["pas_commun"]:
        conseils.append("Ce mot de passe est trop courant ! Choisissez quelque chose d'unique.")
    if not conseils:
        conseils.append("Excellent mot de passe ! Pensez à le stocker dans un gestionnaire sécurisé.")
    return conseils


#  GÉNÉRATION DE MOTS DE PASSE

def generer_mot_de_passe(
    longueur: int = 16,
    avec_majuscules: bool = True,
    avec_chiffres: bool = True,
    avec_symboles: bool = True,
) -> str:
    """
    Génère un mot de passe aléatoire et sécurisé.

    Args:
        longueur        : Nombre de caractères (min 4).
        avec_majuscules : Inclure des majuscules.
        avec_chiffres   : Inclure des chiffres.
        avec_symboles   : Inclure des symboles.

    Returns:
        Le mot de passe généré (str).
    """
    if longueur < 4:
        raise ValueError("La longueur minimale est de 4 caractères.")

    pool = MINUSCULES
    obligatoires = [random.choice(MINUSCULES)]

    if avec_majuscules:
        pool += MAJUSCULES
        obligatoires.append(random.choice(MAJUSCULES))
    if avec_chiffres:
        pool += CHIFFRES
        obligatoires.append(random.choice(CHIFFRES))
    if avec_symboles:
        pool += SYMBOLES
        obligatoires.append(random.choice(SYMBOLES))

    # Compléter jusqu'à la longueur souhaitée
    reste = [random.choice(pool) for _ in range(longueur - len(obligatoires))]
    tous = obligatoires + reste

    # Mélanger pour éviter un pattern prévisible
    random.shuffle(tous)
    return "".join(tous)


def generer_phrase_secrete(nb_mots: int = 4) -> str:
    """
    Génère une phrase secrète mémorisable (diceware simplifié).
    Exemple : 'Tigre-Soleil-Forêt-42!'

    Args:
        nb_mots : Nombre de mots (recommandé : 4-6).

    Returns:
        La phrase secrète (str).
    """
    mots = [
        "Tigre", "Soleil", "Forêt", "Nuage", "Rivière", "Montagne",
        "Étoile", "Océan", "Faucon", "Flamme", "Cristal", "Orage",
        "Cactus", "Lune", "Dragon", "Renard", "Saison", "Brume",
        "Comète", "Sphinx", "Vortex", "Zénith", "Glacier", "Ambre",
    ]
    selection = random.choices(mots, k=nb_mots)
    chiffre   = str(random.randint(10, 99))
    symbole   = random.choice("!@#$%")
    return "-".join(selection) + chiffre + symbole

#  AFFICHAGE

def afficher_rapport(mdp: str, rapport: dict) -> None:
    """Affiche un rapport de sécurité complet dans le terminal."""
    largeur = 52
    print("\n" + "═" * largeur)
    print(" RAPPORT DE SÉCURITÉ".center(largeur))
    print("═" * largeur)
    print(f"  Mot de passe : {mdp}")
    print(f"  Longueur     : {len(mdp)} caractères")
    print(f"  Score        : {rapport['score']}/100")
    print(f"  Niveau       : {rapport['niveau']}")
    print("─" * largeur)

    # Barre de progression
    barre = _barre_progression(rapport["score"])
    print(f"  {barre}")
    print("─" * largeur)

    # Critères
    print("  Critères :")
    labels = {
        "longueur_ok":          "≥ 8 caractères",
        "longueur_forte":       "≥ 12 caractères",
        "longueur_excellente":  "≥ 16 caractères",
        "a_minuscule":          "Minuscules (a-z)",
        "a_majuscule":          "Majuscules (A-Z)",
        "a_chiffre":            "Chiffres (0-9)",
        "a_symbole":            "Symboles (!@#…)",
        "pas_repetitions":      "Pas de répétitions",
        "pas_sequences":        "Pas de séquences",
        "pas_commun":           "Mot de passe unique",
    }
    for cle, label in labels.items():
        icone = "✅" if rapport["criteres"][cle] else "❌"
        print(f"    {icone}  {label}")

    print("─" * largeur)
    print("  Conseils :")
    for conseil in rapport["suggestions"]:
        print(f"     {conseil}")
    print("═" * largeur + "\n")


def _barre_progression(score: int, largeur: int = 40) -> str:
    """Génère une barre de progression  colorée."""
    rempli = int(score / 100 * largeur)
    vide   = largeur - rempli
    if score <= 20:
        couleur = "🔴"
    elif score <= 40:
        couleur = "🟠"
    elif score <= 60:
        couleur = "🟡"
    elif score <= 80:
        couleur = "🟢"
    else:
        couleur = "🔵"
    return f"{couleur} [{'█' * rempli}{'░' * vide}] {score}%"


#  INTERFACE EN LIGNE DE COMMANDE

def menu_generer():
    """Sous-menu : génération de mot de passe."""
    print("\n── Générateur ──────────────────────────")
    print("  1. Mot de passe aléatoire")
    print("  2. Phrase secrète mémorisable")
    choix = input("Votre choix : ").strip()

    if choix == "1":
        try:
            longueur = int(input("Longueur souhaitée [16] : ").strip() or "16")
        except ValueError:
            longueur = 16
        maj  = input("Inclure des majuscules ? (o/n) [o] : ").strip().lower() != "n"
        chif = input("Inclure des chiffres ?   (o/n) [o] : ").strip().lower() != "n"
        symb = input("Inclure des symboles ?   (o/n) [o] : ").strip().lower() != "n"
        mdp  = generer_mot_de_passe(longueur, maj, chif, symb)

    elif choix == "2":
        try:
            nb = int(input("Nombre de mots [4] : ").strip() or "4")
        except ValueError:
            nb = 4
        mdp = generer_phrase_secrete(nb)

    else:
        print("Choix invalide.")
        return

    rapport = analyser_mot_de_passe(mdp)
    afficher_rapport(mdp, rapport)


def menu_verifier():
    """Sous-menu : vérification d'un mot de passe existant."""
    print("\n── Vérificateur ────────────────────────")
    mdp = input("Entrez votre mot de passe : ")
    if not mdp:
        print("Mot de passe vide.")
        return
    rapport = analyser_mot_de_passe(mdp)
    afficher_rapport(mdp, rapport)


def main():
    """Point d'entrée principal."""
    print("\n" + "═" * 52)
    print(" GESTIONNAIRE DE MOTS DE PASSE".center(52))
    print("═" * 52)

    while True:
        print("\n  1. Générer un mot de passe")
        print("  2. Vérifier un mot de passe")
        print("  3. Quitter")
        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            menu_generer()
        elif choix == "2":
            menu_verifier()
        elif choix == "3":
            print("\nÀ bientôt ! Gardez vos mots de passe en sécurité \n")
            break
        else:
            print("Option invalide. Choisissez 1, 2 ou 3.")


if __name__ == "__main__":
    main()
