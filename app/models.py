from .core import db


class Paziente(db.Model):
    __tablename__ = "pazienti"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    cognome = db.Column(db.String(80))


class Medico(db.Model):
    __tablename__ = "medici"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    cognome = db.Column(db.String(80))
    specializzazione = db.Column(db.String(100))


class Appuntamento(db.Model):
    __tablename__ = "appuntamenti"

    id = db.Column(db.Integer, primary_key=True)
    paziente_id = db.Column(db.Integer)
    medico_id = db.Column(db.Integer)
    data_ora = db.Column(db.DateTime)
    durata_minuti = db.Column(db.Integer)
    note = db.Column(db.Text)
    stato = db.Column(db.String(20))


class ChatSessione(db.Model):
    __tablename__ = "chat_sessioni"

    id = db.Column(db.Integer, primary_key=True)
    paziente_id = db.Column(db.Integer)


class ChatMessaggio(db.Model):
    __tablename__ = "chat_messaggi"

    id = db.Column(db.Integer, primary_key=True)
    sessione_id = db.Column(db.Integer)
    ruolo = db.Column(db.String(20))
    contenuto = db.Column(db.Text)