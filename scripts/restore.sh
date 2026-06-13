#!/bin/bash
# RAG Platform Restore Script
set -euo pipefail

RESTORE_FROM="${1:-}"
if [ -z "${RESTORE_FROM}" ]; then
    echo "Usage: $0 <backup-path>"
    echo "Example: $0 s3://backups/20240101_120000"
    exit 1
fi

echo "=== RAG Platform Restore ==="
echo "Restoring from: ${RESTORE_FROM}"

# Restore Qdrant
echo "Restoring Qdrant..."
# Requires manual snapshot restore via API

# Restore MinIO
echo "Restoring MinIO..."
mc alias set ragminio http://localhost:9000 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"
mc mirror "${RESTORE_FROM}/minio-documents" ragminio/documents

# Restore OpenBao
echo "Restoring OpenBao..."
curl -H "X-Vault-Token: ${OPENBAO_TOKEN}" \
    -X PUT "http://localhost:8200/v1/sys/storage/raft/snapshot" \
    -H "Content-Type: application/octet-stream" \
    --data-binary "@${RESTORE_FROM}/openbao.snap"

# Restore Langfuse DB
echo "Restoring Langfuse DB..."
docker exec -i rag-langfuse-db psql -U langfuse langfuse < "${RESTORE_FROM}/langfuse-db.sql"

echo "=== Restore complete ==="
