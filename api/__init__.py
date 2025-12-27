from flask import Flask, jsonify
from datetime import datetime
from api.redis_cli import init_redis
import os

def create_app():
    flask_app = Flask("job-queue-api")

    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        init_redis(redis_url)
        
    from api.health import health_bp
    flask_app.register_blueprint(health_bp)

    from api.job import job_bp
    flask_app.register_blueprint(job_bp)
    
    return flask_app
