import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent Chroma databaseS
client = chromadb.PersistentClient(path="./chroma_data")

# Create/get collection
collection = client.get_or_create_collection(name="risk_docs")

# Sample documents
docs = [
    "High-risk assets require stronger controls.",
    "Low-risk assets need standard monitoring.",
    "Risk appetite defines acceptable exposure."
]

# Create embeddings
embeddings = model.encode(docs).tolist()

# Store in Chroma
collection.add(
    documents=docs,
    embeddings=embeddings,
    ids=["1","2","3"]
)

# Test query
question = "What applies to high-risk assets?"
query_embedding = model.encode([question]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

print(results["documents"])