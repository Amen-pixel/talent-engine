import os
from flask import Flask, render_template, request, redirect, url_for, abort
import store

app = Flask(__name__)
ADMIN_KEY = os.environ.get("ADMIN_KEY")  # si défini, protège /ranking?key=...


@app.route("/", methods=["GET", "POST"])
def apply():
    errors = []
    if request.method == "POST":
        errors = store.save(request.form)
        if not errors:
            return redirect(url_for("thanks"))
    return render_template("form.html", errors=errors, f=request.form)


@app.route("/merci")
def thanks():
    return render_template("thanks.html")


@app.route("/ranking")
def ranking():
    if ADMIN_KEY and request.args.get("key") != ADMIN_KEY:
        abort(403)
    return render_template("ranking.html", rows=store.ranking())


@app.route("/candidat/<int:cid>")
def candidate(cid):
    if ADMIN_KEY and request.args.get("key") != ADMIN_KEY:
        abort(403)
    c = store.get(cid)
    if c is None:
        abort(404)
    return render_template("candidate.html", c=c)


if __name__ == "__main__":
    app.run(debug=True)
