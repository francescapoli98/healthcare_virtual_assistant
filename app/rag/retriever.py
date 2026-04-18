from langchain_core.documents import Document
from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
## data 
from .data__temp import MEDICAL_DOCS

docs = [
    Document(
        page_content=f"{item['domanda']}\n{item['risposta']}",
        metadata={"categoria": item["categoria"], "id": item["id"]}
    )
    for item in MEDICAL_DOCS
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs={"normalize_embeddings": True}
)
db = FAISS.from_documents(docs, embeddings)

def retrieve_context(query):
    docs = db.similarity_search(query, k=3)
    return "\n".join([d.page_content for d in docs])


