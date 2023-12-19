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
    generi = []
    lista_generi = qf.trova_generi()
    for elem in lista_generi:
        item = request.args.get(f'genere_{elem}')
        if item != None:
            generi.append(item)
    inizio = request.args.get('start-date')
    fine = request.args.get('start-date')
    date = ''
    if inizio or fine:
        date = [inizio, fine]
    citta = request.args.get('city')
    artisti = request.args.get('artist')
    try:
        prezzo = int(request.args.get('max-price'))
    except:
        prezzo = ''
    tipo = int(request.args.get('event-type'))
    if tipo == 1:
        results = qf.ottieni_concerti(generi, date, citta, artisti, prezzo)
        return render_template("principale.html", concerti=results, genres=lista_generi)
    elif tipo == 2:
        qf.ottieni_festival(lista_generi, date, citta, artisti, prezzo)
        return render_template("principale_festival.html")


@app.route("/acquista_biglietti")
def acquisto_biglietto():
    id = request.args.get('id')
    nome = request.args.get('nome')
    festival = (request.args.get(('festival')))
    out = ''
    if festival == 'Si':
        out = qf.ottieni_biglietto_festival(id=id, nome=nome)
    else:
        out = qf.ottieni_biglietto(id=id)
    return render_template('acquista.html', concerti=out)


@app.route("/acquisto_fatto")
def acquisto_fatto():
    id = request.args.get('id')
    nome = request.args.get('nome')
    festival = (request.args.get(('festival')))
    if festival == 'Si':
        qf.togli_biglietto_festival(id=id, nome=nome)
    else:
        qf.togli_biglietto(id=id)
    nome = 'concerto ' + nome
    return render_template('acquisto_avvenuto.html', nome=nome)


if __name__ == '__main__':
    app.run()
