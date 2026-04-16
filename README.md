# Healthcare virtual assistant
La challenge consiste nello sviluppare un assistente virtuale per il settore sanitario. L’obiettivo è creare un sistema che possa:

- Rispondere a domande complesse dei pazienti
- Fornire consigli medici di base
- Gestire gli appuntamenti
- Comprendere e generare risposte contestuali in modo accurato e naturale
 

### Componenti 

1. Database

- Relazionale/NoSQL: per informazioni su pazienti, medici, appuntamenti e chat (a scelta: MySQL, MongoDB, PostgreSQL, ecc.)
- Database vettoriale: per la memorizzazione degli embeddings del sistema RAG

2. Backend

- Da implementare con Node.js, Django, Flask o Ruby on Rails
- Deve esporre API REST per tutte le operazioni CRUD su pazienti, medici, appuntamenti e chat

3. Frontend

- Sviluppato in HTML/CSS/JavaScript o framework (React, Angular, Vue.js)
- Deve permettere il dialogo con l’assistente, la visualizzazione delle risposte, la gestione degli appuntamenti e la consultazione dello storico chat
 

### Funzionalità richieste

**Priorità alta**

- Gestione chat: interazione tramite chat con RAG per risposte contestuali (utilizzo dei dataset MedQuAD e MIMIC-III in sinergia)
- Sistema RAG: risposte accurate grazie ai due dataset
- Raccomandazione medico: suggerimento del medico più adatto una volta compresa la necessità del cliente
- Proposta slot liberi: mostrare disponibilità dei medici e prenotazione appuntamenti

**Priorità media**
- Upload foto diagnosi/analisi: possibilità di caricare immagini diagnostiche o analisi
- Visualizzazione prenotazioni: elenco delle proprie prenotazioni
- Storico chat: accesso alle conversazioni passate
 
**Priorità bassa (facoltativo)**
- Login/registrazione utente
- Modifica/cancellazione prenotazioni
- Interfaccia lato medico: visualizzazione pazienti/prenotazioni
- Pagina preview medico: dettaglio problema paziente e chat precedente

_Le funzionalità a priorità bassa sono opzionali: implementale solo dopo aver completato le funzionalità principali (CRUD)._
 

**Requisito obbligatorio:** integra almeno un’altra funzionalità di AI a tua scelta, rilevante per questo caso d’uso.


