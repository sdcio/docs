# Subscription using Prometheus Operator

prerequisites: [install prometheus operator](../../../monitoring/1_prometheus_operator.md)

## Deploy the target metric monitor

Configure the target metric that enables prometheus to scrape metrics from the config-server

```shell
kubectl apply -f - <<EOF
# Prometheus Monitor Service (Metrics)
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  labels:
    app.kubernetes.io/name: config-server
  name: target-metrics-monitor
  namespace: network-system
spec:
  endpoints:
    - interval: 30s
      path: /metrics
      port: targetmetrics # Ensure this is the name of the port that exposes HTTPS metrics
      scheme: https
      bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
      tlsConfig:
        # TODO(user): The option insecureSkipVerify: true is not recommended for production since it disables
        # certificate verification. This poses a significant security risk by making the system vulnerable to
        # man-in-the-middle attacks, where an attacker could intercept and manipulate the communication between
        # Prometheus and the monitored services. This could lead to unauthorized access to sensitive metrics data,
        # compromising the integrity and confidentiality of the information.
        # Please use the following options for secure configurations:
        # caFile: /etc/metrics-certs/ca.crt
        # certFile: /etc/metrics-certs/tls.crt
        # keyFile: /etc/metrics-certs/tls.key
        insecureSkipVerify: true
  selector:
    matchLabels:
      app.kubernetes.io/name: config-server

EOF
```

To verify the scraping works, login to the prometheus web service. We expose the prometheus server using port forwarding.

```shell
kubectl --namespace monitoring port-forward svc/prometheus-operated 9090
```

Navigate to http://localhost:9090 to access the Prometheus interface:

Click on Status, then Targets to see any configured scrape targets.

![Targets](../../../monitoring/prometheus_targets.png "Prometheus Targets")

Navigate to Graph to test metrics collection:

![Graph](../../../monitoring/prometheus_graph.png "Prometheus Graph")

In the Expression box, type `controller_runtime_reconcile_total`, and press ENTER.

## Troublesheeting

In case of trouble here is a link to the [troubleshooting-guide][troubleshooting-guide]

[prometheus-operator]: https://github.com/prometheus-operator/prometheus-operator
[troubleshooting-guide]: https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/troubleshooting.md
