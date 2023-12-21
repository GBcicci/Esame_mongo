from flask import Flask, render_template, request
import query_file as qf
from query_file import filtra_concerti

app = Flask(__name__)
generi = qf.trova_generi()


@app.route("/")
def principale():
    results = qf.ottieni_sample_concerti()
    return render_template("principale.html", concerti=results, genres=generi)


@app.route("/filtri")
def concerti_filtrati():
    lista_generi = request.args.getlist('genere')
    data = request.args.get('data')
    citta = request.args.get('citta')
    artisti = request.args.get('artisti')
    prezzo = request.args.get('prezzo')
    tipo = request.args.get('tipo_evento')
    if int(tipo) == 1:
        risultati = qf.filtra_concerti(
            lista_generi=lista_generi,
            date=data,
            citta=citta,
            artisti=artisti,
            prezzo=prezzo
        )
        return render_template("principale.html", concerti=risultati, genres=generi)
    elif int(tipo) == 2:
        festivals = qf.filtra_festival(
            lista_generi=lista_generi,
            date=data,
            citta=citta,
            artisti=artisti,
            prezzo=prezzo
        )
        return render_template('principale_festival.html', festivals=festivals, genres=generi)


@app.route("/ricerca_generale")
def ricerca_generale():
    stringa = request.args.get('stringa')
    out = qf.ricerca_generale(stringa)
    return render_template("principale.html", concerti=out, genres=generi)


@app.route("/acquista_biglietti")
def acquisto_biglietto():
    id = request.args.get('id')
    out = qf.acquista_concerto(id_biglietto=id)
    if out:
        return render_template('acquisto_avvenuto.html', nome=out)
    return render_template('errore.html', nome=out)


@app.route("/visualizza_festival")
def visualizza_festival():
    id = request.args.get('id_festival')
    festivals = qf.visualizza_festival(id)
    return render_template('principale_festival.html', festivals=festivals, genres=generi)


@app.route("/acquista_festival")
def acquista_festival():
    id = request.args.get('id')
    out = qf.acquista_festival(id_festival=id)
    if out:
        return render_template('acquisto_avvenuto.html', nome=out)
    return render_template('errore.html', nome=out)


if __name__ == '__main__':
    app.run()
