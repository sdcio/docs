# Device discovery using k8s PODs

Pod discovery uses the provided `podSelector` section of the `DiscoveryRule` CustomResource to identify the target device(s). With pod discovery `sdc` allows to enable or disable full discovery (see [Discovery Configuration Options](introduction.md#discovery-configuration-options)). POD discovery checks if the `Pod` is ready and uses the first IP adddress in the POD status to identify the `target`.

## Attributes

* `podSelector`:
    * `matchLabels`: matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. (uses kubernetes logic)
    * `matchExpressions`: matchExpressions is a list of label selector requirements. The requirements are ANDed. (uses kubernetes logic)

### Examples

Example of a `DiscoveryRule`

```yaml
--8<--
config-server-repo/example/discovery-rule/discovery_pod.yaml
--8<--
```