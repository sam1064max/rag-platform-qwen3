#!/bin/bash
# RAG Platform Backup Script
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/tmp/rag-backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="${BACKUP_DIR}/${TIMESTAMP}"
MINIO_ALIAS="ragminio"

echo "=== RAG Platform Backup: ${TIMESTAMP} ==="

mkdir -p "${BACKUP_PATH}"

# Qdrant snapshot
echo "Backing up Qdrant..."
curl -X POST "http://localhost:6333/collections/documents/snapshots" || echo "Qdrant snapshot failed"

# MinIO backup (via mc)
echo "Backing up MinIO..."
mc alias set ${MINIO_ALIAS} http://localhost:9000 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"
mc mirror ${MINIO_ALIAS}/documents "${BACKUP_PATH}/minio-documents"

# OpenBao snapshot
echo "Backing up OpenBao..."
curl -H "X-Vault-Token: ${OPENBAO_TOKEN}" \
    -X PUT "http://localhost:8200/v1/sys/storage/raft/snapshot" \
    -o "${BACKUP_PATH}/openbao.snap"

# Langfuse DB
echo "Backing up Langfuse DB..."
docker exec rag-langfuse-db pg_dump -U langfuse langfuse > "${BACKUP_PATH}/langfuse-db.sql"

echo "Backup complete: ${BACKUP_PATH}"
echo "Uploading to MinIO..."
mc cp --recursive "${BACKUP_PATH}" ${MINIO_ALIAS}/backups/

echo "=== Backup finished ==="
