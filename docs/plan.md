# redisq - Redis Job Queue

## Project Goal
Build a redis-backed job queue from scratch to understand distributed systems concepts, redis patterns and async processing.

## Version 0.1 - Core logic (Synchronous gunicorn)

- [x] Architecture diagram, readme and plan
- [x] Basic Flask health endpoint
- [x] Add Redis connection
- [x] Job submission endpoint
- [x] Job status tracking
- [x] Locust integration and Load testing (1 gunicorn worker and 20/100 users)

## Version 0.2 - Optimization (more workers and pipelining)

- [x] 4 gunicorn workers (synchronous)
- [ ] redis pipelining

## Version 0.3 - Worker Logic and job transitions

- [ ] Single worker implementation
- [ ] Job consumption
- [ ] Job status transitions
- [ ] Graceful shutdown 
