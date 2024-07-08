import streamlit as st
from bayesrag.config import DATA_DIR, QDRANT_COLLECTION
from bayesrag.data_loader import load_directory_pdf
from bayesrag.text_splitter import split_texts
from bayesrag.vector_db import create_db, upsert_embeddings
from bayesrag.retriever import get_Relavant_Context
from bayesrag.generator import generate_response

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

def main():
    st.title("Lawyer-Based Chatbot")

    # Sidebar for file upload
    st.sidebar.title("Upload Document")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        with open(DATA_DIR / uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Load and split documents
        documents = load_directory_pdf(DATA_DIR)
        text_chunks = split_texts(documents)

        # Create vector database and upsert embeddings
        create_db(QDRANT_COLLECTION)
        upsert_embeddings(text_chunks)

        st.sidebar.success("Document uploaded and processed successfully!")

    st.header("Chat with your documents")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        result,_ = get_Relavant_Context(user_input)

        with st.chat_message("assistant"):
            response_container = st.empty()
            response_text = ""
            for response_part in generate_response(user_input, result):
                response_text += response_part
                response_container.markdown(response_text)
        
        st.session_state.messages.append({"role": "assistant", "content": response_text})

if __name__ == "__main__":
    main()
