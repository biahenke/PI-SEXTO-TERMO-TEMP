"""
Simulador de Leituras para Demonstração e Prints do Artigo
Permite visualizar as leituras como se estivessem vindo do MongoDB ou da Serial.
"""
import time
import random
from datetime import datetime

def simular_consulta_mongo(total=10):
    print("iot.sensores: 1.482 registros. Últimos {}:\n".format(total))
    
    sender = "!8fa724e8"
    for i in range(total):
        agora = datetime.now()
        temp = round(random.uniform(20.5, 23.2), 1)
        umid = round(random.uniform(15.0, 19.5), 1)
        hora = agora.strftime("%d/%m %H:%M:%S")
        print(f"[{hora}] {sender} | Temperatura: {temp:5.1f} °C | Umidade: {umid:5.1f} %")
        time.sleep(0.1)

    print("\n--- Exemplo de Agregação (Média, Mínima e Máxima por Hora) ---")
    print("""[
  { "_id": "2026-10-26 15:00", "media_temp": 21.42, "min_temp": 19.8, "max_temp": 23.1, "media_umid": 16.8, "leituras": 142 },
  { "_id": "2026-10-26 14:00", "media_temp": 22.05, "min_temp": 20.3, "max_temp": 23.8, "media_umid": 16.2, "leituras": 180 },
  { "_id": "2026-10-26 13:00", "media_temp": 22.80, "min_temp": 21.0, "max_temp": 24.5, "media_umid": 15.5, "leituras": 175 }
]""")

if __name__ == "__main__":
    print("=" * 65)
    print(" SIMULADOR DE LEITURAS DE SENSORES - PROJETO INTEGRADOR IoT ")
    print("=" * 65)
    simular_consulta_mongo(10)
    print("=" * 65)
