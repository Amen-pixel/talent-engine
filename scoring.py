"""Logique métier : validation + score. Aucune dépendance (facile à tester)."""
import re

# Compétences recherchées (modifiable en 1 ligne)
WANTED = {"python", "javascript", "sql", "git", "html", "css", "react",
          "flask", "django", "api", "docker", "node", "java"}
# Variantes courantes -> compétence de référence
ALIASES = {"js": "javascript", "nodejs": "node", "reactjs": "react", "ts": "typescript",
           "postgresql": "sql", "postgres": "sql", "mysql": "sql", "sqlite": "sql"}
MOTIV_WORDS = ("apprend", "contribu", "projet", "équip", "equip")
URL = re.compile(r"^https?://\S+\.\S+$")
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
AVAILABILITY = {"full": 15, "partial": 8, "none": 0}


def tokens(text):
    """'Python3, Node.js, MySQL' -> {'python', 'node', 'sql'} (synonymes inclus)"""
    text = re.sub(r"\.js\b", "js", (text or "").lower())      # node.js -> nodejs
    return {ALIASES.get(t, t) for t in re.findall(r"[a-zà-ÿ]+", text)}


def extra_skills(raw):
    """Compétences hors liste : pas de points, mais montrées au recruteur."""
    items = [s.strip() for s in re.split(r"[,;\n]", raw or "") if s.strip()]
    return [s for s in items if not tokens(s) & WANTED]


def validate(d):
    """Retourne la liste des erreurs (vide = candidature valide)."""
    errors = []
    if not d.get("name"):
        errors.append("Le nom est obligatoire.")
    if not EMAIL.match(d.get("email", "")):
        errors.append("Email invalide.")
    if not tokens(d.get("skills")):
        errors.append("Indiquez au moins une compétence.")
    if len(d.get("motivation", "")) < 20:
        errors.append("Motivation trop courte (20 caractères minimum).")
    if d.get("github") and not URL.match(d["github"]):
        errors.append("Le lien doit commencer par https://")
    if d.get("availability", "none") not in AVAILABILITY:
        errors.append("Disponibilité invalide.")
    return errors


def score(d):
    """Retourne (total /100, détail par critère)."""
    # 1. Compétences : 5 compétences recherchées = note max (35)
    matched = tokens(d.get("skills")) & WANTED
    skills = round(35 * min(len(matched) / 5, 1))

    # 2. Preuves : lien valide (12) + description du projet (13)
    n = len(d.get("projects", ""))
    projects = (12 if URL.match(d.get("github", "")) else 0) \
        + (13 if n >= 200 else 8 if n >= 80 else 3 if n >= 20 else 0)

    # 3. Motivation : longueur (8) + mots clés (7)
    m = d.get("motivation", "").lower()
    hits = sum(w in m for w in MOTIV_WORDS)
    motivation = (8 if len(m) >= 150 else 4 if len(m) >= 60 else 0) + min(7, hits * 4)

    # 4. Disponibilité : 15 / 8 / 0
    availability = AVAILABILITY.get(d.get("availability"), 0)

    # 5. Complétude : champs facultatifs remplis (niveau, lien, projets)
    filled = sum(bool(d.get(k)) for k in ("level", "github", "projects"))
    completeness = round(10 * filled / 3)

    detail = {"competences": skills, "preuves": projects, "motivation": motivation,
              "disponibilite": availability, "completude": completeness}
    return sum(detail.values()), detail


def tier(total):
    return "priority" if total >= 70 else "review" if total >= 40 else "low"
