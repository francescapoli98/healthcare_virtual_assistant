### $ python -m app.rag.build_index ##da root
from langchain_core.documents import Document
from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from .data.medquad_loader import load_medquad
from .data.mimic_loader import load_mimic

import os

FAISS_DIR = "faiss_index"


def build():
    print("[BUILD] Loading embeddings...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",  # più veloce
        encode_kwargs={"normalize_embeddings": True}
    )
    ### modello medico migliore ma troppo pesante per FAISS
     
    # HuggingFaceEmbeddings(
    #             model_name="BAAI/bge-base-en-v1.5",
    #             encode_kwargs={"normalize_embeddings": True}
    #         )
    
    os.makedirs(FAISS_DIR, exist_ok=True)
    print("[BUILD] Loading documents...")

    medquad_docs = [
        Document(page_content=d["text"], metadata={"source": d["source"]})
        for d in load_medquad()
    ]

    mimic_docs = [
        Document(page_content=d["text"], metadata={"source": d["source"]})
        for d in load_mimic()
    ]

    # Limita a un numero gestibile per FAISS
    medquad_docs = medquad_docs[:3000]
    mimic_docs   = mimic_docs[:3000]

    print(f"[BUILD] MedQuAD: {len(medquad_docs)}")
    print(f"[BUILD] Asclepius: {len(mimic_docs)}")

    print("[BUILD] Creating FAISS... (this is a slow step, be patient)")

    medquad_db = FAISS.from_documents(medquad_docs, embeddings)
    mimic_db   = FAISS.from_documents(mimic_docs, embeddings)

    medquad_db.save_local(os.path.join(FAISS_DIR, "medquad"))
    mimic_db.save_local(os.path.join(FAISS_DIR, "mimic"))

    print("[BUILD] DONE ✔")


if __name__ == "__main__":
    build()