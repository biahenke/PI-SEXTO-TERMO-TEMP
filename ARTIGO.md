# Da Captura à Persistência: Monitoramento de Sensores Ambientais com LoRa e MongoDB

**Beatriz Nunes Henke**  
*Aluna na Fatec Pompeia Shunji Nishimura*  
26 de outubro de 2026  

---

Na 10ª atividade prática da disciplina de Projeto Integrador de Big Data, desenvolvi a análise e acompanhamento do pipeline de telemetria ambiental. O objetivo foi estruturar a esteira de dados que monitora temperatura e umidade via sensor DHT11, garantindo que cada medição de campo seja transmitida e armazenada com segurança em banco NoSQL.

A esteira de transmissão foi composta por cinco etapas integradas:
DHT11 ➔ Arduino Mega ➔ Rádio LoRa (Heltec / Meshtastic) ➔ Broker MQTT ➔ Servidor MongoDB (iot.sensores).

Para validar a consistência das leituras antes de automatizar o consumo, organizei uma síntese com o comportamento temporal das variáveis coletadas:

Métricas consolidadas e histórico das medições:

[IMAGEM 1 - TABELA DE MEDIÇÕES DO SENSOR]

Para consumir essas informações em tempo real via terminal, implementamos o script em Python consulta_mongo.py 200. Ele realiza a busca dos 200 registros mais recentes na base e entra em modo de escuta ativa a cada 2 segundos, capturando novos pacotes conforme chegam sem sobrecarregar o banco com chamadas manuais:

Extração das 200 leituras mais recentes e escuta em tempo real:

[IMAGEM 2 - TERMINAL VS CODE EXECUTANDO A CONSULTA]

Os registros consolidados ficam armazenados como documentos flexíveis na coleção iot.sensores. A verificação direta na base permite validar se a carga útil (payload decodificado) e os metadados da rede mesh foram serializados corretamente para futuras agregações analíticas:

Inspeção dos documentos persistidos no MongoDB:

[IMAGEM 3 - DOCUMENTOS NO MONGODB COMPASS]

Essa atividade foi fundamental para vivenciar na prática a integração entre dispositivos embarcados de baixo consumo e bancos Não-Relacionais voltados a grandes volumes de dados de IoT.

O código-fonte com os scripts e o passo a passo de execução estão disponíveis no meu repositório:
Repositório: https://github.com/biahenke/PI-SEXTO-TERMO-TEMP

Atividade 10 — IAL220, Projeto Integrador de Big Data
Fatec Shunji Nishimura Pompeia | Allan Siriani, PhD

#BigData #IoT #MongoDB #Meshtastic #EngenhariaDeDados #Fatec #Python #LoRa
