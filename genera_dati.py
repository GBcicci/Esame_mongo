import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

generi_musicali = ["Rock", "Pop", "Hip Hop", "Electronic", "Jazz", "Blues", "Country", "Reggae"]
citta_italiane = ["Roma", "Milano", "Napoli", "Torino", "Palermo", "Genova", "Bologna", "Firenze", "Venezia", "Verona"]
province_italiane = ["RM", "MI", "NA", "TO", "PA", "GE", "BO", "FI", "VE", "VR"]


def generate_random_city_and_province():
    citta = random.choice(citta_italiane)
    provincia = province_italiane[citta_italiane.index(citta)]
    return citta, provincia


citta, provincia = generate_random_city_and_province()


def generate_geometry():
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    return {
        "type": "Point",
        "coordinates": [lon, lat]
    }


def generate_random_date(start_date="2020-01-01", end_date="2025-12-31"):
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    delta_days = (end_datetime - start_datetime).days
    random_days = random.randint(0, delta_days)
    random_date = start_datetime + timedelta(days=random_days)
    return random_date.date()


def generate_concert(data: list = False):
    concert = {
        "Nome_concerto": fake.catch_phrase(),
        "Nome_artista": [fake.name() for _ in range(random.randint(1, 3))],
        "Pseudonimi_artista": [fake.user_name() for _ in range(random.randint(1, 3))],
        "Generi": random.sample(generi_musicali, random.randint(1, len(generi_musicali))),
        "Data": str(generate_random_date()),
        "Ora": fake.time(),
        "Citta": citta,
        "Provincia": provincia,
        "geometry": generate_geometry(),
        "Prezzo_min": random.uniform(20, 100),
        "Prezzi": {f"Tipo_{i + 1}": round(random.uniform(30, 150), 2) for i in range(random.randint(1, 4))},
        "Biglietti_disponibili": random.randint(50, 500)
    }

    if not data:
        concert["Indirizzo"] = fake.address()
    if data:
        concert['Citta'] = data[0]
        concert['Provincia'] = data[1]
        concert['Indirizzo'] = data[2]
        concert['geometry'] = data[3]
    return concert


def generate_festival_data(data):
    num_festivals = random.randint(2, 5)
    festivals = []
    for _ in range(num_festivals):
        festivals.append(generate_concert(data))
    return festivals


def generate_festival():
    data = (citta, provincia, fake.address(), generate_geometry())
    concerts = generate_festival_data(data)
    festival = {
        "Nome_festival": fake.company(),
        "Generi": list(set([genre for concert in concerts for genre in concert["Generi"]])),
        "Artisti": list(set([artist for concert in concerts for artist in concert["Pseudonimi_artista"]])),
        "Data_inizio": min(concert["Data"] for concert in concerts),
        "Data_fine": max(concert["Data"] for concert in concerts),
        "Indirizzo": data[2],
        "Citta": data[0],
        "Provincia": data[1],
        "geometry": data[3],
        "Prezzo": round(random.uniform(50, 200), 2),
        "Biglietti_disponibili": min(concert["Biglietti_disponibili"] for concert in concerts)
    }
    json_string = json.dumps(festival, sort_keys=True)
    hash_value = f"_{hash(json_string)}_"
    festival['id_univoco'] = hash_value
    for concert in concerts:
        concert['id_festival'] = hash_value
    return festival, concerts


if __name__ == "__main__":
    festival_list = []
    concert_list = []

    # Genera 20 concerti non associati a festival
    for _ in range(40):
        concert = generate_concert()
        concert_list.append(concert)

    # Genera 5 festival con i rispettivi concerti
    for _ in range(10):
        festival, concerts = generate_festival()
        festival_list.append(festival)
        for concert in concerts:
            concert_list.append(concert)

    # Salva i dati del festival in un file JSON
    with open("dati_festival.json", "w") as festival_file:
        json.dump(festival_list, festival_file, indent=4)

    # Salva i dati dei concerti in un file JSON
    with open("dati_concerti.json", "w") as concert_file:
        json.dump(concert_list, concert_file, indent=4)
