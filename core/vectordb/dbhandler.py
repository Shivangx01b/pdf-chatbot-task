from llama_index.core import VectorStoreIndex,SimpleDirectoryReader

import chromadb
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore





class VectorDbHandler:
    @staticmethod
    def storeindex():

        #Store the index
        print("[+] Storing the pdf in data folder")
        documents = SimpleDirectoryReader("data").load_data()
        db = chromadb.PersistentClient(path="./chroma_db")
        chroma_collection = db.get_or_create_collection("quickstart")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        print("[~] Getting Embeddings")
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )
        print("[+] Index conversion done")

    @staticmethod
    def getindex():

        #Get stored Index
        db = chromadb.PersistentClient(path="./chroma_db")
        chroma_collection = db.get_or_create_collection("quickstart")

        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        index = VectorStoreIndex.from_vector_store(
            vector_store, storage_context=storage_context
        )

        query_engine = index.as_query_engine()
        return query_engine