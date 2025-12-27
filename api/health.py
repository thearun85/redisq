from flask import Blueprint, jsonify
from datetime import datetime, timezone
from api.redis_cli import get_redis

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=['GET'])
def health_check():
    health_status = {
        "service": "job-queue-api",
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "api": "healthy",
        }
    }

    try:
        r = get_redis()
        r.ping()
        health_status["checks"]["redis"] = "connected"
    except Exception as e:
        heath_status["status"] = "degraded"
        health_status["checks"]["redis"] = "disconnected"
        health_status["checks"]["error"] = str(e)
    status_code = 200 if health_status["status"] == "healthy" else 503
    
    return jsonify(health_status), status_code
