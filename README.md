# 🔐 Générateur & Vérificateur de Mots de Passe

Un outil en ligne de commande pour **générer** des mots de passe sécurisés et **analyser** leur robustesse — écrit en Python pur, sans dépendances externes.

---

## Fonctionnalités

| Fonctionnalité | Détail |
|---|---|
| 🎲 Génération aléatoire | Longueur et composition personnalisables |
| 🧩 Phrase secrète | Style diceware, mémorisable et solide |
| 📊 Score de sécurité | 0 → 100 pts avec barre de progression |
| 🔍 Analyse des critères | 10 critères détaillés (longueur, diversité, séquences…) |
| 💡 Conseils personnalisés | Suggestions concrètes pour améliorer le mot de passe |
| 🚫 Détection des mots communs | Blacklist des mots de passe les plus courants |

---

## Démo

```
═══════════════════════════════════════════════════════
🔐  RAPPORT DE SÉCURITÉ
═══════════════════════════════════════════════════════
  Mot de passe : X9#kLm!vQz@2Bnp7
  Longueur     : 17 caractères
  Score        : 100/100
  Niveau       : Excellent 🔵
───────────────────────────────────────────────────────
  🔵 [████████████████████████████████████████] 100%
───────────────────────────────────────────────────────
  Critères :
    ✅  ≥ 8 caractères
    ✅  ≥ 12 caractères
    ✅  ≥ 16 caractères
    ✅  Minuscules (a-z)
    ✅  Majuscules (A-Z)
    ✅  Chiffres (0-9)
    ✅  Symboles (!@#…)
    ✅  Pas de répétitions
    ✅  Pas de séquences
    ✅  Mot de passe unique
───────────────────────────────────────────────────────
  Conseils :
    💡 Excellent mot de passe ! Pensez à le stocker dans un gestionnaire sécurisé.
═══════════════════════════════════════════════════════
```

---

## Prérequis

- Python **3.8** ou supérieur
- Aucune dépendance externe (stdlib uniquement : `random`, `re`, `string`)

---

## Installation & Lancement

```bash
git clone https://github.com/TON_USERNAME/password-manager.git
cd password-manager
python password_manager.py
```

---

## Lancer les tests

```bash
pip install pytest
python -m pytest tests.py -v
```

---

## Structure du projet

```
password-manager/
├── password_manager.py   # Module principal
├── tests.py              # 25+ tests unitaires (pytest)
└── README.md             # Ce fichier
```

---

## Architecture du code

```
password_manager.py
│
├── CONSTANTES
│   ├── MINUSCULES / MAJUSCULES / CHIFFRES / SYMBOLES
│   └── MOTS_PASSE_COURANTS  (blacklist)
│
├── ANALYSE
│   ├── analyser_mot_de_passe()   → rapport complet (score, niveau, critères, conseils)
│   ├── _contient_sequence()      → détecte abc, 123, qwerty…
│   └── _generer_suggestions()    → conseils personnalisés
│
├── GÉNÉRATION
│   ├── generer_mot_de_passe()    → aléatoire, composition configurable
│   └── generer_phrase_secrete()  → style diceware mémorisable
│
└── INTERFACE CLI
    ├── menu_generer()
    ├── menu_verifier()
    └── main()
```

---

## Score de sécurité — Barème

| Critère | Points |
|---|---|
| ≥ 8 caractères | +10 |
| ≥ 12 caractères | +15 |
| ≥ 16 caractères | +10 |
| Minuscules | +10 |
| Majuscules | +15 |
| Chiffres | +15 |
| Symboles | +20 |
| Pas de répétitions | +5 |
| Pas de séquences | +5 |
| Mot de passe unique | +10 (ou bloqué à 10 si commun) |

---

## Licence

Ce projet est sous licence **MIT**.
