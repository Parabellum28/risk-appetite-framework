from flask import Blueprint, request, jsonify
from services.groq_client import get_groq_response

bp = Blueprint("categorise", __name__)

@bp.route("/categorise", methods=["POST"])
def categorise():
    data = request.json
    text = data.get("text")

    # Step 1: check input
    if not text:
        return jsonify({"error": "Text is required"}), 400

    # Step 2: create prompt
    prompt = f"""
    Classify the following into:
    Low Risk, Medium Risk, High Risk, Critical Risk.

    Return JSON:
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

        # Step 4: return result
        return jsonify(result)

    except Exception as e:
        # Step 5: fallback
        return jsonify({
            "category": "Unknown",
            "confidence": 0.0,
            "reasoning": "Error occurred",
            "error": str(e)
        }), 200