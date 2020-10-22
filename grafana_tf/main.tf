provider "grafana" {
  url  = "http://localhost:3000"
  auth = "admin:admin"
}

resource "grafana_data_source" "loki" {
  type = "loki"
  name = "loki"
  url  = "http://loki:3100"
}

resource "grafana_data_source" "prometheus" {
  type = "prometheus"
  name = "prometheus"
  url  = "http://prometheus:9090"
}

resource "grafana_dashboard" "poc" {
  depends_on  = [grafana_data_source.loki, grafana_data_source.prometheus]
  config_json = file("poc_dashboard.json")
}
