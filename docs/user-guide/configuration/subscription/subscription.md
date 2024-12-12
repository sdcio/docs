# Subscription

Subscription defines the subscription to collect metrics from the devices and export them using prometheus.

Future:

- other export mechanims (Influx, Kafka, NATS, etc)
- abstractions/vendor agnostic subcriptions
- output transformers/event handlers


## Attributes

* `target`: 
    * `targetSelector`: A label selector that selects which targets this subscription should apply to
* `protocol`: the protocol used to collect the data (gnmi, others TBD)
* `port`: The default TCP port for gNMI sessions is `57400`.
* `encoding`: Specifies the encoding format for gNMI (`ASCII`, `PROTO`).
* `subscriptions`: Specifies the subscription details (list)
    * `name`: name of the subscription
    * `description`: a description for the description
    * `adminState`: detrmines if the subscription is `enabled` or `disabled`
    * `mode`: defines the subscription mode (`onChange`, `sample`)
    * `interval`: defines the interval for sampled subscriptions (`1s`, `15s`, `30s`, `60s`)
    * `paths`: define the subscription paths

## Example

```yaml
--8<--
config-server-repo/example/subscription/subscription.yaml
--8<--
```

## Promtheus usage

[prometheus usage](./prometheus.md)