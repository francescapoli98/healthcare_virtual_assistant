from langchain_core.documents import Document
from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from .data.medquad_loader import load_medquad
from .data.mimic_loader import load_mimic

# Lazy: inizializzati solo alla prima chiamata
_embeddings  = None
_medquad_db  = None
_mimic_db    = None


def _get_dbs():
    global _embeddings, _medquad_db, _mimic_db

    if _medquad_db is not None:
        return _medquad_db, _mimic_db   # già pronti

    print("[RAG] Caricamento embeddings e indici FAISS...")

    _embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )

    medquad_docs = [
        Document(page_content=item["text"], metadata={"source": item["source"]})
        for item in load_medquad()
    ]
    mimic_docs = [
        Document(page_content=item["text"], metadata={"source": item["source"]})
        for item in load_mimic(base_path="data/mimiciii-demo/1.4")
    ]

    _medquad_db = FAISS.from_documents(medquad_docs, _embeddings)
    _mimic_db   = FAISS.from_documents(mimic_docs,   _embeddings)

    print("[RAG] Indici pronti.")
    return _medquad_db, _mimic_db


def reciprocal_rank_fusion(results_lists: list[list[Document]], k: int = 60) -> list[Document]:
    scores: dict[str, float] = {}
    doc_map: dict[str, Document] = {}

    for results in results_lists:
        for rank, doc in enumerate(results):
            key = doc.page_content[:120]
            scores[key] = scores.get(key, 0) + 1 / (k + rank + 1)
            doc_map[key] = doc

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [doc_map[key] for key, _ in ranked]


def retrieve_context(query: str, top_k: int = 4) -> str:
    medquad_db, mimic_db = _get_dbs()

    medquad_results = medquad_db.similarity_search(query, k=top_k)