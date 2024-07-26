## This Local and Decentralized  RAG File

### Clone and Build

Clone the repository and build the package locally:

```bash
python setup.py sdist bdist_wheel
pip install .
```

### Download and Run Qdrant

First, download the latest Qdrant image from Docker Hub:

```bash
docker pull qdrant/qdrant
```

Then, run the Qdrant service:

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

### Download and Install Dependencies

- Download and install **LM Studio**.
- Download the **Llama3 model**.
- Download the **Nomic text embedding model**.

### Run the Application

**CLI App:**

```bash
python main.py
```

**Streamlit App:**

```bash
streamlit run app.py
```

