# Do Pacote Bruto ao Dado Útil: Monitoramento de Sensores com Meshtastic e MongoDB

> **Atividade de Projeto Integrador — Big Data & IoT**  
> **Autora:** Beatriz Nunes Henke  
> **Orientação:** Prof. Allan Siriani, PhD | Fatec Shunji Nishimura Pompeia  

---

## 📌 Introdução

No contexto da agricultura digital e da Internet das Coisas (IoT), a telemetria em campo enfrenta desafios críticos de conectividade e alcance. O uso de redes em malha (*mesh networks*) operando via rádio frequência LoRa, por meio do ecossistema **Meshtastic**, viabiliza uma infraestrutura de baixo consumo e grande resiliência para a coleta descentralizada de dados ambientais.

Neste projeto integrador, exploramos todo o ciclo de vida do dado: desde a leitura de temperatura e umidade com sensor **DHT11**, passando pela transmissão por rádio LoRa, corretagem MQTT e ingestão no banco de dados NoSQL **MongoDB** (na base `iot`, coleção `sensores`), até o consumo analítico com agregações estatísticas e scripts em **Python**.

---

## 🏗️ Arquitetura da Solução

O dado percorre uma cadeia bem estruturada até se tornar informação analítica:

```
[ Sensor DHT11 ]
       │ (Leitura analógica/digital)
       ▼
[ Arduino Mega ]
       │ (Comunicação Serial)
       ▼
[ Heltec LoRa ESP32 (!8fa724e8) ]
       │ (Transmissão Mesh LoRa)
       ▼
[ Gateway / Broker MQTT ]
       │ (Payload JSON publicado no tópico sensores/tempUmid/2/json/mqtt_teste/...)
       ▼
[ Serviço de Ingestão do Servidor ]
       │ (Persistência NoSQL)
       ▼
[ MongoDB Server (iot.sensores) ]
       │
       ├─► Consultas e Agregações (MongoDB Compass / mongosh)
       └─► Script de Consumo em Tempo Real (Python + PyMongo)
```

---

## 📦 Estrutura do Documento Real no MongoDB

Um dos grandes diferenciais do MongoDB em projetos de IoT é a capacidade de persistir documentos semiestruturados, guardando tanto a mensagem de rede bruta quanto o payload decodificado.

Abaixo está o exemplo de um documento real persistido na coleção `sensores`:

```json
{
  "_id": ObjectId("6adce936e61373062a68c4a6"),
  "topic": "sensores/tempUmid/2/json/mqtt_teste/!8fa724e8",
  "payload": "{\"channel\":0,\"from\":2410095848,\"hop_start\":3,\"hops_away\":0,\"id\":263253573,\"payload\":{\"t\":23,\"u\":14},\"sender\":\"!8fa724e8\",\"timestamp\":1792862500,\"to\":4294967295,\"type\":\"text\"}",
  "payload_data": {
    "channel": 0,
    "from": 2410095848,
    "hop_start": 3,
    "hops_away": 0,
    "id": 263253573,
    "payload": {
      "t": 23,
      "u": 14
    },
    "sender": "!8fa724e8",
    "timestamp": 1792862500,
    "to": 4294967295,
    "type": "text"
  },
  "received_at": ISODate("2026-10-24T17:21:58.271Z"),
  "qos": 0,
  "retain": false,
  "data": ISODate("2026-10-24T17:21:58.271Z")
}
```

### 💡 Boas Práticas e Engenharia de Dados:
1. **Tratamento de Fuso Horário:** Os registros chegam com `received_at` em **UTC**. Para análises locais (Horário de Brasília), aplicamos a conversão para `America/Sao_Paulo` (UTC - 3).
2. **Filtragem de Ruído:** Nem todo documento contém leitura de telemetria. Filtramos com `"payload_data.payload.t": { $exists: true }` para garantir a integridade das métricas.
3. **Exploração Segura:** Em ambientes compartilhados de Big Data, utilizamos estritamente comandos de leitura (`find`, `countDocuments`, `aggregate`) sempre acompanhados de `.limit()`.
4. **Standalone vs Change Streams:** Por se tratar de um servidor standalone (sem replica set), o monitoramento em tempo real é feito via polling consultando `_id` maior que o último registrado.

---

## 🔍 Consultas e Agregações Analíticas

### 1. Últimas Leituras do Rádio
```javascript
db.sensores.find(
  { 
    "payload_data.sender": "!8fa724e8", 
    "payload_data.payload.t": { $exists: true } 
  },
  { 
    _id: 0, 
    received_at: 1, 
    temp: "$payload_data.payload.t", 
    umid: "$payload_data.payload.u" 
  }
).sort({ _id: -1 }).limit(10)
```

### 2. Agregação Temporal: Média, Mínima e Máxima por Hora
```javascript
db.sensores.aggregate([
  { 
    $match: { 
      "payload_data.sender": "!8fa724e8", 
      "payload_data.payload.t": { $exists: true } 
    } 
  },
  { 
    $group: {
      _id: { 
        $dateToString: { 
          date: "$received_at", 
          format: "%Y-%m-%d %H:00", 
          timezone: "America/Sao_Paulo" 
        } 
      },
      media_temp: { $avg: "$payload_data.payload.t" },
      min_temp:   { $min: "$payload_data.payload.t" },
      max_temp:   { $max: "$payload_data.payload.t" },
      media_umid: { $avg: "$payload_data.payload.u" },
      leituras:   { $sum: 1 }
    } 
  },
  { $sort: { _id: -1 } },
  { $limit: 5 }
])
```

#### 📊 Resultado Real da Agregação (Base Fatec):
```json
[
  {
    "_id": "2026-10-24 14:00",
    "media_temp": 23.00,
    "min_temp": 23,
    "max_temp": 23,
    "media_umid": 14.00,
    "leituras": 12
  },
  {
    "_id": "2026-10-24 13:00",
    "media_temp": 23.00,
    "min_temp": 23,
    "max_temp": 23,
    "media_umid": 14.00,
    "leituras": 36
  },
  {
    "_id": "2026-10-24 12:00",
    "media_temp": 22.17,
    "min_temp": 22,
    "max_temp": 23,
    "media_umid": 14.83,
    "leituras": 36
  },
  {
    "_id": "2026-10-24 11:00",
    "media_temp": 21.58,
    "min_temp": 21,
    "max_temp": 22,
    "media_umid": 15.08,
    "leituras": 36
  },
  {
    "_id": "2026-10-24 10:00",
    "media_temp": 21.00,
    "min_temp": 21,
    "max_temp": 21,
    "media_umid": 15.00,
    "leituras": 36
  }
]
```

---

## 💻 Consumo com Python (`pymongo`)

Com a biblioteca `pymongo` e `python-dotenv`, o consumo é realizado de forma automatizada e protegida:

```python
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
cliente = MongoClient(os.environ["MONGO_URI"])
col = cliente[os.environ["MONGO_DB"]][os.environ["MONGO_COLLECTION"]]

filtro = {
    "payload_data.sender": "!8fa724e8",
    "payload_data.payload.t": {"$exists": True}
}

for doc in col.find(filtro).sort("_id", -1).limit(10):
    t = doc["payload_data"]["payload"]["t"]
    u = doc["payload_data"]["payload"]["u"]
    print(f"[{doc['received_at']}] Temp: {t}°C | Umidade: {u}%")
```

---

## 📸 Evidências das Leituras no Terminal

Output real obtido na consulta da base `iot.sensores`:

```text
Conectando ao MongoDB em iot.sensores...
Total estimado de documentos: 2.807
Documentos válidos do rádio (!8fa724e8): 2.659

Últimas leituras registradas:
-----------------------------------------------------------------
[24/10/2026 14:03:50] !8fa724e8 | Temp: 23.0 °C | Umidade: 14.0 %
[24/10/2026 14:08:35] !8fa724e8 | Temp: 23.0 °C | Umidade: 14.0 %
[24/10/2026 14:08:41] !8fa724e8 | Temp: 23.0 °C | Umidade: 14.0 %
[24/10/2026 14:08:49] !8fa724e8 | Temp: 23.0 °C | Umidade: 14.0 %
[24/10/2026 14:13:34] !8fa724e8 | Temp: 23.0 °C | Umidade: 14.0 %
[24/10/2026 14:13:42] !8fa724e8 | Temp: 23.0 °C | Umidade: 14.0 %
[24/10/2026 14:13:49] !8fa724e8 | Temp: 23.0 °C | Umidade: 14.0 %
[24/10/2026 14:21:42] !8fa724e8 | Temp: 23.0 °C | Umidade: 14.0 %
[24/10/2026 14:21:48] !8fa724e8 | Temp: 23.0 °C | Umidade: 14.0 %
[24/10/2026 14:21:58] !8fa724e8 | Temp: 23.0 °C | Umidade: 14.0 %
-----------------------------------------------------------------
```

> **Dica para o post:** Tire um print do seu terminal executando `python consultar_leituras_reais.py` ou `python consulta_mongo.py` e um print da tela do **MongoDB Compass** com o documento aberto.

---

## 🎯 Conclusão

A integração entre hardware de baixo custo, rádio LoRa via Meshtastic e bancos de dados NoSQL consolida uma arquitetura extremamente robusta e escalável. O MongoDB permitiu acomodar com naturalidade o esquema variável dos pacotes de telemetria sem perda de metadados, enquanto o pipeline de agregação forneceu estatísticas instantâneas de temperatura e umidade, fundamentais para a tomada de decisão agronômica e monitoramento contínuo.

---

### 🏷️ Hashtags para a postagem no LinkedIn:
`#BigData #IoT #MongoDB #Meshtastic #LoRa #EngenhariaDeDados #ProjetoIntegrador #Fatec #Agronegocio #Python #NoSQL`
