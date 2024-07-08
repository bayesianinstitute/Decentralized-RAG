## This Local Rag File


Download and run
First, download the latest Qdrant image from Dockerhub:

```bash
docker pull qdrant/qdrant
```
Then, run the service:
```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

Download and Install Lm Studio also download llama3 model and nomic text embedding model

#### Run APP

CLI APP : 
```bash
python main.py
```

Streamlit APP :
```bash
streamlit run app.py
```
