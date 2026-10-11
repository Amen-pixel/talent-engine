"""Remplit la base avec des candidats de démonstration : python seed.py"""
import store

DEMO = [
    dict(name="Awa Diallo", email="awa@example.com", level="Licence 3 GL", skills="Python, Flask, SQL, Git, API",
         github="https://github.com/awa", availability="full",
         projects="Application de gestion de stock pour une pharmacie, avec API REST, base SQL et tests automatisés. " * 2,
         motivation="Je veux apprendre en équipe et contribuer à des projets concrets qui ont un impact. " * 2),
    dict(name="Koffi Mensah", email="koffi@example.com", level="Licence 2", skills="HTML, CSS, JavaScript",
         github="https://github.com/koffi", availability="partial",
         projects="Site vitrine pour un restaurant local, responsive.",
         motivation="Je souhaite progresser et rejoindre une équipe de développeurs."),
    dict(name="Jean Test", email="jean@example.com", skills="Word, Excel", availability="none",
         motivation="Je cherche un stage pour mon CV, merci."),
    dict(name="Fatou Sow", email="fatou@example.com", level="Master 1", skills="Python, Django, Docker, SQL, React, Git",
         github="https://gitlab.com/fatou", availability="full",
         projects="Plateforme de mentorat étudiante : authentification, messagerie temps réel, déploiement Docker. " * 3,
         motivation="Contribuer à un projet utile, apprendre les méthodes d'une équipe pro et évoluer. " * 3),
]

if __name__ == "__main__":
    for d in DEMO:
        print(d["name"], "->", store.save(d) or "OK")
    print("Doublon ->", store.save(DEMO[0]))
    print("Invalide ->", store.save({"name": "", "email": "pas-un-email"}))
