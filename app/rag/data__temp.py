'''
DA SOSTITUIRE CON MEDQUADS O ALTRO DATABASE VETTORIALE
'''
# Dati medici di esempio in italiano.
# Da sostituire questa lista con il vero dataset MedQuAD (file JSON o CSV nella stessa cartella).

MEDICAL_DOCS = [
    {
        "id": "med_001",
        "domanda": "Quali sono i sintomi del diabete di tipo 2?",
        "risposta": (
            "I sintomi più comuni del diabete di tipo 2 includono: sete eccessiva, "
            "minzione frequente, affaticamento, visione offuscata, guarigione lenta "
            "delle ferite, formicolio alle mani o ai piedi. Molte persone non presentano "
            "sintomi nelle fasi iniziali, quindi i controlli regolari della glicemia "
            "sono fondamentali."
        ),
        "categoria": "diabete",
    },
    {
        "id": "med_002",
        "domanda": "Come si controlla la pressione alta?",
        "risposta": (
            "L'ipertensione si gestisce con: riduzione del sale nella dieta, "
            "attività fisica regolare (almeno 30 minuti al giorno), mantenimento "
            "di un peso sano, limitazione dell'alcol e smettere di fumare. "
            "Se lo stile di vita non basta, il medico può prescrivere farmaci "
            "antipertensivi come ACE-inibitori, sartani o betabloccanti."
        ),
        "categoria": "cardiologia",
    },
    {
        "id": "med_003",
        "domanda": "Cosa fare in caso di mal di schiena lombare?",
        "risposta": (
            "Per il mal di schiena acuto: riposo breve (1-2 giorni al massimo), "
            "applicare ghiaccio nelle prime 48 ore poi calore, antinfiammatori "
            "da banco come ibuprofene se tollerati. Per la prevenzione: rafforzare "
            "i muscoli addominali e paravertebrali, mantenere una postura corretta, "
            "evitare di sollevare pesi in modo scorretto. Se il dolore dura più di "
            "6 settimane o irradia alla gamba, consultare un medico."
        ),
        "categoria": "ortopedia",
    },
    {
        "id": "med_004",
        "domanda": "Quali sono i sintomi di un infarto?",
        "risposta": (
            "I sintomi classici dell'infarto includono: dolore o pressione al petto "
            "che può irradiarsi al braccio sinistro, alla mascella o alla schiena, "
            "mancanza di respiro, sudorazione fredda, nausea, sensazione di "
            "stordimento. ATTENZIONE: in caso di sospetto infarto chiamare "
            "immediatamente il 118. Non guidare autonomamente al pronto soccorso."
        ),
        "categoria": "cardiologia",
    },
    {
        "id": "med_005",
        "domanda": "Come si tratta una dermatite atopica?",
        "risposta": (
            "La dermatite atopica si gestisce con: idratazione quotidiana della "
            "pelle con emollienti, evitare saponi aggressivi e profumi, "
            "corticosteroidi topici nelle fasi acute (da usare solo su indicazione "
            "medica), antistaminici per il prurito, identificare e rimuovere i "
            "fattori scatenanti (alcuni alimenti, acari, stress). I casi gravi "
            "possono richiedere immunosoppressori o biologici."
        ),
        "categoria": "dermatologia",
    },
    {
        "id": "med_006",
        "domanda": "Cosa sono le aritmie cardiache?",
        "risposta": (
            "Le aritmie sono alterazioni del ritmo cardiaco: il cuore può battere "
            "troppo veloce (tachicardia), troppo lento (bradicardia) o in modo "
            "irregolare (come la fibrillazione atriale). I sintomi includono "
            "palpitazioni, vertigini, mancanza di respiro, svenimento. "
            "La diagnosi si fa con ECG o Holter cardiaco. Il trattamento dipende "
            "dal tipo: farmaci antiaritmici, ablazione o pacemaker."
        ),
        "categoria": "cardiologia",
    },
    {
        "id": "med_007",
        "domanda": "Come si previene l'osteoporosi?",
        "risposta": (
            "Per prevenire l'osteoporosi: assumere adeguato calcio (latticini, "
            "legumi, verdure a foglia verde), vitamina D (esposizione solare "
            "moderata o integratori), esercizio fisico con carico (camminata, "
            "ballo), evitare fumo e alcol eccessivo. Gli esami di densitometria "
            "ossea (MOC/DEXA) sono consigliati dopo i 65 anni o in caso di "
            "fattori di rischio."
        ),
        "categoria": "ortopedia",
    },
    {
        "id": "med_008",
        "domanda": "Quali esami fare per controllare la tiroide?",
        "risposta": (
            "Per valutare la funzione tiroidea si eseguono: TSH (esame principale "
            "di screening), FT3 e FT4 (ormoni tiroidei liberi), anticorpi anti-TPO "
            "e anti-tireoglobulina in caso di sospetta tiroidite autoimmune. "
            "L'ecografia tiroidea valuta la struttura ghiandolare. I sintomi "
            "di disfunzione includono stanchezza, variazioni di peso, intolleranza "
            "al caldo/freddo, alterazioni del ritmo cardiaco."
        ),
        "categoria": "endocrinologia",
    },
    {
        "id": "med_009",
        "domanda": "Come si gestisce l'ansia?",
        "risposta": (
            "L'ansia si gestisce con: tecniche di respirazione diaframmatica, "
            "mindfulness e meditazione, attività fisica regolare che riduce "
            "il cortisolo, limitare caffeina e alcol, mantenere routine regolari "
            "di sonno. La psicoterapia cognitivo-comportamentale (CBT) è il "
            "trattamento psicologico più efficace. Nei casi gravi il medico può "
            "prescrivere ansiolitici o antidepressivi SSRI."
        ),
        "categoria": "psicologia",
    },
    {
        "id": "med_010",
        "domanda": "Quali sono i sintomi di una psoriasi?",
        "risposta": (
            "La psoriasi si manifesta con: placche rosse coperte da squame "
            "argentee, prurito, pelle secca e screpolata, unghie ispessite o "
            "con fossette. Colpisce più frequentemente gomiti, ginocchia, cuoio "
            "capelluto e zona lombare. Il trattamento include: emollienti, "
            "cortisonici topici, vitamina D topica, fototerapia e nei casi "
            "gravi farmaci biologici."
        ),
        "categoria": "dermatologia",
    },
]