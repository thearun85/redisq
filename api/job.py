from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
import uuid
import json
from api.redis_cli import get_redis

job_bp = Blueprint("jobs", __name__)

@job_bp.route("/jobs", methods=["POST"])
def submit_job():
    data = request.get_json()
    job = {
        'id': str(uuid.uuid4()),
        'type': data.get("type", "default"),
        'payload': data.get("payload", {}),
        'status': "pending",
        'created_at': datetime.now(timezone.utc).isoformat(),
        'attempts': 0,
    }
    try:
        r = get_redis()
        
        r.rpush('job_queue', json.dumps(job))

        r.hset(f"Job:{job['id']}", mapping={
            'data': json.dumps(job),
            'status': 'pending'
        })

        r.incr('metrics:jobs_submitted')

        return jsonify({
            "id": job['id'],
            "status": "pending",
            "message": f"Job: {job['id']} submitted successfully"
        }), 201
    except redis.ConnectionError as e:
        return jsonify({
            "error": "Redis connection failed",
            "message": str(e)
        }), 503
        
