from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

# memory_size = number_of_vectors * vector_dimension * 4 bytes * 1.5

class VectorClient:
    def __init__(self, url):
        self.client = QdrantClient(url=url)

    def create_collection(self, collection_name, vector_size, distance):
        collections = self.client.get_collections().collections
        if any(c.name == collection_name for c in collections):
            print(f"Collection '{collection_name}' already exists.")
            return
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance),
        )
        print(f"Collection '{collection_name}' created.")

    def upsert(self, points, collection_name):
        """
        points: list of PointStruct
        """
        operation_info = self.client.upsert(
            collection_name=collection_name,
            wait=True,
            points=points,
        )
        return operation_info

    def search(self, query_vector, param=None, limit=7):
        must_conditions = []
        if param:
            must_conditions.append(
                FieldCondition(
                    key="section",
                    match=MatchValue(value=param)
                )
            )
        query_filter = Filter(must=must_conditions) if must_conditions else None
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            with_payload=True,
            limit=limit,
        )
        return results

if __name__ == "__main__":
    vector_client = VectorClient("http://localhost:6333")
    
    def create_collection(collection_name, vector_size, distance):
        vector_client.create_collection(collection_name, vector_size, distance)

    def insert_collection(documents_path):
        from embedding import Embedding
        import json
        documents = documents_path
        documents = documents.readlines()
        documents = [json.loads(documents) for documents in documents.read().splitlines()]
        embedding = Embedding()
        points = embedding.embed(documents)
        operation_info = vector_client.upsert(points, "PDPA")
        print(operation_info)
    
    def search(question_vector, limit):
        search_result = vector_client.search(question_vector, limit=limit)
        print(search_result)

    # search(embedding.encode("What is PDPA?")["embeddings"][0], 77)
    # insert_collection(open("/Users/dlyf/SLM/vector/chunks/document_to_be_chunked.jsonl"))
    create_collection("chat_history", 1024, Distance.DOT)