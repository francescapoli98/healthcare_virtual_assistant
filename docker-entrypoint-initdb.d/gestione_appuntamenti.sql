-- ============================================================
--  DATABASE: gestione_appuntamenti
--  Struttura: medici, pazienti, studi, appuntamenti
-- ============================================================

CREATE DATABASE IF NOT EXISTS gestione_appuntamenti
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE gestione_appuntamenti;

-- ------------------------------------------------------------
--  TABELLA: studi
-- ------------------------------------------------------------
CREATE TABLE studi (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  nome        VARCHAR(120) NOT NULL,
  indirizzo   VARCHAR(200) NOT NULL,
  citta       VARCHAR(80)  NOT NULL,
  telefono    VARCHAR(20)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
--  TABELLA: medici
-- ------------------------------------------------------------
CREATE TABLE medici (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  nome          VARCHAR(80)  NOT NULL,
  cognome       VARCHAR(80)  NOT NULL,
  specializzazione VARCHAR(100),
  studio_id     INT NOT NULL,
  CONSTRAINT fk_medico_studio FOREIGN KEY (studio_id)
    REFERENCES studi(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
--  TABELLA: pazienti
-- ------------------------------------------------------------
CREATE TABLE pazienti (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  nome          VARCHAR(80)  NOT NULL,
  cognome       VARCHAR(80)  NOT NULL,
  data_nascita  DATE,
  telefono      VARCHAR(20),
  email         VARCHAR(120)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
--  TABELLA: appuntamenti
-- ------------------------------------------------------------
CREATE TABLE appuntamenti (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  paziente_id     INT NOT NULL,
  medico_id       INT NOT NULL,
  data_ora        DATETIME NOT NULL,
  durata_minuti   INT DEFAULT 30,
  note            TEXT,
  stato           ENUM('programmato','completato','annullato') DEFAULT 'programmato',
  CONSTRAINT fk_app_paziente FOREIGN KEY (paziente_id)
    REFERENCES pazienti(id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_app_medico FOREIGN KEY (medico_id)
    REFERENCES medici(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
--  Evitare prenotazioni sovrapposte
-- ------------------------------------------------------------
CREATE UNIQUE INDEX idx_unique_medico_slot
ON appuntamenti (medico_id, data_ora);



-- ============================================================
--  DATI 
-- ============================================================

-- 4 Studi medici
INSERT INTO studi (nome, indirizzo, citta, telefono) VALUES
  ('Studio Medico Centrale',   'Via Roma 14',            'Milano',  '02-4521890'),
  ('Poliambulatorio San Luca', 'Corso Vittorio 87',      'Torino',  '011-3378542'),
  ('Studio Dott. Ferretti',    'Viale dei Pini 33',      'Bologna', '051-9987432'),
  ('Centro Salute Adriatico',  'Lungomare Cristoforo 5', 'Rimini',  '0541-778234');

-- 4 Medici (uno per studio)
INSERT INTO medici (nome, cognome, specializzazione, studio_id) VALUES
  ('Marco',     'Bianchi',   'Medicina Generale',  1),
  ('Federica',  'Conti',     'Cardiologia',        2),
  ('Luca',      'Ferretti',  'Ortopedia',          3),
  ('Valentina', 'Moretti',   'Dermatologia',       4);

-- 10 Pazienti
INSERT INTO pazienti (nome, cognome, data_nascita, telefono, email) VALUES
  ('Giovanni',  'Russo',     '1978-03-15', '333-1122334', 'g.russo@email.it'),
  ('Chiara',    'Esposito',  '1990-07-22', '347-5566778', 'c.esposito@email.it'),
  ('Matteo',    'Ricci',     '1965-11-08', '320-9988776', 'm.ricci@email.it'),
  ('Silvia',    'Marino',    '1985-02-28', '348-4433221', 's.marino@email.it'),
  ('Alessandro','Greco',     '1972-09-14', '339-6677889', 'a.greco@email.it'),
  ('Laura',     'Lombardi',  '1995-05-03', '335-2211443', 'l.lombardi@email.it'),
  ('Roberto',   'Gallo',     '1958-12-19', '328-8899001', 'r.gallo@email.it'),
  ('Francesca', 'Mancini',   '1982-08-31', '347-0012345', 'f.mancini@email.it'),
  ('Davide',    'Coppola',   '1993-04-17', '333-5544332', 'd.coppola@email.it'),
  ('Elena',     'Cattaneo',  '1970-01-25', '366-7788990', 'e.cattaneo@email.it');

-- Appuntamenti (2-3 per paziente, distribuiti su tutti i medici)
INSERT INTO appuntamenti (paziente_id, medico_id, data_ora, durata_minuti, note, stato) VALUES
  (1,  1, '2025-06-02 09:00:00', 30, 'Visita di controllo',            'programmato'),
  (1,  3, '2025-06-15 11:30:00', 45, 'Dolore al ginocchio sinistro',   'programmato'),
  (2,  2, '2025-06-03 10:00:00', 45, 'ECG di routine',                 'programmato'),
  (2,  4, '2025-06-20 14:00:00', 30, 'Controllo nei cutanei',          'programmato'),
  (3,  1, '2025-06-04 08:30:00', 30, 'Rinnovo piano terapeutico',      'programmato'),
  (3,  2, '2025-05-20 09:00:00', 60, 'Ecocardiogramma',                'completato'),
  (4,  4, '2025-06-05 15:00:00', 30, 'Acne – follow up',               'programmato'),
  (4,  1, '2025-06-18 08:00:00', 30, 'Certificato medico sportivo',    'programmato'),
  (5,  3, '2025-06-06 10:30:00', 45, 'Post-operatorio spalla destra',  'programmato'),
  (5,  2, '2025-05-28 11:00:00', 45, 'Palpitazioni – prima visita',    'completato'),
  (6,  1, '2025-06-07 09:30:00', 30, 'Influenza ricorrente',           'programmato'),
  (6,  4, '2025-06-22 16:00:00', 30, 'Dermatite atopica',              'programmato'),
  (7,  2, '2025-06-09 08:00:00', 60, 'Holter cardiaco – refertazione', 'programmato'),
  (7,  3, '2025-05-15 10:00:00', 45, 'Protesi anca – controllo',       'completato'),
  (8,  1, '2025-06-10 11:00:00', 30, 'Ipertensione – follow up',       'programmato'),
  (8,  4, '2025-06-25 14:30:00', 30, 'Esame del neo sospetto',         'programmato'),
  (9,  3, '2025-06-11 09:00:00', 45, 'Lombalgia cronica',              'programmato'),
  (9,  1, '2025-04-10 08:30:00', 30, 'Visita urgente – febbre alta',   'completato'),
  (10, 2, '2025-06-12 10:00:00', 45, 'Aritmia – secondo parere',       'programmato'),
  (10, 4, '2025-05-05 15:30:00', 30, 'Psoriasi – inizio terapia',      'completato');

-- Storico conversazioni chat
CREATE TABLE chat_sessioni (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  paziente_id INT NOT NULL,
  creata_il   DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (paziente_id) REFERENCES pazienti(id)
);

CREATE TABLE chat_messaggi (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  sessione_id INT NOT NULL,
  ruolo       ENUM('utente', 'assistente') NOT NULL,
  contenuto   TEXT NOT NULL,
  creato_il   DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sessione_id) REFERENCES chat_sessioni(id)
);



-- ============================================================
--  QUERY DI ESEMPIO UTILI
-- ============================================================

-- 1. Lista completa appuntamenti con nomi medico e paziente
-- SELECT
--   a.id,
--   CONCAT(p.nome, ' ', p.cognome) AS paziente,
--   CONCAT('Dott. ', m.nome, ' ', m.cognome) AS medico,
--   m.specializzazione,
--   a.data_ora,
--   a.durata_minuti,
--   s.indirizzo,
--   s.citta,
--   a.stato
-- FROM appuntamenti a
-- JOIN pazienti  p ON a.paziente_id = p.id
-- JOIN medici    m ON a.medico_id   = m.id
-- JOIN studi     s ON m.studio_id   = s.id
-- ORDER BY a.data_ora;

-- 2. Appuntamenti di un paziente specifico
-- SELECT ... FROM appuntamenti a JOIN ... WHERE p.cognome = 'Russo';

-- 3. Agenda giornaliera di un medico
-- SELECT ... WHERE m.cognome = 'Bianchi' AND DATE(a.data_ora) = '2025-06-02';
