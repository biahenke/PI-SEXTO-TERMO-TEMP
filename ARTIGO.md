# Do Rádio ao Banco NoSQL: Monitoramento de Sensores IoT com Meshtastic e MongoDB

**Beatriz Nunes Henke**  
*Aluna na Fatec Pompeia Shunji Nishimura*  
26 de outubro de 2026  

---

Na 10ª atividade prática da disciplina de Projeto Integrador de Big Data na Fatec Shunji Nishimura Pompeia, explorei o ciclo de vida completo de dados de telemetria ambiental em redes descentralizadas.

O projeto acompanha o fluxo de leituras de temperatura e umidade a partir de um sensor DHT11, passando por um microcontrolador Arduino Mega e um rádio LoRa Heltec (ESP32) com firmware Meshtastic. Os pacotes são encaminhados via protocolo MQTT e persistidos no servidor NoSQL MongoDB (banco `iot`, coleção `sensores`).

O caminho percorrido pelos dados:  
**DHT11 ➔ Arduino Mega ➔ Rádio Meshtastic (!8fa724e8) ➔ Broker MQTT ➔ MongoDB**

Para validar a recepção e consumir esses registros de forma automatizada, utilizamos scripts em Python com a biblioteca `pymongo`. Como o servidor opera em arquitetura standalone, estruturamos a escuta contínua via polling inteligente (filtrando por `_id` recente), garantindo uma consulta segura e com volume controlado (`limit`).

No terminal do VS Code, realizamos a extração das leituras mais recentes do rádio e ativamos o monitoramento em tempo real:

### Validação das Leituras no Terminal:

[INSERIR O PRINT DO SEU TERMINAL AQUI]

Essa prática reforçou na prática conceitos essenciais de IoT e Engenharia de Dados: desde a ingestão de payloads de rádio até a persistência NoSQL, viabilizando o monitoramento contínuo de variáveis ambientais no agronegócio.

---

O código e as instruções de execução estão disponíveis no meu repositório:  
**Repositório:** [https://github.com/biahenke/PI-SEXTO-TERMO-TEMP](https://github.com/biahenke/PI-SEXTO-TERMO-TEMP)

Atividade 10 — IAL220, Projeto Integrador de Big Data  
[Fatec Shunji Nishimura Pompeia](https://www.linkedin.com/company/fatecpompeiaoficial/) | [Allan Siriani, PhD](https://www.linkedin.com/in/siriani)

#BigData #IoT #MongoDB #Meshtastic #LoRa #EngenhariaDeDados #Fatec #Python #NoSQL
