from flask import Blueprint, jsonify
import time
import chromadb

bp = Blueprint("health", __name__)

# Track uptime
start_time = time.time()

# Track response times
response_times = []

def record_response_time(t):
    response_times.append(t)
    if len(response_times) > 10:
        response_times.pop(0)

def get_avg_response_time():
    if not response_times:
        return 0
    return round(sum(response_times) / len(response_times), 3)


@bp.route("/health", methods=["GET"])
def health():
    try:
        # ChromaDB count
        client = chromadb.PersistentClient(path="./chroma_data")
        collection = client.get_or_create_collection(name="risk_docs")
        count = collection.count()

        # Uptime
        uptime = round(time.time() - start_time, 2)

        return jsonify({
            "model": "llama-3.3-70b-versatile",
            "avg_response_time": get_avg_response_time(),
            "chroma_docs": count,
            "uptime_seconds": uptime,
            "cache": "not implemented"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500