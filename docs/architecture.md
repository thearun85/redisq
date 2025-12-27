# redisq - Redis backed Job Queue

## Architecture

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Flask API │────▶│    Redis    │◀────│  Worker(s)  │
│   (Submit)  │     │   (Queue)   │     │  (Process)  │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                    │
       └───────────────────┴────────────────────┘
                           │
                    ┌─────────────┐
                    │  Prometheus │
                    │   Grafana   │
                    └─────────────┘
