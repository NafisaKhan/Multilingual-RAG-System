from rag_core.vector_embedding import VectorDB

class ChunkRetriever:
    def __init__(self, vectorstore_path="vectorstore"):
        self.db = VectorDB()
        self.db.load_index(vectorstore_path)

    def retrieve_chunks(self, query: str, top_k: int = 3) -> list:
        results = self.db.query(query, top_k=top_k)
        
        #Filter out any irrelevant chunks
        filtered_results = [chunk for chunk in results if self.is_relevant(chunk, query)]
        return filtered_results

    def is_relevant(self, chunk, query):
        return True

