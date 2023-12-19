from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://Giuseppe:1Admin!@localhost:54321/')
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
    try:
        object_id = ObjectId(id_biglietto)
        biglietto = Concerti_clt.find_one({"_id": object_id})
        if int(biglietto["Biglietti_disponibili"]) > 0:
            Concerti_clt.update_one({"_id": object_id}, {"$inc": {"Biglietti_disponibili": -1}})
            try:
                Festival = Festival_clt.find_one({'id_univoco': biglietto['id_festival']})
                biglietto = Concerti_clt.find_one({"_id": object_id})
                if int(Festival['Biglietti_disponibili']) > int(biglietto["Biglietti_disponibili"]):
                    Festival_clt.update_one({'id_univoco': biglietto['id_festival']},
                                            {"$set": {'Biglietti_disponibili': biglietto["Biglietti_disponibili"]}})
                client.close()
            except:
                return False
            return biglietto['Nome_concerto']
    except:
        return False
    # funzione che permette di acquistare un biglietto, restituisce vero se tutto va a buon fine


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
    ...


def filtra_festival(lista_generi: list, date: str, citta: str, artisti: str, prezzo: str) -> list:
    # funzione che restituisce una lista di festival in base ai filtri inseriti.
    ...


def ricerca_generale(stringa: str) -> list:
    # funzione che data una stringa in input, interroghi tutti i campi dei documenti e restituisca una lista di concerti
    ...
