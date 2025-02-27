import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

# Yhdistä tietokantaan
connection_string = os.getenv("MONGO_URI")

client = pymongo.MongoClient(connection_string)

# Valitse tietokanta ja kokoelma
database = client.get_database("tikape")
apartments = database["apartments"]

# Tarkistetaan yhteys tulostamalla asuntojen kokonaismäärä
count = apartments.count_documents({})
print(f"Asuntojen kokonaismäärä: {count}")

# Tulostetaan esimerkki asunnosta
first_apartment = apartments.find_one()
print("Esimerkkiasunto:")
print(first_apartment)

# Osatehtävä 1: Postinumerot
print("\n--- Osatehtävä 1: Postinumerot ---")
postinumero_count = apartments.count_documents({"zip_code": "00700"})
print(f"Asuntojen määrä postinumerolla 00700: {postinumero_count}")

# Osatehtävä 2: Rakennusvuodet
print("\n--- Osatehtävä 2: Rakennusvuodet ---")
rakennus_count = apartments.count_documents({"construction_year": {"$gte": 2000}})
print(f"Asuntojen määrä 2000-luvulla rakennetuissa taloissa: {rakennus_count}")

# Osatehtävä 3: Pinta-alat
print("\n--- Osatehtävä 3: Pinta-alat ---")
pinta_ala_count = apartments.count_documents({"apartment_size": {"$gte": 50, "$lte": 70}})
print(f"Asuntojen määrä, joiden pinta-ala on 50-70 m²: {pinta_ala_count}")

# Osatehtävä 4: Myyntimäärät
print("\n--- Osatehtävä 4: Myyntimäärät ---")
myynti_count = apartments.count_documents({
    "transactions": {
        "$elemMatch": {
            "date": {
                "$gte": "2010-01-01",
                "$lte": "2012-12-31"
            }
        }
    }
})
print(f"Asuntojen määrä, jotka on myyty ainakin kerran 2010-2012: {myynti_count}")

# Osatehtävä 5: Myyntihinnat
print("\n--- Osatehtävä 5: Myyntihinnat ---")
pipeline = [
    {"$unwind": "$transactions"},
    {"$group": {"_id": None, "max_price": {"$max": "$transactions.selling_price"}}},
    {"$project": {"_id": 0, "max_price": 1}}
]
result = list(apartments.aggregate(pipeline))
max_price = result[0]["max_price"]
print(f"Kallein asunnon myyntihinta aineistossa: {max_price}")