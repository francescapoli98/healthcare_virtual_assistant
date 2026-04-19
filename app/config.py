import os

class Config:
    SECRET_KEY = "la-tua-chiave-generata"
    ## mysql db
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/gestione_appuntamenti"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ## gemini AI API
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AQ.Ab8RN6L2xbxlh0wt8dQQf4TONBuhZCf_ErbRZ8d5KECZC5CKDw")
     ## huggingface
    HF_TOKEN = os.getenv("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")