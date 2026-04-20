import os
from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

FAISS_DIR = "faiss_index"


class RAGEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Alternativa più leggera e veloce
            cls._instance._embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                encode_kwargs={"normalize_embeddings": True}
            )

            # Alternativa più accurata ma più lenta
            # cls._instance._embeddings = HuggingFaceEmbeddings(
            #     model_name="BAAI/bge-base-en-v1.5",
            #     encode_kwargs={"normalize_embeddings": True}
            # )

            cls._instance._medquad_db = None
            cls._instance._mimic_db = None

            cls._instance._load_indexes()

        return cls._instance

    # -----------------------------
    # LOAD INDEX (UNA SOLA VOLTA)
    # -----------------------------
    def _load_indexes(self):
        medquad_path = os.path.join(FAISS_DIR, "medquad")
        mimic_path   = os.path.join(FAISS_DIR, "mimic")

        print("[RAG] Loading FAISS indexes...")

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
    # RETRIEVE BASE (COMPAT)
    # -----------------------------
    def retrieve(self, query: str, top_k: int = 6):
        results = self.retrieve_with_scores(query, top_k)

        docs = [doc for doc, _ in results]

        context = "\n\n".join(
            f"[{doc.metadata.get('source','?')}]\n{doc.page_content}"
            for doc in docs
        )

        best_score = results[0][1] if results else 1.0

        return {
            "context": context,
            "confidence": self._score_to_confidence(best_score),
            "has_clinical_cases": any(
                d.metadata.get("source", "").startswith("asclepius")
                for d in docs
            )
        }

    # -----------------------------
    # RETRIEVE CON SCORE 
    # -----------------------------
    def retrieve_with_scores(self, query: str, top_k: int = 6):
        medquad = self._medquad_db.similarity_search_with_score(query, k=top_k)
        mimic   = self._mimic_db.similarity_search_with_score(query, k=top_k)

        fused = self._fusion_with_scores(medquad, mimic)

        return fused[:top_k]

    # -----------------------------
    # FUSION CON SCORE
    # -----------------------------
    def _fusion_with_scores(self, a, b):
        seen = set()
        out = []

        for doc, score in a + b:
            key = doc.page_content[:120]

            if key not in seen:
                seen.add(key)
                out.append((doc, score))

        # ordina per similarità (score più basso = più simile)
        out.sort(key=lambda x: x[1])

        return out

    # -----------------------------
    # SCORE → CONFIDENCE
    # -----------------------------
    def _score_to_confidence(self, score: float) -> float:
        """
        Converte distanza FAISS in confidence (0–1)
        Più score basso → più confidence alta
        """
        confidence = max(0.0, min(1.0, 1 - score))
        return round(confidence, 3)

    # -----------------------------
    # CLASSIFICAZIONE SEMANTICA
    # -----------------------------
    def semantic_filter(self, query: str):
        results = self.retrieve_with_scores(query, top_k=4)

        if not results:
            return "unknown", 0.0

        best_score = results[0][1]
        confidence = self._score_to_confidence(best_score)

        if best_score < 0.4:
            return "medical", confidence
        elif best_score < 0.7:
            return "uncertain", confidence
        else:
            return "non_medical", confidence


# -----------------------------
# PUBLIC API
# -----------------------------
def retrieve_context(query: str, top_k: int = 6):
    engine = RAGEngine()
    return engine.retrieve(query, top_k)


def semantic_check(query: str):
    engine = RAGEngine()
    return engine.semantic_filter(query)