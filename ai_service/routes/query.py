import time
from flask import Blueprint, request, jsonify
from services.groq_client import get_groq_response
import chromadb
from sentence_transformers import SentenceTransformer
from routes.health import record_response_time

bp = Blueprint("query", __name__)

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="risk_docs")


@bp.route("/query", methods=["POST"])
def query():
    start = time.time()  

    data = request.json
    question = data.get("question")
    
    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        # Step 1: Convert question to embedding
        query_embedding = model.encode([question]).tolist()

        # Step 2: Retrieve top 3 documents
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=3
        )

        docs = results["documents"][0]

        # Step 3: Create context
        context = "\n".join(docs)

        # Step 4: Create prompt
        prompt = f"""
        Answer the question using ONLY the context below.

        Context:
        {context}

        Question:
        {question}

        Return a clear and professional answer.
        """

        # Step 5: Call Groq
        answer = get_groq_response(prompt)

        end = time.time()   
        record_response_time(end - start)   

        # Step 6: Return result
        return jsonify({
            "answer": answer,
            "sources": docs
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500