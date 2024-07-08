from bayesrag.config import DATA_DIR, QDRANT_COLLECTION
from bayesrag.data_loader import load_directory_pdf
from bayesrag.text_splitter import split_texts
from bayesrag.vector_db import create_db, upsert_embeddings
from bayesrag.retriever import get_Relavant_Context
from bayesrag.generator import generate_response,classify_query
from bayesrag.utils import ClassificationResult
from bayesrag.evaluator import evaluate_response

def preRun():
    # Load and split documents
    documents = load_directory_pdf(DATA_DIR)
    text_chunks = split_texts(documents)
    
    # Create vector database and upsert embeddings
    create_db(QDRANT_COLLECTION)
    upsert_embeddings(text_chunks)
    
    print("Pre-run completed successfully.")

def main():

    preRun()
    
    # Example queries and responses
    user_query = input("Enter your query or type 'q' to quit: ")

    while user_query.lower() != "q":
        result = classify_query(user_query)

        if result == ClassificationResult.YES:
            relevant_context = get_Relavant_Context(user_query)

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
