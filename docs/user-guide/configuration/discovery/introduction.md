# Target Discovery guide

SDC offers robust and flexible mechanisms for discovering devices within a network. This capability is crucial for automating the configuration and management of network devices.
SDC supports various discovery methods, including IPs or DNS names, IP prefixes, and service and POD discovery.

A central aspect of this discovery process is the `DiscoveryRule` CustomResource, which not only configures discovery mechanisms but also generates a specific CustomResource called `Target` for each discovered device.

## Overview of Discovery Methods in SDC

SDC offer 4 kinds of discovery:

- IP Prefix Based Discovery: Ideal for handling IP ranges and scenarios where the specific target IP address is unknown. This method allows `sdc` to intelligently explore and identify devices within specified IP prefixes.
- IP Address Based Discovery: Perfect for situations where the exact IP address of the target device is known. `sdc` enables precise discovery based on provided addresses (IP or DNS), ensuring accuracy in device identification.
- POD Based Discovery: Ideal when devices are instantiated as pods in a cluster. `sdc` enables device discovery based on the address of Kubernetes Pods. This advancement aligns with modern containerized environments, providing enhanced visibility into your network infrastructure.
- SVC Based Discovery: Ideal when devices are accessible through services in a pod. `sdc` discovers devices by utilizing the address of Kubernetes Services. This approach ensures comprehensive network mapping within dynamic Kubernetes services.

Discovery Configuration Options:

In addition to the diverse discovery methods, `sdc` offers the flexibility to enable or disable discovery based on your specific requirements. However, it's important to note that for IP Prefix Based Discovery, disabling discovery is not supported, as this method is designed to continuously scan and adapt to changing IP ranges.

Disabling discovery is enabled by supplying a `defaultSchema` in the CR definition

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
apiVersion: inv.sdcio.dev/v1alpha1
kind: DiscoveryRule
metadata:
  name: dr-static
  namespace: default
spec:
  period: 1m
  concurrentScans: 2
  defaultSchema:
    provider: srl.nokia.sdcio.dev  
    version: 23.10.1
  addresses:
  - address: 172.18.0.4
    hostName: dev1
  - address: 172.18.0.3
    hostName: dev2
  targetConnectionProfiles:
  - credentials: srl.nokia.sdcio.dev 
    connectionProfile: gnmi-skipverify
    syncProfile: gnmi-onchange
  targetTemplate:
    labels:
      sdcio.dev/region: us-east
```

This documentation page highlights the versatility and sophistication of SDC's device discovery capabilities. By leveraging DiscoveryRule, users can efficiently integrate a wide range of devices into their network management workflows, paving the way for a more automated and streamlined network configuration process.
