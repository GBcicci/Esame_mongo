from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://Giuseppe:1Admin!@localhost:54321/')
# client = MongoClient('mongodb://localhost:59846/')
db = client.Esami
Concerti_clt = db.Concerti
Festival_clt = db.Festival


def trova_generi() -> list:
    # funzione che restituisce una lista di generi dei concerti
    return sorted(Concerti_clt.distinct("Generi"))


def visualizza_festival(hash_festival: str or list) -> dict and list:
    # funzione che dato l'id di un festival (campo del biglietto) restituisce il festival e i concerti appartenenti a esso
    out = []
    if type(hash_festival) == str:
        festival = list(Festival_clt.find({"id_univoco": hash_festival}))
        concerti = list(Concerti_clt.find({"id_festival": hash_festival}))
        out.append([festival, concerti])
        return out
    else:
        for elem in hash_festival:
            festival = list(Festival_clt.find({"id_univoco": elem}))
            concerti = list(Concerti_clt.find({"id_festival": elem}))
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


def acquista_concerto(id_biglietto: str, num: int) -> str or bool:
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
        Concerti_clt.update_one({"_id": object_id}, {"$inc": {"Biglietti_disponibili": -num}})
        biglietto = Concerti_clt.find_one({"_id": object_id})
        client.close()
        return biglietto['Nome_concerto'], biglietto['Biglietti_disponibili']
    else:
        return False


def acquista_festival(id_festival: str, num: int):
    # funzione che permette di acquistare un festival, restituisce vero se tutto va a buon fine
    biglietto = Festival_clt.find_one({"id_univoco": id_festival})
    if int(biglietto["Biglietti_disponibili"]) > 0:
        Festival_clt.update_one({"id_univoco": id_festival}, {"$inc": {"Biglietti_disponibili": -num}})
        Concerti_clt.update_many({"id_festival": id_festival}, {"$inc": {"Biglietti_disponibili": -num}})
        biglietto = Festival_clt.find_one({"id_univoco": id_festival})
        client.close()
        return biglietto['Nome_festival'], biglietto['Biglietti_disponibili']


def filtra_concerti(lista_generi: list, date: str, citta: str, artista: str, prezzo: str) -> list:
    query = {}
    conditions = []
    oggi = str(datetime.now().date())
    conditions.append({"Biglietti_disponibili": {"$gt": 0}, "Data": {"$gte": oggi}})
    if lista_generi:
        conditions.append({"Generi": {"$in": lista_generi}})
    if date:
        conditions.append({"Data": {"$gte": date}})
    if citta:
        conditions.append({"Citta": {"$regex": citta, "$options": 'i'}})
    if artista:
        conditions.append({
            "$or": [
                {"Nome_artista": {"$regex": artista, "$options": 'i'}},
                {"Pseudonimi_artista": {"$regex": artista, "$options": 'i'}}
            ]
        })
    if prezzo:
        conditions.append({"Prezzo_min": {"$lte": float(prezzo)}})

    if conditions:
        query["$and"] = conditions
    risultati = list(Concerti_clt.find(query))
    return risultati


def filtra_festival(lista_generi: list, date: str, citta: str, artista: str, prezzo: str) -> list:
    # funzione che restituisce una lista di festival in base ai filtri inseriti.
    query = {}
    conditions = []
    oggi = str(datetime.now().date())
    conditions.append({"Biglietti_disponibili": {"$gt": 0}, "Data_fine": {"$gte": oggi}})
    if lista_generi:
        conditions.append({"Generi": {"$in": lista_generi}})
    if date:
        conditions.append({"Data": {"$gte": date}})
    if citta:
        conditions.append({"Citta": {"$regex": citta, "$options": 'i'}})
    if artista:
        conditions.append({
            "$or": [
                {"Nome_artista": {"$regex": artista, "$options": 'i'}},
                {"Pseudonimi_artista": {"$regex": artista, "$options": 'i'}}
            ]
        })
    if prezzo:
        conditions.append({"Prezzo_min": {"$lte": float(prezzo)}})

    if conditions:
        query["$and"] = conditions
    risultati = list(Festival_clt.find(query))
    out = []
    for elem in risultati:
        out.append(elem["id_univoco"])
    return out


def ricerca_generale(stringa: str) -> list:
    # funzione che data una stringa in input, interroghi tutti i campi dei documenti e restituisca una lista di concerti
    query = {
        '$or': [
            {'Nome_concerto': {'$regex': stringa, '$options': 'i'}},
            {'Nome_artista': {'$regex': stringa, '$options': 'i'}},
            {'Pseudonimi_artista': {'$regex': stringa, '$options': 'i'}},
            {'Generi': {'$regex': stringa, '$options': 'i'}},
            {'Citta': {'$regex': stringa, '$options': 'i'}}
        ]
    }
    risultati_concerti = Concerti_clt.find(query)
    risultati_concerti_lista = list(risultati_concerti)
    return risultati_concerti_lista


def ricerca_geografica_concerti(latitudine: float, longitudine: float, raggio: float):
    # funzione che date le coordinate e raggio restituisce i concerti in quell'area
    query = {"geometry.coordinates": {
        "$near": {
            "$geometry": {
                "type": "Point", "coordinates": [latitudine, longitudine]
            },
            "$maxDistance": raggio * 1000
        }
    }
    }
    risultati = Concerti_clt.find(query)
    return list(risultati)


def ricerca_geografica_festival(latitudine: float, longitudine: float, raggio: float):
    # funzione che date le coordinate e raggio restituisce i concerti in quell'area
    query = {"geometry.coordinates": {
        "$near": {
            "$geometry": {
                "type": "Point", "coordinates": [latitudine, longitudine]
            },
            "$maxDistance": raggio * 1000
        }
    }
    }
    risultati = Festival_clt.find(query)
    out = []
    for elem in risultati:
        out.append(elem["id_univoco"])
    return out
