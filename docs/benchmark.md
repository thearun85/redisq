# Benchmarks

## Redis Queue Baseline
Flask API with Redis queue operations (RPUSH, HSET, INCR).

### 1 Worker

| Users | Requests/s | Peak | Median | P95  | P99  | Failures |
|-------|-----------|------|--------|------|------|----------|
| 20    | ~54       | 67   | 5ms    | 9ms  | 11ms | 0 (0%)   |
| 100   | ~120      | 197  | 3ms    | 10ms | 14ms | 0 (0%)   |

### Observations: 1 Worker
- **Throughput ceiling**: ~120 req/s sustained, ~197 req/s burst
- **Efficiency degradation**: 2.69 req/s per user (20 users) → 1.20 req/s per user (100 users)
- **Latency paradox**: Median latency improves under load (5ms → 3ms) due to connection pooling
- **Perfect reliability**: Zero failures at all load levels

### Bottleneck Analysis
- **1 Worker**: CPU-bound by Python GIL at ~120 req/s
- **Redis operations**: 3 per request (RPUSH, HSET, INCR) - pipelining would reduce to 1

### Next Steps
1. **Redis pipelining**: Batch 3 operations → 1 round trip (est. +30% throughput)
2. **Connection pooling**: Reuse Redis connections (est. +10% throughput)  
3. **Async workers**: Use gevent for I/O concurrency (est. 2-3x throughput)

### Test Configuration
- **Load pattern**: 67% POST /jobs, 19% GET /jobs/[id], 13% GET /stats, 1% GET /health
- **User wait time**: between(0.01, 0.05) seconds
- **Test duration**: 30 seconds per test
- **Environment**: Docker containers (Redis + Flask + Gunicorn)

### Raw Data
- [20 Users, 1 Worker](results/v0.1/test20_stats.csv)
- [100 Users, 1 Worker](results/v0.1/test100_stats.csv)
