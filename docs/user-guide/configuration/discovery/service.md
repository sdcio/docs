# Device discovery using k8s services

Service discovery uses the provided `serviceSelector` section of the `DiscoveryRule` CustomResource to identify the target device(s). With service discovery `sdc` allows to enable or disable full discovery. Service discovery uses the kubernetes `Service` to identify the target using the cluster domain name following the [kubernetes logic](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#services).

## Attributes

* `serviceSelector`:
    * `matchLabels`: matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. (uses kubernetes logic)
    * `matchExpressions`: matchExpressions is a list of label selector requirements. The requirements are ANDed. (uses kubernetes logic)
* `serviceDomain`: identifies the local service domain that is used in the cluster. Defaults to `cluster.local` but can be changed based on the cluster setup
### Examples

Example of a `DiscoveryRule`

```yaml
--8<--
config-server-repo/example/discovery-rule/discovery_svc.yaml
--8<--
```