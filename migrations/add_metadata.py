from pymongo import MongoClient

#Conexión:
cliente = MongoClient("mongodb://prelara:pr3l4r4m3c@27.0.172.67/prelara")
db = cliente["prelara"]

def add_metadata():
    #Colección audios
    resultado_audios = db.audios.update_many(
        {"metadata": {"$exists": False}},
        {
            "$set":{
                "metadata": {
                    "fuente": "audio",
                    "idioma": "ES",
                    "version": "1"
                }
            }
        }
    )

    #Colección syllabus
    resultado_syllabus = db.syllabus.update_many(
        {"metadata" : {"$exists" : False}},
        {
            "$set": {
                "metadata": {
                    "fuente": "syllabus",
                    "idioma": "ES",
                    "version": "1"
                }
            }
        }
    )

    print("Migración de metadata completada")
    print(f"Audios modificados: {resultado_audios.modified_count}")
    print(f"Syllabus modificados: {resultado_syllabus.modified_count}")


if __name__ == "__main__":
    add_metadata()