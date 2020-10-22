# Stack

This POC is done using [Grafana](1), [Loki+Promtail](2), and [Prometheus](3). Each is used for the following:

- `Promtail`: Client side log aggregation, deployed to host. Configures scraping and etl of logs
- `Prometheus`: Label-based metric aggregation service
- `Loki`: Label-baed log aggregation service
- `Grafana`: Overall data aggregation, visualization, and alerting.

Promtail would be deployed wherever logs would need to be aggregated from. It's deployment is flexible, with support for
helm, EKS, and more. As part of the deployment, the log source, metrics, and labels would be declared. Metrics are
extracted as part of the log ETL (usually by regex). The labels declared here are used by Loki and Prometheus and serve
as indexes for queries in the respective system. Labels can be defined statically or dynamically. A static label would
be one defined in the configuration file itself, and would specify environment, application, etc. A dynamic label is
declared in the configuration, but the value is pulled from a log message during ETL. It is advisable to minimize the
cardinality of the dynamic label sets as parsing stream is opened for the superset of label combinations across ALL
labels. Once ingested, Promtail will send post about relevant metrics on `/metrics` and push the parsed logs to Loki.

Loki acts as a data store for the aggregated logs, facilitating querying and viewing of logs. Prometheus pulls metrics
from Promtail via `/metrics`. From there, it fulfills a similar duty to Loki, but for metrics.

Grafana uses Loki and Prometheus as data sources, from which visualization and alerts are built.

Here is some good reading:

- https://grafana.com/blog/2020/04/21/how-labels-in-loki-can-make-log-queries-faster-and-easier/
- https://grafana.com/blog/2020/08/27/the-concise-guide-to-labels-in-loki/

# Goal

Build a simple application that logs. Standup a Grafana-Loki-Promtail-Prometheus stack to build dashboard and alerting.

The dashboard should display the following information:

- Average time it takes to find a number (requires special log message)
- The total number of inputs (promtail metric)
- The total number of requests (promtail metric)
- The average input size (combinations of total number of inputs/total number of requests)
- % of requests for parallel work (loki metric)

We should also alarm for:

- High volume of errors

# Instructions

To run the full stack locally:

```
docker-compose -f docker-compose.yaml up
```

You can access the gui with:

```
open http://localhost:3000
```

If you have not logged in before, you can login with:

- Username: `admin`
- Password: `admin`

You will be prompted to change the password, which you can skip.

Grafana can be orchestrated with terraform; the following will setup Grafana to talk to Loki:

```
cd grafana_tf/
terraform init
terraform apply
```

Alternatively, [These](4) instructions can be followed, the URL should be `http://loki:3100` for docker compose.

As a source of logs, you can use `sample_tool`, which was written to test some logging scenarios. It's goal to is expose
common situations for logging (parent-child process relationship and entry point setup), while providing actionable log
messages. The tool can be installed and used like this:

```
pip install ./sample_tool
st work 5 10 # Lower bound of 0, can raise a DivisionByZero error
st work 14 53 6 -l 1 # This should always be fine, so long as numbers are within the bounds

# Execute a bunch in parallel
st work $(python -c 'import random " ".join(random.randint(1, 9999) for _ in range(random.randint(1, 20)))') --parallel

# Use helper script to automate
bash keep_alive.sh
```

To get a feel for Grafana, use `keep_alive.sh` to get some logs going. After you've got in running go [here](5) to view
the dashboard.

[1](https://github.com/grafana/grafana) [2](https://github.com/grafana/loki)
[3](https://gthub.com/prometheus/prometheus) [4](https://grafana.com/docs/loki/latest/getting-started/grafana/)
[5](http://localhost:3000/d/4NeYOdtMk/poc-dashboard?orgId=1&refresh=5s)
