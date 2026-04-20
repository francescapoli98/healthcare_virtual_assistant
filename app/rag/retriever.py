import os
from langchain_core.documents import Document
from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from .data.medquad_loader import load_medquad
from .data.mimic_loader import load_mimic

FAISS_DIR = "faiss_index"


class RAGEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance._embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",  # più veloce
                encode_kwargs={"normalize_embeddings": True}
            )

            # cls._instance._embeddings = HuggingFaceEmbeddings(
            #     model_name="BAAI/bge-base-en-v1.5",
            #     encode_kwargs={"normalize_embeddings": True}
            # )

            cls._instance._medquad_db = None
            cls._instance._mimic_db = None

            cls._instance._load_indexes()

        return cls._instance

    # -----------------------------
    # LOAD INDEX UNA SOLA VOLTA
    # -----------------------------
    def _load_indexes(self):
        medquad_path = os.path.join(FAISS_DIR, "medquad")
        mimic_path   = os.path.join(FAISS_DIR, "mimic")

        print("[RAG] Loading FAISS indexes ONLY...")

        self._medquad_db = FAISS.load_local(
            medquad_path,
            self._embeddings,
            allow_dangerous_deserialization=True
        )

        self._mimic_db = FAISS.load_local(
            mimic_path,
            self._embeddings,
            allow_dangerous_deserialization=True
        )

        print("[RAG] Ready ✔")

    # -----------------------------
    # RETRIEVAL
    # -----------------------------
    def retrieve(self, query: str, top_k: int = 6):
        medquad_results = self._medquad_db.similarity_search(query, k=top_k)
        mimic_results   = self._mimic_db.similarity_search(query, k=top_k)

        fused = self._fusion(medquad_results, mimic_results)
        selected = fused[:top_k]

        context = "\n\n".join(
            f"[{doc.metadata.get('source','?')}]\n{doc.page_content}"
            for doc in selected
        )

        return {
            "context": context,
            "has_clinical_cases": any(
                d.metadata.get("source", "").startswith("asclepius")
                for d in selected
            )
        }

    # -----------------------------
    # SIMPLE FUSION
    # -----------------------------
    def _fusion(self, a, b):
        seen = set()
        out = []

        for doc in a + b:
            key = doc.page_content[:120]
            if key not in seen:
                seen.add(key)
                out.append(doc)

        return out


# -----------------------------
# PUBLIC FUNCTION (COMPATIBILITÀ)
# -----------------------------
def retrieve_context(query: str, top_k: int = 6):
    engine = RAGEngine()
    return engine.retrieve(query, top_k)