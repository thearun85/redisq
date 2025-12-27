# Benchmarks

## Redis Queue Baseline
Flask API with Redis queue operations (RPUSH, HSET, INCR).

### 1 Worker

| Users | Requests/s | Median | P95  | P99  | Failures |
|-------|-----------|------|--------|------|------|----------|
| 20    | ~54       | 5ms  | 9ms  | 11ms | 0 (0%)   |
| 100   | ~120      | 3ms  | 10ms | 14ms | 0 (0%)   |
| 200   | ~112      | 3ms  | 16ms | 20ms | 0 (0%)   |

### 4 Workers

| Users | Requests/s | Median | P95  | P99  | Failures |
|-------|-----------|--------|------|------|----------|
| 20    | ~55       | 5ms    | 9ms  | 13ms | 0 (0%)   |
| 100   | ~155      | 3ms    | 10ms | 15ms | 0 (0%)   |
| 200   | ~112      | 3ms    | 16ms | 20ms | 0 (0%)   |

### 4 Workers + Redis Pipelining

| Users | Requests/s | Median | P95  | P99  | Failures |
|-------|-----------|--------|------|------|----------|
| 20    | ~41       | 5ms    | 10ms | 17ms | 0 (0%)   |
| 100   | ~121      | 3ms    | 10ms | 16ms | 0 (0%)   |
| 200   | **~198**  | 3ms    | 16ms | 20ms | 0 (0%)   |

### Comparison: 1 worker versus 4 workers

| Users | Metric     | 1 Worker | 4 Workers | Improvement |
|-------|------------|----------|-----------|-------------|
| 20    | Requests/s | 54       | 55        | +2% |
| 20    | Median     | 5ms      | 5ms       | — |
| 20    | P99        | 11ms     | 13ms      | -18% slower |
| 20    | Failures   | 0        | 0         | ✓ |
| 100   | Requests/s | 120      | 155       | **+29%** |
| 100   | Median     | 3ms      | 3ms       | — |
| 100   | P99        | 14ms     | 15ms      | -7% slower |
| 100   | Failures   | 0        | 0         | ✓ |
| 200   | Requests/s | 112      | 112       | **0%** |
| 200   | Median     | 3ms      | 3ms       | — |
| 200   | P99        | 20ms     | 20ms      | — |
| 200   | Failures   | 0        | 0         | ✓ |

### Comparison: Impact of Redis Pipelining (4 Workers)

| Users | Metric     | Without Pipelining | With Pipelining | Change |
|-------|------------|--------------------|-----------------|---------|
| 20    | Requests/s | 55                 | 41              | **-25%** |
| 20    | Median     | 5ms                | 5ms             | — |
| 20    | P99        | 13ms               | 17ms            | -31% slower |
| 100   | Requests/s | 155                | 121             | **-22%** |
| 100   | Median     | 3ms                | 3ms             | — |
| 100   | P99        | 15ms               | 16ms            | -7% slower |
| 200   | Requests/s | 112                | **198**         | **+77%** ✅ |
| 200   | Median     | 3ms                | 3ms             | — |
| 200   | P99        | 20ms               | 20ms            | — |

### Observations: 1 Worker
- **Throughput ceiling**: ~120 req/s at 100 users
- **Degradation at 200**: Peak 270 → sustained 112 req/s
- **Latency stable**: Median 3ms across all loads
- **Perfect reliability**: Zero failures

### Observations: 4 Workers
- **Optimal at 100 users**: 155 req/s sustained, 227 peak
- **No benefit at extremes**: Same as 1 worker at 20 and 200 users
- **I/O bound at 200**: Identical 270 → 112 req/s degradation
- **Perfect reliability**: Zero failures

### Critical Finding
At 200 users, both 1 and 4 workers deliver identical performance (112 req/s), proving the bottleneck is I/O operations, not worker capacity.

### Bottleneck Analysis
- **1 Worker**: CPU-bound by Python GIL at ~120 req/s
- **Redis operations**: 3 per request (RPUSH, HSET, INCR) - pipelining would reduce to 1

### Key Finding
Redis pipelining successfully addresses the I/O bottleneck at high concurrency (200 users), achieving **198 req/s** compared to 112 req/s without pipelining. However, it introduces overhead that reduces performance at lower concurrency levels.

### Test Configuration
- **Load pattern**: 67% POST /jobs, 19% GET /jobs/[id], 13% GET /stats, 1% GET /health
- **User wait time**: between(0.01, 0.05) seconds
- **Test duration**: 60 seconds per test
- **Environment**: Docker containers (Redis + Flask + Gunicorn)

### Raw Data
- [1 Worker Tests](results/v0.1)
- [4 Worker Tests](results/v0.2)
