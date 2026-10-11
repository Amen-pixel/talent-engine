# Talent Engine — mini-challenge SKULLVI

Petite application web qui **reçoit des candidatures, les valide, leur attribue un score sur 100 et les classe** pour repérer les profils à examiner en priorité.

## Lancer (2 minutes)
```bash
pip install -r requirements.txt
python seed.py          # (optionnel) 4 candidats de démo
python app.py           # formulaire : http://127.0.0.1:5000  |  classement : /ranking
python -m pytest        # 12 tests
```
Option : `ADMIN_KEY=secret python app.py` protège le classement (`/ranking?key=secret`).

## Comment ça marche
```
Formulaire → validation → score → SQLite → page de classement
 (app.py)   (scoring.py) (scoring.py) (store.py)   (ranking.html)
```
Un fichier = un rôle : `scoring.py` (la logique, sans dépendance), `store.py` (la base), `app.py` (les pages).

## Données collectées
Nom*, email*, niveau d'études, compétences*, lien GitHub/portfolio, un projet réalisé, motivation*, disponibilité au 2 novembre. (* obligatoire)
Le score et son détail sont enregistrés avec chaque candidat → **le classement est explicable**.

## Logique de score (/100)
| Critère | Points | Règle |
|---|---|---|
| Compétences | 35 | 5 compétences recherchées (Python, SQL, Git, React…) = note max |
| Preuves | 25 | lien valide (12) + description du projet : ≥200 car. 13, ≥80 car. 8, ≥20 car. 3 |
| Motivation | 15 | longueur (8) + mots-clés « apprendre, contribuer, projet, équipe » (7) |
| Disponibilité | 15 | temps plein 15, partiel 8, faible 0 |
| Complétude | 10 | niveau, lien, projet remplis |

**Statuts** : ≥ 70 → **priorité** · 40-69 → **à étudier** · < 40 → **faible**. À égalité, le plus ancien passe devant.

## Choix assumés
- **Règles simples plutôt que du ML** : pas de données historiques pour entraîner un modèle, et un score doit pouvoir être justifié à un candidat. Les poids sont en haut de `scoring.py`, faciles à ajuster.
- **Le score aide à trier, il ne décide pas** : un humain examine toujours les profils.
- **Pas de note sur la qualité de l'écriture** de la motivation (trop subjectif, injuste pour qui écrit moins bien en français).

## Erreurs anticipées
Email invalide · champs obligatoires vides · motivation trop courte · lien sans `https://` · **doublon d'email** (insensible aux majuscules) · compétences mal écrites (`JavaScript` ne compte pas comme `java`) · accès au classement protégeable par clé.

## Tests (12)
Validation (cas valides / invalides), score (candidat parfait = 100, vide < 10, jamais > 100), seuils des statuts, enregistrement + ordre du classement, doublons, candidature invalide jamais enregistrée.

## Limites et suite
- Mots-clés et compétences : un candidat peut « bourrer » son texte → prochaine étape : relecture humaine des profils prioritaires et vérification des liens (appel HTTP).
- Pas de compte admin complet, pas d'export CSV, pas d'envoi d'email de confirmation.
- Les compétences recherchées sont fixes ; à rendre configurables par programme.

## Usage de l'IA
> *À compléter honnêtement avant dépôt.*
- J'ai utilisé Claude pour : (ex. générer une première version du code, relire, proposer des tests).
- Ma contribution personnelle : (ex. les critères et pondérations, les cas limites, les tests que j'ai ajoutés, ce que j'ai modifié/refusé).
- Ce que je sais expliquer sans l'IA : le flux complet, le calcul du score, pourquoi ces choix.
