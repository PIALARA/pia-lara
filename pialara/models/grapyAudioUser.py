from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta

class AudioModel:
    def __init__(self, user_id, month, total_audios):
        self.user_id = user_id
        self.month = month
        self.total_audios = total_audios

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data['_id'],
            month=None,  # Set to appropriate value based on your data structure
            total_audios=data['audiosPorMes']
        )

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
                        "$gte": ninety_days_ago
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

        audio_results = [sum(entry['totalAudios'] for entry in data['audiosPorMes']) for data in result]






        return audio_results




