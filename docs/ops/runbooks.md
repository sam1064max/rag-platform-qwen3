# Operations Runbooks

## 1. Incident Response

### 1.1 Service Down

1. Check Docker status: `docker ps -a | grep rag-`
2. Check logs: `docker compose logs -f <service>`
3. Restart service: `docker compose restart <service>`
4. If persistent: `docker compose down <service> && docker compose up -d <service>`

### 1.2 GPU Out of Memory

1. Check GPU: `nvidia-smi`
2. Check vLLM logs: `docker compose -f docker/vllm/docker-compose.gpu.yml logs`
3. Reduce `--max-model-len` or `--max-num-seqs`
4. Restart vLLM container

### 1.3 OpenBao Sealed

1. Check status: `docker exec rag-openbao vault status`
2. Unseal: `docker exec rag-openbao vault operator unseal <key>`
3. Requires 2 of 3 keys
4. Verify: `docker exec rag-openbao vault status`

### 1.4 Qdrant Corruption

1. List snapshots: `curl http://localhost:6333/collections/documents/snapshots`
2. Restore latest snapshot
3. Verify: `curl http://localhost:6333/collections/documents`

## 2. Backup Procedures

### 2.1 Automated Backup

```bash
# Run backup script
./scripts/backup.sh

# Schedule with cron (daily at 2 AM)
0 2 * * * /opt/rag-platform/scripts/backup.sh
```

### 2.2 Manual Snapshot

```bash
# Qdrant snapshot
curl -X POST "http://localhost:6333/collections/documents/snapshots"

# MinIO backup
mc mirror ragminio/documents /tmp/backup/documents

# OpenBao snapshot
curl -X PUT "http://localhost:8200/v1/sys/storage/raft/snapshot" \
    -H "X-Vault-Token: $TOKEN" -o /tmp/backup/openbao.snap
```

## 3. Restore Procedures

### 3.1 Full Restore

```bash
./scripts/restore.sh s3://backups/20240101_120000
```

### 3.2 Qdrant Only

```bash
# Upload snapshot to Qdrant
curl -X POST \
    "http://localhost:6333/collections/documents/snapshots/upload" \
    -F "snapshot=@/path/to/snapshot.snapshot"
```

## 4. Upgrade Procedures

### 4.1 Rolling Upgrade

```bash
# 1. Pull new images
docker compose pull

# 2. Upgrade stateless services first
docker compose up -d rag-api

# 3. Upgrade stateful services (one at a time)
docker compose up -d qdrant
docker compose up -d minio

# 4. Verify all services
docker compose ps
```

### 4.2 Model Update

```bash
# 1. Update vLLM image or model
# 2. Restart vLLM services
docker compose -f docker/vllm/docker-compose.gpu.yml up -d
# 3. Verify model loads
curl http://localhost:8012/v1/models
```

## 5. Capacity Planning

| Signal | Threshold | Action |
|--------|-----------|--------|
| Qdrant disk > 70% | 70% | Add storage or cleanup |
| Qdrant query latency > 100ms | 100ms | Add Qdrant node |
| GPU memory > 90% | 90% | Reduce batch size or add GPU |
| API CPU > 70% | 70% | Add API replicas |
| MinIO storage > 80% | 80% | Add storage or archive old data |
