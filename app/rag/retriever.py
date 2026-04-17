from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
##data
from data__temp import MEDICAL_DOCS
from langchain.schema import Document

docs = [
    Document(
        page_content=f"{item['domanda']}\n{item['risposta']}",
        metadata={"categoria": item["categoria"], "id": item["id"]}
    )
    for item in MEDICAL_DOCS
]

embeddings = HuggingFaceEmbeddings()

db = FAISS.from_documents(docs, embeddings)

def retrieve_context(query):
    docs = db.similarity_search(query, k=3)
    return "\n".join([d.page_content for d in docs])