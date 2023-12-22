from flask import Flask, render_template, request
import query_file as qf

app = Flask(__name__)
generi = qf.trova_generi()


@app.route("/")
def principale():
    results = qf.ottieni_sample_concerti()
    return render_template("principale.html", concerti=results, genres=generi)


@app.route("/filtri")
def concerti_filtrati():
    generi_lista = []
    for elem in generi:
        item = request.args.get(f'genere_{elem}')
        if item != None:
            generi_lista.append(item)
    data = request.args.get('date')
    citta = request.args.get('city')
    artista = request.args.get('artist')
    prezzo = request.args.get('max-price')
    tipo = request.args.get('tipo_evento')
    if int(tipo) == 1:
        risultati = qf.filtra_concerti(lista_generi=generi_lista, date=data, citta=citta, artista=artista,
                                       prezzo=prezzo)
        return render_template("principale.html", concerti=risultati, genres=generi)
    elif int(tipo) == 2:
        festivals_hash = qf.filtra_festival(
            lista_generi=generi_lista,
            date=data,
            citta=citta,
            artista=artista,
            prezzo=prezzo
        )
        festivals = qf.visualizza_festival(festivals_hash)
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


@app.route("/filtri_geo")
def filtri_geo():
    longitudine = float(request.args.get('longitudine'))
    latitudine = float(request.args.get('latitudine'))
    raggio = float(request.args.get('raggio'))
    tipo_evento = int(request.args.get('tipo_evento'))
    if tipo_evento == 1:
        out = qf.ricerca_geografica_concerti(latitudine=latitudine, longitudine=longitudine, raggio=raggio)
        return render_template("principale.html", concerti=out, genres=generi)
    else:
        festivals_hash = qf.ricerca_geografica_festival(latitudine=latitudine, longitudine=longitudine, raggio=raggio)
        festivals = qf.visualizza_festival(festivals_hash)
        return render_template('principale_festival.html', festivals=festivals, genres=generi)



if __name__ == '__main__':
    app.run()
