from openai import OpenAI
from bayesrag.config import OPENAI_BASE_URL, OPENAI_API_KEY

client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

def get_embedding(text, model="nomic-ai/nomic-embed-text-v1.5-GGUF"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding
