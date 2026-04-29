from flask import Blueprint, request, jsonify
from services.groq_client import get_groq_response
import time
from routes.health import record_response_time  

bp = Blueprint("categorise", __name__)

@bp.route("/categorise", methods=["POST"])
def categorise():
    start = time.time()

    data = request.json
    text = data.get("text")

    # Step 1: check input
    if not text:
        return jsonify({"error": "Text is required"}), 400

    # Step 2: create prompt
    prompt = f"""
    You are a cybersecurity risk analyst.

    Classify the input into:
    Low Risk, Medium Risk, High Risk, Critical Risk.

    Rules:
    - Be precise
    - Give short reasoning
    - Confidence must be realistic (0.0–1.0)

    eturn JSON:
{{
  "category": "...",
  "confidence": 0.0-1.0,
  "reasoning": "..."
}}

    Input: {text}
    """

    try:
        # Step 3: call AI
        result = get_groq_response(prompt)

        end = time.time()
        response_time_ms = round((end - start) * 1000, 2)
        record_response_time(end - start)

        # Step 4: return result
        return jsonify({
            "result": result,
            "sources": [],
            "meta": {
                "confidence": 0.85,
                "model_used": "llama-3.3-70b-versatile",
                "tokens_used": len(prompt.split()),
                "response_time_ms": response_time_ms,
                "cached": False
    }
})

    except Exception as e:
        end = time.time()
        response_time_ms = round((end - start) * 1000, 2)
        record_response_time(end - start)

        return jsonify({
    "category": "Unknown",
    "confidence": 0.0,
    "reasoning": "Error occurred",
    "error": str(e),
    "meta": {
        "confidence": 0.0,
        "model_used": "llama-3.3-70b-versatile",
        "tokens_used": 0,
        "response_time_ms": response_time_ms,
        "cached": False
    }
}), 200