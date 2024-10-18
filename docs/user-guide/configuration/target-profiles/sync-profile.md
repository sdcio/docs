# Sync Profile

The Sync Profile is an integral component of SDC, enabling the accurate configuration of devices and validation of configuration payloads. 
SDC achieves this by synchronizing the device's running store and state store into an internal cache. The synchronization process, including the protocol and strategy used, is customizable through the `TargetSyncProfile` CustomResource, detailed [here](Path to CRD).

## Synchronization protocols

SDC supports the synchronization of a device's configuration and state using two protocols: gNMI and NETCONF. The `TargetSyncProfile` encompasses both protocol-specific and general fields.

### General sync Attributes

These attributes are common across synchronization protocols:

* `validate`: If set to true, SDC validates the received updates against the device's schema.
* `workers`: Determines the number of cache workers, optimizing write performance to the cache.
* `buffer`: Specifies the buffer size for queuing sync updates before writing to the cache.
* `sync`: A list of synchronization strategies, each defining a protocol and its specific attributes. Multiple strategies can be employed concurrently.

### NETCONF Sync strategy

For NETCONF synchronization, the netconf strategy is used with protocol: netconf. SDC periodically retrieves the current running configuration of the device using the NETCONF get-config RPC. This can be adjusted with the following attributes:

* `paths`: A list of paths included as `filter` in the `get-config` RPC.
* `interval`: The frequency at which `get-config` is executed.

Example NETCONF Sync Profile:

```yaml
--8<--
config-server-repo/example/sync-profiles/target-sync-profile-netconf.yaml
--8<--
```

### gNMI Sync strategy

For gNMI synchronization, set the protocol to `protocol: gnmi`:

SDC supports various gNMI subscription modes:

* `onChange`: Corresponds to gNMI stream mode ON_CHANGE.
* `sample`: Matches gNMI stream mode SAMPLE, using interval as the sample-interval.
* `once`: Equivalent to gNMI mode ONCE, where a SubscribeRequest is sent at each interval.
* `get`: Periodic get Config, interval needs to be specified.

Other gNMI specific attributes:

* `encoding`: The gNMI encoding used for subscriptions.

Example of an `onChange` gNMI SyncProfile:

```yaml
--8<--
config-server-repo/example/sync-profiles/target-sync-profile-gnmi.yaml
--8<--
```

Example of a gNMI `TargetSyncProfile` with both `once` and `onChange` modes:

```yaml
--8<--
config-server-repo/example/sync-profiles/target-sync-profile-gnmi-once-and-onchange.yaml
--8<--
```
