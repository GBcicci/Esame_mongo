from flask import Flask, render_template, request
import query_file as qf

app = Flask(__name__)


@app.route("/")
def principale():
    results = qf.ottieni_sample_concerti()
    generi = qf.trova_generi()
    return render_template("principale.html", concerti=results, genres=generi)


@app.route("/filtri")
def concerti_filtrati():
    ...


@app.route("/acquista_biglietti")
def acquisto_biglietto():
    id = request.args.get('id')
    out = qf.acquista_concerto(id_biglietto=id)
    if out:
        return render_template('acquisto_avvenuto.html', nome=out)
    return render_template('errore.html', nome=out)


if __name__ == '__main__':
    app.run()
