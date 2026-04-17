from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader

# carica una volta sola
loader = TextLoader("medical_data.txt")
documents = loader.load()

embeddings = HuggingFaceEmbeddings()

db = FAISS.from_documents(documents, embeddings)

def retrieve_context(query):
    docs = db.similarity_search(query, k=3)
    return "\n".join([d.page_content for d in docs])