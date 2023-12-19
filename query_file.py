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


def ottinei_festival_da_concerti(hash_festival: str) -> dict and list:
    # funzione che dato l'id di un festival (campo del biglietto) restituisce il festival e i concerti appartenenti a esso
    # return festival, concerti
    ...

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
            return biglietto['Nome_concerto']
    except:
        return False
    # funzione che permette di acquistare un biglietto, restituisce vero se tutto va a buon fine


def acquista_festival(id_festival: str) -> bool:
    # funzione che permette di acquistare un festival, restituisce vero se tutto va a buon fine
    ...


def filtra_concerti(lista_generi: list, date: str, citta: str, artisti: str, prezzo: str) -> list:
    # funzione che restituisce una lista di concerti in base ai filtri inseriti.
    ...


def filtra_festival(lista_generi: list, date: str, citta: str, artisti: str, prezzo: str) -> list:
    # funzione che restituisce una lista di festival in base ai filtri inseriti.
    ...


def ricerca_generale(stringa: str) -> list:
    # funzione che data una stringa in input, interroghi tutti i campi dei documenti e restituisca una lista di concerti
    ...
