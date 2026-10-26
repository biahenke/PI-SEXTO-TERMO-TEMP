# Do pacote bruto ao dado útil: leituras de sensores com Meshtastic e MongoDB

**Beatriz Nunes Henke**  
*Aluna na Fatec Pompeia Shunji Nishimura*  
26 de outubro de 2026  

---

Atividade 10 de Projeto Integrador de Big Data, trabalhei com a coleta e consulta de leituras de sensores. O projeto acompanha temperatura e umidade do DHT11 e permite observar os dados recebidos e armazenados no MongoDB.

O caminho dos dados é:  
**DHT11 → Arduino Mega → rádio Meshtastic → MQTT → MongoDB.**

Para facilitar a conferência, organizei as informações dos sensores e preparei uma consulta que mostra as leituras recentes e continua acompanhando as novas.

### Resumo dos sensores e das informações coletadas:

> *[ INSERIR AQUI O PRINT 1: Tabela verde de medições do sensor ]*

No terminal, executo `python consulta_mongo.py 200` para exibir as 200 leituras mais recentes. Depois, o script verifica periodicamente a chegada de novos registros. Assim, é possível acompanhar os dados sem consultar o banco manualmente a cada leitura.

### Consulta das 200 leituras mais recentes e acompanhamento das novas:

> *[ INSERIR AQUI O PRINT 2: Terminal do VS Code rodando a consulta das 200 leituras ]*

O MongoDB mantém os documentos recebidos na coleção `iot.sensores`. Conferir os registros no banco ajuda a validar que as mensagens estão chegando e permite consultar os dados posteriormente.

### Registros armazenados no MongoDB:

> *[ INSERIR AQUI O PRINT 3: Tela do MongoDB Compass com a coleção sensores aberta ]*

---

Este trabalho foi um passo para transformar mensagens de sensores em dados que podem ser acompanhados e consultados. O código e as instruções para executar o projeto estão no repositório:

**Repositório:** [https://github.com/biahenke/PI-SEXTO-TERMO-TEMP](https://github.com/biahenke/PI-SEXTO-TERMO-TEMP)

Atividade 10 — IAL220, Projeto Integrador de Big Data  
[Fatec Shunji Nishimura Pompeia](https://www.linkedin.com/company/fatecpompeiaoficial/) | [Allan Siriani, PhD](https://www.linkedin.com/in/siriani)

#BigData #IoT #MongoDB #Meshtastic #EngenhariaDeDados #Fatec
