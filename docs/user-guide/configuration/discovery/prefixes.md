# Device discovery using IP prefixes

IP Prefix discovery uses the provided prefix in the `prefixes` section of the `DiscoveryRule` CustomResource to identify the target device. With prefix discovery `sdc` full discovery cannot be disabled,

## Attributes

* `prefixes`:
    * `prefix`: The ip prefix used for discovery.
    * `excludes`: The IP addresses or prefixes to exclude during discovery

### Examples

Example of a `DiscoveryRule`

```yaml
--8<--
config-server-repo/example/discovery-rule/discovery_prefix.yaml
--8<--
```