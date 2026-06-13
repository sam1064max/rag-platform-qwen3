#!/bin/sh
# MinIO configuration script
# Called by minio-init container
mc alias set ragminio http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}
mc mb ragminio/documents --ignore-existing
mc mb ragminio/backups --ignore-existing
mc mb ragminio/snapshots --ignore-existing
mc policy set download ragminio/documents
