# The DiscoveryRule CustomResource

The DiscoveryVendorProfile defines the provider specific information that uniquely identify the provider, version together with additional metadata (such as platformType, hostname, serial-number and mac Address)

Curently we support gnmi, but other protocols are envisioned to be supported going forward.

## Attributes

* `gnmi`:
    * `organization`: organization matches the gnmi capabilities organization 
    * `modelMatch`: if an organization has multiple NOS(es) it can distibuish the provider using a unique key in the model
    * `encoding`: the gnmi encoding used to get the paths (default: JSON_IETF, other: JSON, PROTO, ASCII)
    * `paths`: slice/list to identify the key (fixed mapping to the target information in the target CR)
        * `key`: supported keys are `version`, `platform`, `hostname`, `serialNumber`, `macAddress`
        * `path`: gnmi path related to the key (the path can contain the keys or not)
        * `regex`: used to transform the retrieved data
        * `script`: starlark script to transform the retrieved data (used after regex in sequence) 

## How gnmi discovery works

A gNMI Capabilities Request is send

- The organization field in the capabilities identifies the provider.
- If the vendor supports multiple Network OS (NOS) options, modelMatch is used to distinguish them.

Once the NOS is identified, additional device parameters (e.g., version, MAC address, serial number, and platform) are retrieved using gNMI paths defined in DiscoveryVendorProfile.

- for each provided path the retrieved data can be transformed using regex and starlark function before it is being used to update the target CR.

If discovery is successful, the extracted parameters are reflected in the Target CR.

!!! Note "The version and provider are important as they are used to match the schema"

### Examples

```yaml
--8<--
config-server-repo/example/discoveryvendor-profile/discoveryvendor-profile-nokia-srlinux.yaml
--8<--
```

```yaml
--8<--
config-server-repo/example/discoveryvendor-profile/discoveryvendor-profile-arista.yaml
--8<--
```


```yaml
--8<--
config-server-repo/example/discoveryvendor-profile/discoveryvendor-profile-nokia-sros.yaml
--8<--
```