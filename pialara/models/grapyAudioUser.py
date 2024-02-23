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
        user_id = data['usuarioId']
        month = []
        audios = []

        for i in range(len(data['audiosPorMes'])):
            month.append(int(data['audiosPorMes'][i]["month"]))
            audios.append(int(data['audiosPorMes'][i]["totalAudios"]))

        month_array = np.array(month)
        audios_array = ",".join(map(str, audios)) 

        return cls(user_id, month_array, audios_array)

    def to_dict(self):
        return {
            '_id': self.user_id,
            'month': self.month,
            'totalAudios': self.total_audios
        }
    @classmethod
    def execute_aggregation(cls):
        client = MongoClient('mongodb://localhost:27017/pialara')
        db = client.pialara  # Change 'pialara' to your actual database name
        audios_collection = db.audios 

        # Calculate the date 90 days ago
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)

        pipeline = [
            {
                "$match": {
                    "fecha": {
                        "$gte": ninety_days_ago,
                        "$lte": datetime.now()
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "usuarioId": "$usuario.id",
                        "month": { "$month": "$fecha" }
                    },
                    "totalAudios": { "$sum": 1 }
                }
            },
            {
                "$group": {
                    "_id": "$_id.usuarioId",
                    "audiosPorMes": {
                        "$push": {
                            "month": "$_id.month",
                            "totalAudios": "$totalAudios"
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "usuarioId": "$_id",
                    "audiosPorMes": {
                        "$concatArrays": [
                            { "$filter": { "input": "$audiosPorMes", "as": "audios", "cond": { "$eq": ["$$audios.month", 1] } } },
                            { "$filter": { "input": "$audiosPorMes", "as": "audios", "cond": { "$eq": ["$$audios.month", 2] } } },
                            { "$filter": { "input": "$audiosPorMes", "as": "audios", "cond": { "$eq": ["$$audios.month", 3] } } }
                        ]
                    }
                }
            },
            {
                "$project": {
                    "usuarioId": 1,
                    "audiosPorMes": {
                        "$map": {
                            "input": [1, 2, 3],
                            "as": "month",
                            "in": {
                                "month": "$$month",
                                "totalAudios": {
                                    "$sum": {
                                        "$map": {
                                            "input": { "$ifNull": [{ "$filter": { "input": "$audiosPorMes", "as": "audios", "cond": { "$eq": ["$$audios.month", "$$month"] } } }, []] },
                                            "as": "audio",
                                            "in": "$$audio.totalAudios"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        ]

        result = list(audios_collection.aggregate(pipeline))
        print(result)
        dataUsers={}
        for data in result:
            wow= AudioModel.from_dict(data)
            dataUsers[wow.user_id]=wow.total_audios
     
# Ahora audio_results es un diccionario donde las claves son los ObjectIds convertidos a cadena
# y los valores son listas asociativas con la información que necesitas.







        return dataUsers




