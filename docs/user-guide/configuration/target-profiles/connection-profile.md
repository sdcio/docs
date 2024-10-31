# Connection Profile

SDC offers versatile connection capabilities with devices, supporting multiple protocols like NETCONF and gNMI.
It is designed to accommodate a range of devices and security needs. The connection details are comprehensively outlined in the `TargetConnectionProfile` CustomResource. For further information, please refer to [here](path to CRD).

## Understanding Supported Protocols in SDC

SDC seamlessly integrates two key protocols - NETCONF and gNMI - for device communication.
Configuring connection profiles in SDC involves both general attributes and protocol-specific ones.

### General Connection Attributes

* `protocol`: Determines the connection protocol, with options being `netconf` or `gnmi`.
* `connectRetry`: The interval between retries after a connection failure, defaulting to 10 seconds.
* `timeout`: The duration for attempting initial connection establishment, set by default to 10 seconds.

### Protocol-Specific Attributes

#### NETCONF Connection Attributes

For connections via NETCONF, the `protocol` needs to be set to `netconf`. Specific attributes include:

* `port`: The designated SSH port for NETCONF sessions, usually `830`.
* `includeNS`: When enabled, XML tags incorporate their namespace as an attribute.
* `operationWithNS`: Activates proper namespacing for the `edit-config` RPC operation attribute in NETCONF.
* `useOperationRemove`: If set to true, SDC utilizes the NETCONF operation `remove` rather than `delete`.
* `preferredNetconfVersion`: Selects between NETCONF versions `1.0` or `1.1`.
* `commitCandidate`: Selects the datastore on the target for applying the config to. Defaults to `candidate`, but can be set to `running` if the target does not support a `candidate` datastore.

```yaml
--8<--
config-server-repo/example/connection-profiles/target-conn-profile-netconf.yaml
--8<--
```

#### gNMI Connection Attributes

For gNMI protocol connections, set protocol to gnmi. Key attributes for gNMI are:

* `port`: The default TCP port for gNMI sessions is `57400`.
* `encoding`: Specifies the encoding format for gNMI (`JSON`, `JSON_IETF`, `PROTO`).
* `skipVerify`: If enabled, SDC secures the connection without validating device certificates.
* `insecure`: Establishes an insecure gNMI connection when set to true.

Example gNMI Configuration with Skip-Verify:

```yaml
--8<--
config-server-repo/example/connection-profiles/target-conn-profile-gnmi.yaml
--8<--
```
