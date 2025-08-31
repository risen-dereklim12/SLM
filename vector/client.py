from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

# memory_size = number_of_vectors * vector_dimension * 4 bytes * 1.5

class VectorClient:
    def __init__(self, collection_name, vector_size, url, distance):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.distance = distance

    def create_collection(self):
        collections = self.client.get_collections().collections
        if any(c.name == self.collection_name for c in collections):
            print(f"Collection '{self.collection_name}' already exists.")
            return
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=self.vector_size, distance=self.distance),
        )
        print(f"Collection '{self.collection_name}' created.")

    def upsert(self, points):
        """
        points: list of PointStruct
        """
        operation_info = self.client.upsert(
            collection_name=self.collection_name,
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
    vector_client = VectorClient("PDPA", 1024, "http://localhost:6333", Distance.DOT)
    
    # vector_client.create_collection()

    from embedding import Embedding
    # import json
    # documents = open("/Users/dlyf/SLM/vector/chunks/pdpa_2012_parts_chunks.jsonl")
    # # documents = documents.readlines()
    # documents = [json.loads(documents) for documents in documents.read().splitlines()]
    embedding = Embedding()
    # points = embedding.embed(documents)
    
    # operation_info = vector_client.upsert(points)
    # print(operation_info)
    
    search_result = vector_client.search(embedding.encode("What is PDPA?")["embeddings"][0], limit=77)
    print(search_result)