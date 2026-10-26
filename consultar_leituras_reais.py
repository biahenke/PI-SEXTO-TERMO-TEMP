"""
Consulta estritamente de leitura das leituras reais no MongoDB.
Respeita o limite e boas práticas do projeto.
"""
import os
import json
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def main():
    uri = os.environ["MONGO_URI"]
    db_name = os.environ.get("MONGO_DB", "iot")
    col_name = os.environ.get("MONGO_COLLECTION", "sensores")

    print(f"Conectando ao MongoDB em {db_name}.{col_name}...")
    cliente = MongoClient(uri, serverSelectionTimeoutMS=8000)
    col = cliente[db_name][col_name]

    total = col.estimated_document_count()
    print(f"Total estimado de documentos: {total}\n")

    # 1. Últimas 10 leituras do rádio
    filtro_radio = {
        "payload_data.sender": "!8fa724e8",
        "payload_data.payload.t": {"$exists": True}
    }
    total_radio = col.count_documents(filtro_radio)
    print(f"Documentos válidos do rádio (!8fa724e8): {total_radio}")
    print("Últimas 10 leituras:")
    print("-" * 65)

    recentes = list(col.find(filtro_radio).sort("_id", -1).limit(10))
    for doc in reversed(recentes):
        quando = doc.get("received_at") or doc["_id"].generation_time
        hora = quando.strftime("%d/%m/%Y %H:%M:%S UTC")
        payload = doc.get("payload_data", {}).get("payload", {})
        temp = payload.get("temp", payload.get("t"))
        umid = payload.get("umid", payload.get("u"))
        sender = doc.get("payload_data", {}).get("sender", "?")
        print(f"[{hora}] {sender} | Temp: {temp} °C | Umidade: {umid} %")

    print("-" * 65)

    # 2. Exemplo de agregação por hora no horário de Brasília (UTC-3)
    print("\nExecutando agregação por hora (Média, Mínima, Máxima):")
    pipeline = [
        {"$match": filtro_radio},
        {"$group": {
            "_id": {
                "$dateToString": {
                    "date": "$received_at",
                    "format": "%Y-%m-%d %H:00",
                    "timezone": "America/Sao_Paulo"
                }
            },
            "media_temp": {"$avg": "$payload_data.payload.t"},
            "min_temp": {"$min": "$payload_data.payload.t"},
            "max_temp": {"$max": "$payload_data.payload.t"},
            "media_umid": {"$avg": "$payload_data.payload.u"},
            "leituras": {"$sum": 1}
        }},
        {"$sort": {"_id": -1}},
        {"$limit": 5}
    ]

    agregados = list(col.aggregate(pipeline))
    print(json.dumps(agregados, indent=2, ensure_ascii=False))

    # 3. Exemplo real de 1 documento completo para usar no artigo
    if recentes:
        print("\nExemplo de documento real:")
        doc_exemplo = recentes[0].copy()
        doc_exemplo["_id"] = str(doc_exemplo["_id"])
        if isinstance(doc_exemplo.get("received_at"), datetime):
            doc_exemplo["received_at"] = doc_exemplo["received_at"].isoformat()
        if isinstance(doc_exemplo.get("data"), datetime):
            doc_exemplo["data"] = doc_exemplo["data"].isoformat()
        print(json.dumps(doc_exemplo, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
