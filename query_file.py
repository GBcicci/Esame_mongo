from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime

# client = MongoClient('mongodb://Giuseppe:1Admin!@localhost:54321/')
client = MongoClient('mongodb://localhost:59846/')
db = client.Esami
Concerti_clt = db.Concerti
Festival_clt = db.Festival


def trova_generi() -> list:
    # funzione che restituisce una lista di generi dei concerti
    return sorted(Concerti_clt.distinct("Generi"))


def visualizza_festival(hash_festival: str) -> dict and list:
    # funzione che dato l'id di un festival (campo del biglietto) restituisce il festival e i concerti appartenenti a esso
    # return festival, concerti
    out = []
    for _ in range(3):
        festival = list(Festival_clt.find({"id_univoco": hash_festival}))
        concerti = list(Concerti_clt.find({"id_festival": hash_festival}))
        out.append([festival, concerti])
    return out


def ottieni_sample_concerti() -> list:
    # funzione che restituisce 10 concerti casuali
    # con disponibilità biglietti maggiore di 0 e data posteriore a quella odierna
    oggi = str(datetime.now().date())
    concerti_casuali = Concerti_clt.aggregate([
        {"$match": {"Biglietti_disponibili": {"$gt": 0}, "Data": {"$gte": oggi}}},
        {"$sample": {"size": 10}}
    ])
    concerti_lista = (list(concerti_casuali))
    return concerti_lista


def acquista_concerto(id_biglietto: str) -> str or bool:
    # funzione che permette di acquistare un biglietto, restituisce vero se tutto va a buon fine
    object_id = ObjectId(id_biglietto)
    biglietto = Concerti_clt.find_one({"_id": object_id})
    quantita = int(biglietto["Biglietti_disponibili"])
    if quantita > 0:
        try:
            Festival = Festival_clt.find_one({'id_univoco': biglietto['id_festival']})
            concerti_in_festival = Concerti_clt.find({'id_festival': biglietto['id_festival']})
            for elem in concerti_in_festival['Biglietti_disponibili']:
                elem = int(elem)
                if elem > 0:
                    if quantita < elem:
                        quantita = elem
            if int(Festival['Biglietti_disponibili']) > quantita:
                Festival_clt.update_one({'id_univoco': biglietto['id_festival']},
                                        {"$set": {'Biglietti_disponibili': biglietto["Biglietti_disponibili"]}})
        except:
            pass
        Concerti_clt.update_one({"_id": object_id}, {"$inc": {"Biglietti_disponibili": -1}})
        client.close()
        return biglietto['Nome_concerto']
    else:
        return False


def acquista_festival(id_festival: str) -> bool:
    # funzione che permette di acquistare un festival, restituisce vero se tutto va a buon fine
    biglietto = Festival_clt.find_one({"id_univoco": id_festival})
    if int(biglietto["Biglietti_disponibili"]) > 0:
        Festival_clt.update_one({"id_univoco": id_festival}, {"$inc": {"Biglietti_disponibili": -1}})
        Concerti_clt.update_many({"id_festival": id_festival}, {"$inc": {"Biglietti_disponibili": -1}})
        client.close()
        return biglietto['Nome_festival']


def filtra_concerti(lista_generi: list, date: str, citta: str, artisti: str, prezzo: str) -> list:
    # funzione che restituisce una lista di concerti in base ai filtri inseriti.
    query = {}

    if lista_generi:
        query["Generi"] = {"$in": lista_generi}

    if date:
        try:
            query["Data"] = {"$gte": datetime.strptime(date, "%d/%m/%Y")}
        except ValueError:
            print("Formato data non valido. Inserisci la data nel formato corretto (DD/MM/YYYY).")
            return []

    if citta:
        query["Citta"] = citta

    if artisti:
        artisti_list = [artista.strip() for artista in artisti]
        query["$or"] = [
            {"Nome_artista": {"$in": artisti_list}},
            {"Pseudonimi_artista": {"$in": artisti_list}}
        ]

    if prezzo is not None:
        query["Prezzo_min"] = {"$lte": prezzo}

    # Esecuzione della query
    risultati = list(Concerti_clt.find(query))

    return risultati


# Richiedi i filtri in input
lista_generi = input("Inserisci i generi (separati da virgola): ").split(',')
date = input("Inserisci la data di inizio (formato YYYY-MM-DD): ")
citta = input("Inserisci la città: ")
artisti = input("Inserisci gli artisti (separati da virgola): ")
prezzo = input("Inserisci il prezzo massimo: ")

# Chiamata alla funzione con i filtri inseriti dall'utente
risultati = filtra_concerti(lista_generi, date, citta, artisti, prezzo)

# Stampa i risultati ottenuti dalla funzione
for risultato in risultati:
    print(risultato['Nome_artista'])
    print(risultato)


def filtra_festival(lista_generi: list, date: str, citta: str, artisti: str, prezzo: str) -> list:
    # funzione che restituisce una lista di festival in base ai filtri inseriti.
    query = {}
    if lista_generi:
        query["Generi"] = {"$in": lista_generi}

    if date:
        query["Data"] = {"$gte": date}

    if citta:
        query["Citta"] = citta

    if artisti:
        query["$or"] = [
            {"Artisti": {"$in": [artista.strip() for artista in artisti.split(",")]}},
            {"Pseudonimi_artista": {"$in": [artista.strip() for artista in artisti.split(",")]}}
        ]

    if prezzo:
        query["Prezzo_min"] = {"$lte": float(prezzo)}

    risultati = list(Festival_clt.find(query))
    for risultato in risultati:
        print(risultato)
        print(risultato['Generi'])
    return risultati


def ricerca_generale(stringa: str) -> list:
    # funzione che data una stringa in input, interroghi tutti i campi dei documenti e restituisca una lista di concerti
    risultati_concerti = Concerti_clt.find({
        "$or": [
            {"$text": {"$search": stringa}},
            {"Nome_concerto": {"$regex": stringa, "$options": "i"}},
            {"Nome_artista": {"$regex": stringa, "$options": "i"}},
            {"Pseudonimi_artista": {"$regex": stringa, "$options": "i"}},
            {"Generi": {"$regex": stringa, "$options": "i"}},
            {"Citta": {"$regex": stringa, "$options": "i"}}]})

    risultati_concerti_lista = list(risultati_concerti)
    print(risultati_concerti_lista)
    return risultati_concerti_lista
