import threading
import uuid
import time
from flask import Blueprint, request, jsonify
from services.job_store import create_job, update_job, get_job

bp = Blueprint("generate_report", __name__)


def generate_report_task(job_id, data):
    time.sleep(5)  # simulate heavy work

    result = {
        "report": f"Generated report for {data}"
    }

    update_job(job_id, result)


@bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.json.get("input")

    job_id = str(uuid.uuid4())
    create_job(job_id)

    thread = threading.Thread(
        target=generate_report_task,
        args=(job_id, data)
    )
    thread.start()

    return jsonify({
        "job_id": job_id,
        "status": "processing"
    })


@bp.route("/job/<job_id>", methods=["GET"])
def get_status(job_id):
    job = get_job(job_id)

    if not job:
        return jsonify({"error": "Job not found"}), 404

    return jsonify(job)