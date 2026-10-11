import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import store
from scoring import validate, score, tier, tokens

GOOD = dict(name="A", email="a@b.com", level="L3", skills="Python, SQL, Git, Flask, API",
            github="https://github.com/a", availability="full",
            projects="x" * 200, motivation="Apprendre et contribuer à un projet en équipe. " * 4)


def test_valid_candidate_has_no_errors():
    assert validate(GOOD) == []

def test_invalid_email_and_empty_fields():
    errs = validate(dict(GOOD, email="nope", name="", skills=""))
    assert len(errs) == 3

def test_short_motivation_rejected():
    assert validate(dict(GOOD, motivation="ok"))

def test_bad_link_rejected():
    assert validate(dict(GOOD, github="github.com/a"))

def test_tokens_no_false_positive_java_vs_javascript():
    assert "java" not in tokens("JavaScript")

def test_perfect_candidate_scores_100():
    total, _ = score(GOOD)
    assert total == 100

def test_empty_candidate_scores_low():
    total, _ = score(dict(name="A", email="a@b.com", skills="Word", motivation="x" * 20, availability="none"))
    assert total < 10

def test_score_never_exceeds_100():
    total, _ = score(dict(GOOD, skills="python sql git flask api docker react node css html java"))
    assert total <= 100

def test_tiers():
    assert (tier(70), tier(69), tier(40), tier(39)) == ("priority", "review", "review", "low")

# --- stockage ---
def test_save_and_rank(tmp_path):
    db = str(tmp_path / "t.db")
    weak = dict(name="W", email="w@b.com", skills="Word", motivation="x" * 20, availability="none")
    assert store.save(weak, db) == [] and store.save(GOOD, db) == []
    rows = store.ranking(db)
    assert [r["name"] for r in rows] == ["A", "W"] and rows[0]["tier"] == "priority"

def test_duplicate_email_rejected_case_insensitive(tmp_path):
    db = str(tmp_path / "t.db")
    store.save(GOOD, db)
    assert store.save(dict(GOOD, email="A@B.COM"), db) == ["Cet email a déjà candidaté."]

def test_invalid_not_saved(tmp_path):
    db = str(tmp_path / "t.db")
    assert store.save(dict(GOOD, email="bad"), db)
    assert store.ranking(db) == []


# --- synonymes et compétences hors liste ---
from scoring import extra_skills

def test_aliases_are_recognised():
    assert tokens("JS, PostgreSQL") >= {"javascript", "sql"}

def test_nodejs_counts_once():
    assert tokens("Node.js") == {"node"}

def test_extra_skills_listed_not_scored():
    assert extra_skills("Python, Rust, Figma, MySQL") == ["Rust", "Figma"]
    base = dict(GOOD, skills="Python")
    assert score(dict(base, skills="Python, Rust"))[0] == score(base)[0]


def test_get_one_candidate(tmp_path):
    db = str(tmp_path / "t.db")
    store.save(GOOD, db)
    c = store.get(1, db)
    assert c["name"] == "A" and c["detail"]["competences"] == 35
    assert store.get(99, db) is None
