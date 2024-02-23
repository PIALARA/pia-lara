from pymongo import MongoClient
import numpy as np
from bson import ObjectId
from datetime import datetime, timedelta

class AudioModel:
    def __init__(self, user_id, month, total_audios):
        self.user_id = user_id
        self.month = month
        self.total_audios = total_audios

    @classmethod
    def from_dict(cls, data):
        user_id = data['_id']
        month = []
        audios = []
        fecha_hace_90_dias = datetime.now() - timedelta(days=90)
        # Obtener el mes y el año actuales
        mes_actual = datetime.now().month
        año_actual = datetime.now().year

        # Inicializar listas para almacenar los datos
        month = []
        audios = []

        # Iterar sobre cada elemento en data['countsByMonth']
        for item in data['countsByMonth']:
            # Extraer el mes y el año del registro
            mes_registro, año_registro = map(int, item["monthYear"].split('-'))

            # Verificar si el mes y el año corresponden al mes actual, al mes anterior o al año anterior al mes actual
            if (año_registro == año_actual and mes_registro == mes_actual) or \
            (año_registro == año_actual and mes_registro == mes_actual - 1) or \
            (año_registro == año_actual - 1 and mes_registro == 12):
                # Si coincide, añadir el registro al array de meses y el número de audios al array de audios
                month.append(item["monthYear"])
                print("itemcount",item["count"])
                audios.append(item["count"])

        # Convertir a numpy array
        month_array = np.array(month)
        print("month array:", month_array)
        audios_array = ",".join(map(str, audios))

        return cls(user_id, month_array, audios_array)

    def to_dict(self):
        return {
            '_id': self.user_id,
            'month': self.month,
            'totalAudios': self.total_audios
        }
    @classmethod
    def execute_aggregation(cls,id_user):
        client = MongoClient('mongodb://localhost:27017/pialara')
        db = client.pialara  # Change 'pialara' to your actual database name
        audios_collection = db.audios 

        # Calculate the date 90 days ago

        pipeline  = [
                    {
                        "$match": {
                            "usuario.parent": id_user  # Filtras por el ID de usuario proporcionado
                        }
                    },
                    {
                        "$group": {
                            "_id": {
                                "month": {"$month": "$fecha"},  # Agrupas por mes
                                "year": {"$year": "$fecha"},    # y año
                                "userId": "$usuario.id"         # y el ID de usuario
                            },
                            "count": {"$sum": 1}  # Cuentas los registros en cada grupo
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "userId": "$_id.userId",
                            "monthYear": {
                                "$concat": [
                                    {"$toString": "$_id.month"},  # Convertimos el mes a string
                                    "-",                          # Agregamos un guión para separar
                                    {"$toString": "$_id.year"}    # Convertimos el año a string
                                ]
                            },
                            "count": 1
                        }
                    },
                    {
                        "$group": {
                            "_id": "$userId",  # Agrupas por ID de usuario
                            "countsByMonth": {
                                "$push": {
                                    "monthYear": "$monthYear",  # Guardas el mes y el año concatenados
                                    "count": "$count"           # y el conteo
                                }
                            }
                        }
                    }
                ]



        result = list(audios_collection.aggregate(pipeline))
        
        dataUsers=[]
        for data in result:
            
            wow= AudioModel.from_dict(data)
            print("mont",wow.month,"count",wow.total_audios)
            dataUsers.append(wow)
     
# Ahora audio_results es un diccionario donde las claves son los ObjectIds convertidos a cadena
# y los valores son listas asociativas con la información que necesitas.
        return dataUsers




