# Security Documentation

## 1. Secrets Management

### 1.1 Architecture

All secrets managed via **OpenBao** (open-source fork of HashiCorp Vault).

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  OpenBao     │◄────│  Service     │────►│  Audit Log   │
│  (Raft HA)   │     │  AppRole     │     │  (File/Syslog)│
└──────┬───────┘     └──────────────┘     └──────────────┘
       │
       ├── secret/llm/vllm          (vLLM API keys)
       ├── secret/llm/openai        (OpenAI-compat keys)
       ├── secret/llm/openrouter    (OpenRouter keys)
       ├── secret/database/qdrant   (Qdrant API keys)
       ├── secret/storage/minio     (MinIO access keys)
       ├── secret/api/app           (Application tokens)
       └── secret/observability/*   (Langfuse, Grafana keys)
```

### 1.2 Secret Provider Abstraction

| Provider | Environment | Use Case |
|----------|-------------|----------|
| `OpenBaoProvider` | Production | All secrets via OpenBao API |
| `EnvProvider` | Development | Environment variables (never in production) |

### 1.3 Bootstrap Process

```bash
# 1. Start OpenBao
docker compose up -d openbao

# 2. Initialize (save unseal keys securely)
docker exec rag-openbao vault operator init \
    -key-shares=3 \
    -key-threshold=2 \
    -format=json > openbao-keys.json

# 3. Unseal (requires 2 of 3 keys)
docker exec rag-openbao vault operator unseal <key-1>
docker exec rag-openbao vault operator unseal <key-2>

# 4. Login
docker exec rag-openbao vault login <root-token>

# 5. Enable KV store
docker exec rag-openbao vault secrets enable -path=secret kv-v2

# 6. Write secrets
docker exec rag-openbao vault kv put secret/llm/vllm api_key=not-needed
docker exec rag-openbao vault kv put secret/api/app token=<generated-token>

# 7. Enable AppRole auth
docker exec rag-openbao vault auth enable approle
```

### 1.4 Secret Rotation

| Secret | Rotation Period | Method |
|--------|----------------|--------|
| LLM API keys | 90 days | Re-write to OpenBao, restart services |
| Database credentials | 90 days | Re-write to OpenBao, rotate in Qdrant |
| Application tokens | 30 days | Issue new token, deprecate old |
| TLS certificates | 30 days | Auto-renew via PKI engine |

### 1.5 Access Control

```hcl
# App policy - read-only access to app secrets
path "secret/data/llm/*" {
  capabilities = ["read", "list"]
}
path "secret/data/database/*" {
  capabilities = ["read", "list"]
}
path "secret/data/api/*" {
  capabilities = ["read", "list"]
}

# Admin policy - full access
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
```

### 1.6 Audit Logging

OpenBao audit logs all secret access:

```
- Timestamp
- Client IP
- Auth type (AppRole, token)
- Path accessed
- Operation type (read, write, delete)
- Allowed/Denied
```

## 2. Network Security

### 2.1 Traffic Encryption

| Path | Protocol | Certificate |
|------|----------|-------------|
| User → API | HTTPS (TLS 1.3) | Let's Encrypt / self-signed |
| API → Qdrant | gRPC + mTLS | OpenBao PKI |
| API → MinIO | HTTPS (S3 over TLS) | OpenBao PKI |
| API → OpenBao | HTTPS | OpenBao self-signed |
| Internal services | mTLS | OpenBao PKI |

### 2.2 Network Zones

| Zone | Networks | Access |
|------|----------|--------|
| DMZ | Public | API endpoints (port 8000) |
| Application | 172.20.0.0/24 | Service-to-service |
| Data | 172.20.1.0/24 | Qdrant, MinIO, OpenBao |
| GPU | 172.20.2.0/24 | vLLM instances |
| Observability | 172.20.3.0/24 | Prometheus, Grafana, Langfuse |

## 3. Container Security

### 3.1 Image Hardening

- Non-root user (`rag` with UID/GID 1000)
- Read-only root filesystem
- Dropped Linux capabilities
- No shell in production images
- Image vulnerability scanning (Trivy)
- SBOM generation per image

### 3.2 Runtime Security

- No privileged containers
- Resource limits (CPU, memory)
- Read-only volume mounts where possible
- Seccomp profile (default)
- AppArmor/SELinux (if available)

## 4. API Security

### 4.1 Authentication

- Bearer token in `Authorization` header
- Token issued by platform auth service
- Token stored in OpenBao
- Token lifetime: 24 hours (configurable)

### 4.2 Rate Limiting

| Endpoint | Rate Limit |
|----------|-----------|
| POST /query | 60 requests/min per tenant |
| POST /ingest | 10 requests/min (large payloads) |
| All endpoints | 1000 requests/min per IP |

### 4.3 Input Validation

- Content-type validation
- File extension whitelist (.pdf, .docx, .txt, .md)
- Max file size: 100MB
- Max request body: 200MB
- Guardrail checks for injection/PII/toxicity

## 5. Data Protection

### 5.1 Encryption at Rest

| Component | Method |
|-----------|--------|
| Qdrant | Storage encryption (AES-256-GCM) |
| MinIO | SSE-S3 (AES-256) |
| OpenBao | Auto-seal with AWS KMS / transit engine |
| PostgreSQL (Langfuse) | TDE / filesystem encryption |

### 5.2 Encryption in Transit

- TLS 1.3 for all external connections
- mTLS for all internal service communication
- Certificate issued by OpenBao PKI (30-day validity)
- Auto-renewal via cert-manager pattern

## 6. Incident Response

### 6.1 Secret Leak

1. Revoke compromised secret in OpenBao
2. Rotate all services using that secret
3. Audit logs to determine scope
4. Issue new secret
5. Post-mortem

### 6.2 Data Breach

1. Isolate affected components (network policy)
2. Rotate all credentials
3. Restore from clean backup
4. Forensic analysis of audit logs
5. Notify affected parties

### 6.3 DoS Attack

1. Enable rate limiting (if not already)
2. Block offending IPs at network level
3. Scale out API replicas
4. Enable circuit breakers
5. Monitor for recurrence
