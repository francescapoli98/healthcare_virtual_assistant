# Healthcare virtual assistant 🤖⚕️
Sviluppo di un assistente virtuale per il settore sanitario che combina un sistema RAG su dataset medici specializzati con funzionalità di triage automatico, raccomandazione del medico e gestione degli appuntamenti.

## 🔧 Setup e avvio 
- **Prerequisiti:** Docker e Docker Compose installati
1. Clona il repository
```bash
git clone https://github.com/tuo-username/healthcare_virtual_assistant.git
cd healthcare_virtual_assistant
```
2. Configura le variabili d'ambiente: modifica `.env` con le tue API keys (Groq, HuggingFace necessarie)
```bash
cp .env.example .env
```
#### Opzione 1: uso di Docker Hub
3. Avvia i container
```bash
docker-compose up --build
```
#### Opzione 2: build in locale
3. Costruisci gli indici FAISS (solo la prima volta)
```bash
docker compose run backend python -m app.rag.build_index
```
6. Avvia tutto con Docker
```bash
docker-compose up --build
```
5. Vedi su `http://localhost:5173`

-----------------------------

## 📁 Struttura del Progetto
 
```
healthcare_virtual_assistant/
│
├── app/                          # Package principale del backend Flask
│   ├── rag/                      # Pipeline RAG: embeddings, query FAISS, composizione contesto LLM
│   ├── routes/                   # Blueprint Flask con tutti gli endpoint REST
│   ├── __init__.py               # Application factory
│   ├── config.py                 # Configurazione centralizzata (DB, chiavi API, parametri RAG)
│   ├── core.py                   # Logica di business: orchestrazione triage → RAG → risposta
│   ├── extensions.py             # Estensioni Flask (SQLAlchemy, Login, CORS)
│   ├── models.py                 # Modelli ORM: Paziente, Medico, Appuntamento, Messaggio
│   ├── dockerfile                # Dockerfile del servizio backend
│   └── requirements.txt          # Dipendenze Python
│
├── faiss_index/                  # Indice FAISS pre-costruito (embeddings MedQuAD + Asclepius)
│
├── frontend/                     # Applicazione React
│
├── docker-entrypoint-initdb.d/   # Script SQL per inizializzazione e seeding del DB MySQL
│
├── .env.example                  # Template variabili d'ambiente (copiare in .env)
├── docker-compose.yml            # Orchestrazione multi-container (Flask + React + MySQL)
└── run.py                        # Entry point Flask (sviluppo locale)
```
  
## ✅ Funzionalità Implementate
- [x] **Chat con RAG** — interazione in linguaggio naturale con contesto recuperato da MedQuAD e Asclepius¹
- [x] **Raccomandazione medico** — suggerimento del professionista più adatto in base ai sintomi
- [x] **Proposta slot liberi e prenotazione** — visualizzazione disponibilità e booking appuntamenti
- [x] **Visualizzazione prenotazioni** — elenco delle prenotazioni dell'utente autenticato
- [x] **Login / Registrazione utente**
- [x] **Modifica / Cancellazione prenotazioni**
### AI Feature aggiuntiva — Triage automatico
Il sistema classifica i sintomi descritti dall'utente in tre livelli di urgenza (**bassa / media / alta**) prima di formulare la risposta. In caso di urgenza alta, viene mostrato un avviso esplicito. Il risultato del triage influenza anche la raccomandazione del medico specialista.
## Sistema RAG
 
L'indice FAISS in `faiss_index/` è pre-costruito a partire da:
 
- **MedQuAD** — dataset di domande e risposte mediche
- **Asclepius** — dataset clinico con note in linguaggio naturale
 
