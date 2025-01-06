# Decentralized Retrieval-Augmented Generation (DRAG)

![DRAG](./doc/drags.JPG)
This repository presents a decentralized extension of Retrieval-Augmented Generation (RAG), addressing privacy, scalability, and security issues of traditional RAG systems using IPFS, MQTT, and blockchain. DRAG enables users to interact with local knowledge bases and contribute to a global, shared database, promoting knowledge democratization and incentivizing participation.

## DRAG Overview

DRAG improves RAG by decentralizing storage, communication, and processing, ensuring:

- **Privacy**: Secure, decentralized data storage with IPFS.
- **Scalability**: Global knowledge contributions without central authority.
- **Security**: Blockchain for transparency and safe record-keeping, with rewards for contributors.
- **Collaborative Learning**: Continuous improvement from distributed nodes.

### Key Technologies:
- **IPFS** for decentralized storage.
- **MQTT** for low-latency communication.
- **Blockchain** for secure record-keeping.
- **Qdrant** for vector database storage and retrieval.



## Traditional RAG vs. DRAG

The main difference between traditional RAG and DRAG is the decentralization. In DRAG, multiple nodes contribute knowledge, while traditional RAG relies on a centralized approach. Below is a visual comparison:

![Traditional RAG](./doc/rag.png)
*Traditional RAG: Centralized architecture with a single knowledge base.*

![DRAG](./doc/drags.JPG)
*DRAG: Decentralized architecture with multiple nodes contributing to a global knowledge base.*

## Architecture

The system consists of two types of nodes:

1. **Data Nodes**: Provide domain-specific knowledge to the global vector database.
2. **Evaluator Nodes**: Verify contributions and ensure the integrity of the global database.

The framework incorporates a **blockchain-based reward system** that incentivizes nodes for their contributions, improving both system accuracy and knowledge sharing.

## Setup and Installation

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

### Running in Docker Container

Run all services:
```bash
docker compose up -d
```

Download the model and start the application:
```bash
bash run.sh
```

### Setting up Qdrant (Vector Database)

1. **Download Qdrant Image**:
   ```bash
   docker pull qdrant/qdrant
   ```

2. **Run Qdrant**:
   ```bash
   docker run -d -p 6333:6333 -p 6334:6334 \
       -v ./qdrant_data:/qdrant/storage \
       qdrant/qdrant
   ```
   For Windows:
   ```bash
   docker run -d --name qdrant_container -p 6333:6333 -p 6334:6334 \
       -v C:/path/to/qdrant_data:/qdrant/storage \
       qdrant/qdrant:latest
   ```

### Setting up Dependencies

1. **Ollama**: Install Ollama by following the instructions on [Ollama's website](https://ollama.ai/).

2. **Language Model**: Pull a language model from the Ollama library:
   ```bash
   ollama pull llama3:8b
   ```

3. **Text Embedding Model**:
   ```bash
   ollama pull nomic-embed-text:latest
   ```

4. Install required Python libraries (e.g., `qdrant-client`).

### Running the Application

1. **Configure Node Type**:  
   Edit `main.py` to specify the node type:
   - `admin`: Institute Node (manages the global embedding)
   - `data`: Data Node (contributes specialized knowledge)

2. **Start the Application**:
   ```bash
   python main.py --data-dir data --nodetype admin
   ```

   Replace `data` with the desired data directory. Set `--nodetype` to either `admin` or `data`.

### IPFS Installation

To set up IPFS for decentralized storage, follow the installation instructions from [IPFS Documentation](https://docs.ipfs.tech/install/command-line/#system-requirements) or use the following commands for Windows:

```bash
wget https://dist.ipfs.tech/kubo/v0.23.0/kubo_v0.23.0_windows-amd64.zip -Outfile kubo_v0.23.0.zip
Expand-Archive -Path kubo_v0.23.0.zip -DestinationPath .\kubo
cd .\kubo
.\install.bat
```

## Conclusion

This framework showcases the potential of decentralized systems in enhancing RAG applications by reducing retrieval errors, preserving privacy, and fostering continuous, collaborative learning. By leveraging blockchain technology, it ensures secure and transparent record-keeping, while rewarding participants for their contributions. For a complete implementation, visit our GitHub repository: [Decentralized RAG GitHub](https://github.com/bayesianinstitute/Decentralized-RAG).

## References

- Ollama Docker Hub: [https://hub.docker.com/r/ollama/ollama](https://hub.docker.com/r/ollama/ollama)
- IPFS Documentation: [https://docs.ipfs.tech](https://docs.ipfs.tech)

