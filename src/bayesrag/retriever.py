from bayesrag.embedder import get_embedding
from bayesrag.vector_db import qclient
from bayesrag.config import QDRANT_COLLECTION

# from bayesrag.communication.mq import Mqttclient
# from bayesrag.constant import SEND_TOPIC


# client=Mqttclient()
ID="Node1"
REPLAY_TOPIC=f"USER_TOPIC {ID}"

def get_Relavant_Context(query):
    query_embedding = get_embedding(query)
    results = qclient.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_embedding,
        limit=1,
    )
    print("Score : ",results[0].score)
    if results[0].score <0.60:
        data={
            "replay_topic": REPLAY_TOPIC,
            "query": query,
        }
        ## TODO: send request to other node to get relvant information
        # client.send_message(SEND_TOPIC,data)
        print("No relevant context found in local VectorDB")
        return None  # TODO: return appropriate message or None for no relevant context found in local VectorDB  # TODO: send request to other node to get relvant information
    
    else:
        print("Found in local VectorDb")
        return results[0].payload["data"],results[0].score

if __name__ == '__main__':
    query = "hey how are you?"
    relevant_context = get_Relavant_Context(query)
    print(f"Relevant context: {relevant_context}")