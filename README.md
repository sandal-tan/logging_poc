# Stuff

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

[These][1] instructions can be followed, the URL should be `http://loki:3100` for docker compose.

Alternatively, Grafana can be orchestrated with terraform; the following will setup Grafana to talk to Loki:

```
cd grafana_tf/
terraform init
terraform apply
```

As a source of logs, you can use `sample_tool`, which was written to test some logging scenarios:

```
pip install ./sample_tool
st work
```

Loki works on Labels. Labels are defined under the `scrape_configs` key of the promtail config file. Here is some good
reading:

- https://grafana.com/blog/2020/04/21/how-labels-in-loki-can-make-log-queries-faster-and-easier/
- https://grafana.com/blog/2020/08/27/the-concise-guide-to-labels-in-loki/

[1](https://grafana.com/docs/loki/latest/getting-started/grafana/)
