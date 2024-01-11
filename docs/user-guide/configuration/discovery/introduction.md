# Target Discovery guide

SDC offers robust and flexible mechanisms for discovering devices within a network. This capability is crucial for automating the configuration and management of network devices.
SDC supports various discovery methods, including IPs or DNS names, IP prefixes, and upcoming features like service and POD discovery.

A central aspect of this discovery process is the `DiscoveryRule` CustomResource, which not only configures discovery mechanisms but also generates a specific CustomResource called `Target` for each discovered device.

## Overview of Discovery Methods in SDC

TBD

## The DiscoveryRule CustomResource

The DiscoveryRule CustomResource is the cornerstone of the SDC discovery process. It not only initiates and manages the discovery of devices but also links these devices to their corresponding configurations and credentials. The key aspects of this CustomResource include:

### Key Features

#### Device and Profiles association

Once a device is discovered, the DiscoveryRule links it with several essential components:

* __Schema__: Associates the device with its corresponding schema, enabling SDC to understand and manage the device's configuration correctly and validate changes made by users.
* __Connection Profile__: Connects the device to one or more pre-defined connection profile, which specifies how SDC should communicate with the device to modify and retrieve configuration.
* __Sync Profile__: Assigns a sync profile to the device, dictating how the device's configuration and state should be synchronized and managed.
* __Credentials__: Integrates with Kubernetes secrets to securely manage the credentials needed for accessing and configuring the device.
* __Hostname__: Either statically configured or retrieved from the device.

#### Creation of `Target` CR

For every device discovered, DiscoveryRule creates a `Target` CustomResource. This CR encapsulates details about the device, including its network address, associated schema, connection information, and synchronization settings.

### Examples

Example of a `DiscoveryRule`

```yaml
# TBD
```

This documentation page highlights the versatility and sophistication of SDC's device discovery capabilities. By leveraging DiscoveryRule, users can efficiently integrate a wide range of devices into their network management workflows, paving the way for a more automated and streamlined network configuration process.
