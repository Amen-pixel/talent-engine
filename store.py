"""Stockage SQLite : enregistrer une candidature, lire le classement."""
import json
import sqlite3
from scoring import validate, score, tier, extra_skills

DB = "talent.db"
FIELDS = ("name", "email", "level", "skills", "github", "projects", "motivation", "availability")


def connect(path=DB):
    c = sqlite3.connect(path)
    c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS candidates(
        id INTEGER PRIMARY KEY, name, email UNIQUE, level, skills, github, projects,
        motivation, availability, score INTEGER, breakdown TEXT,
        created TEXT DEFAULT CURRENT_TIMESTAMP)""")
    return c


def save(form, path=DB):
    """Valide, score et enregistre. Retourne la liste des erreurs."""
    d = {k: (form.get(k) or "").strip() for k in FIELDS}
    d["email"] = d["email"].lower()          # évite les doublons A@x.com / a@x.com
    errors = validate(d)
    if errors:
        return errors
    total, detail = score(d)
    try:
        with connect(path) as c:
            c.execute(f"INSERT INTO candidates({','.join(FIELDS)},score,breakdown) "
                      f"VALUES({','.join('?' * len(FIELDS))},?,?)",
                      [d[k] for k in FIELDS] + [total, json.dumps(detail)])
    except sqlite3.IntegrityError:
        return ["Cet email a déjà candidaté."]
    return []


def _row(r):
    return dict(r, tier=tier(r["score"]), detail=json.loads(r["breakdown"]),
                extras=extra_skills(r["skills"]))


def ranking(path=DB):
    """Candidats triés : meilleur score d'abord, à égalité le plus ancien d'abord."""
    with connect(path) as c:
        rows = c.execute("SELECT * FROM candidates ORDER BY score DESC, id ASC").fetchall()
    return [_row(r) for r in rows]


def get(cid, path=DB):
    """Une candidature complète, ou None si elle n'existe pas."""
    with connect(path) as c:
        r = c.execute("SELECT * FROM candidates WHERE id = ?", (cid,)).fetchone()
    return _row(r) if r else None
