from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
import uuid
import json
from api.redis_cli import get_redis
import redis

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
        
@job_bp.route("/jobs/<string:job_id>", methods=["GET"])
def get_job_status(job_id:str)->dict:
    try:
        r = get_redis()
        job_data = r.hget(f"Job:{job_id}", 'data')
        if not job_data:
            return jsonify({
                "error": f"Job {job_id} not found"
            }), 404
        job = json.loads(job_data)
        return jsonify(job), 200
        
    except redis.ConnectionError as e:
        return jsonify({
            "error": "Redis connection failed",
            "message": str(e)
        }), 503

@job_bp.route("/stats", methods=["GET"])
def get_stats():
    try:
        r = get_redis()
        queue_count = r.llen('job_queue')
        jobs_submitted = r.get('metrics:jobs_submitted') or 0
        jobs_completed = r.get('metrics:jobs_completed') or 0
        jobs_failed = r.get('metrics:jobs_failed') or 0

        return jsonify({
            "queue_length": queue_count,
            "total_submitted": jobs_submitted,
            "total_completed": jobs_completed,
            "total_failed": jobs_failed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }), 200
    except redis.ConnectionError as e:
        return jsonify({
            "error": "Redis connection failed",
            "message": str(e)
        }), 503
