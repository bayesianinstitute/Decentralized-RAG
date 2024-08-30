## Local Decentralized RAG File

This repository houses a demo application for local and decentralized Retrieval Augmented Generation (RAG). The project allows users to interact with both local knowledge bases and contribute to a shared, global knowledge .

### Run in Docker Container

Run all services:
```bash
docker compose up -d
```

Download the model and run the application:
```bash
bash run.sh
```

### Clone and Build

1. Clone the repository:
```bash
git clone https://github.com/bayesianinstitute/Decentralized-RAG
cd Decentralized-RAG 
```

2. Build the package:
```bash
python setup.py sdist bdist_wheel
pip install .
```

### Setting up Qdrant (Vector Database)

1. **Download Qdrant Image:**
   ```bash
   docker pull qdrant/qdrant
   ```

2. **Run Qdrant:**
   ```bash
   docker run -d -p 6333:6333 -p 6334:6334 \
       -v ./qdrant_data:/qdrant/storage \
       qdrant/qdrant
   ```
   This command starts a Qdrant instance and maps the necessary ports. It also mounts a local directory (`qdrant_storage`) to persist the database.

### Dependencies

1. **Ollama:**

   - Download and install Ollama by following the instructions on the official website: [https://ollama.ai/](https://ollama.ai/)

2. **Language Model:**

   - Choose a language model from the Ollama library ([https://ollama.ai/library](https://ollama.ai/library)) or create your own. Make sure to pull the model using the `ollama pull` command. For example, to pull the "llama3:8b" model:

     ```bash
     ollama pull llama3:8b
     ```

3. **Text Embedding Model:**

     ```bash
     ollama pull nomic-embed-text:latest
     ```

4. **Other Python Libraries:**
   - Install any other required Python libraries, likely including:
     * `qdrant-client` (to interact with Qdrant)

### Running the Application

1. **Configure Node Type:**
   - Modify the `main.py` file to specify the desired node type:  
     * `admin`: Institute Node (manages the global embedding)
     * `data`: Data Node (contributes specialized knowledge) 

2. **Start the Application:**
   ```bash
   python main.py --data-dir data --nodetype admin
   ```
   - Replace `data` with your desired data directory.
   - Set `--nodetype` to either `admin` or `data`.

## References

Ollama Docker hub: [https://hub.docker.com/r/ollama/ollama](https://hub.docker.com/r/ollama/ollama)
