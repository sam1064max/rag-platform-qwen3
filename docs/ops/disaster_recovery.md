# Disaster Recovery Plan

## 1. Recovery Objectives

| Metric | Target |
|--------|--------|
| RTO (Recovery Time Objective) | < 1 hour |
| RPO (Recovery Point Objective) | < 15 minutes |

## 2. Failure Scenarios

### 2.1 Single Service Failure

**Impact:** Partial system degradation

**Response:**
1. Restart service: `docker compose restart <service>`
2. Check logs: `docker compose logs -f --tail=100 <service>`
3. If restart fails, check resource limits and configuration

### 2.2 Node Failure

**Impact:** Service unavailable

**Response:**
1. Provision replacement node
2. Install Docker and NVIDIA Container Toolkit
3. Restore from backup (see restore procedures)
4. Verify data integrity
5. Update DNS/load balancer

### 2.3 Full Site Failure

**Impact:** Complete system outage

**Response:**
1. Provision new infrastructure (VPS, bare metal)
2. Deploy Docker Compose stack
3. Restore OpenBao from Raft snapshot
4. Restore MinIO data from remote backup
5. Restore Qdrant from snapshot
6. Start vLLM services and load models
7. Verify end-to-end query flow

## 3. Backup Locations

| Data | Primary | Secondary |
|------|---------|-----------|
| Qdrant snapshots | MinIO (local) | Remote site |
| MinIO data | Local storage | Remote site (replication) |
| OpenBao | Raft (HA cluster) | MinIO snapshot |
| Config | Git (Gitea) | GitHub mirror |

## 4. Recovery Verification

After every restore:
1. Run health checks: `curl http://localhost:8000/api/v1/health`
2. Run test query: `curl -X POST http://localhost:8000/api/v1/query`
3. Verify document count
4. Run evaluation suite
