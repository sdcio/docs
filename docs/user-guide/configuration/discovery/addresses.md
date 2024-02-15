# Device discovery using Addresses (IPs or DNS names)

Address discovery uses the provided address in the `addresses` section of the `DiscoveryRule` CustomResource to identify the target device. With address discovery `sdc` allows to enable or disable full discovery (see [Discovery Configuration Options](introduction.md#discovery-configuration-options)).

## Attributes

* `addresses`
    * `address`: The mgmt address of the Target.
    * `hostName`: The hostname of the target. if left empty the provided address will be used as the hostname.

### Examples

Example of a `DiscoveryRule`

```yaml
--8<--
config-server-repo/example/discovery-rule/discovery_address.yaml
--8<--
```