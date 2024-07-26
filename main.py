import argparse
import sys
from bayesrag.data_loader import load_directory_pdf
from bayesrag.text_splitter import split_texts
from bayesrag.vector_db import  VectorDB
from bayesrag.retriever import get_Relavant_Context
from bayesrag.generator import generate_response,classify_query
from bayesrag.utils import ClassificationResult
from bayesrag.evaluator import evaluate_response
import uuid
from loguru import logger

def preRun(DATA_DIR,QDRANT_COLLECTION):
    # Load and split documents
    documents = load_directory_pdf(DATA_DIR)
    text_chunks = split_texts(documents)
    # Create vector database and upsert embeddings
    vectorDb=VectorDB(QDRANT_COLLECTION)
    vectorDb.create_db()
    vectorDb.upsert_embeddings(text_chunks)
    
    logger.info("Pre-run completed successfully.")

def main():
    parser = argparse.ArgumentParser(description="Run the BayesRAG query system.")
    parser.add_argument('--data-dir', type=str, help="Directory containing the PDF documents.")
    args = parser.parse_args()

    from bayesrag.mq import Mqttclient 
    ID=uuid.uuid4()
    REPLAY_TOPIC = f"USER_TOPIC-{ID}"
    QDRANT_COLLECTION=f"law_doc-{ID}"

    client = Mqttclient(replyTopic=REPLAY_TOPIC,collection_name=QDRANT_COLLECTION)

    if args.data_dir:
        preRun(args.data_dir,QDRANT_COLLECTION)
    
    
    # Example queries and responses
    user_query = input("Enter your query or type 'q' to quit: ")

    while user_query.lower() != "q":
        result = classify_query(user_query)

        if result == ClassificationResult.YES:
            relevant_context = get_Relavant_Context(user_query,client,REPLAY_TOPIC,collection_name=QDRANT_COLLECTION)

            print("-" * 100)
        else:
            relevant_context = None

        for text in generate_response(user_query, relevant_context):
            print(text, end=" ")

        user_query = input("\nEnter your query or type 'q' to quit: ")



    # # Evaluation
    # score_df = evaluate_response(user_query, llm_response, result.payload['data'])
    # print(score_df)

if __name__ == "__main__":
    main()
