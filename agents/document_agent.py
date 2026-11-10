import os
from docx import Document as DocxDocument
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def load_documents(docx_dir="data/veriler"):
    documents = []
    for filename in os.listdir(docx_dir):
        if filename.endswith(".docx"):
            doc_path = os.path.join(docx_dir, filename)
            doc = DocxDocument(doc_path)
            text = "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])
            documents.append(Document(page_content=text, metadata={"source": filename}))
    return documents

def create_vector_store(documents):
    embeddings = HuggingFaceEmbeddings(model_name="emrecan/bert-base-turkish-cased-mean-nli-stsb-tr")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    all_splits = text_splitter.split_documents(documents)
    vector_store = Chroma(
        collection_name="vectordb",
        embedding_function=embeddings,
        persist_directory="chroma_langchain_db"
    )
    # Her başlatmada aynı parçaların tekrar eklenmesini önle
    if vector_store._collection.count() == 0:
        vector_store.add_documents(all_splits)
    return vector_store

def retrieve_documents(vector_store, question):
    return vector_store.similarity_search(question)
