provider "grafana" {
  url = "http://localhost:3000"
  auth = "admin:admin"
}

resource "grafana_data_source" "loki" {
  type = "loki"
  name = "loki"
  url = "http://loki:3100"
}
