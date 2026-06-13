storage "raft" {
  path = "/vault/data"
  node_id = "node1"
}

listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = true
}

api_addr = "http://localhost:8200"
cluster_addr = "https://localhost:8201"

ui = true

seal "shamir" {
  secret_shreshold = 2
  total_shares = 3
}

telemetry {
  prometheus_retention_time = "30s"
  disable_hostname = true
}
