# Config server system architecture

The config-server comprises 6 essential components:

* `Schema Reconciler`: Manages the lifecycle of a `yang` schema via the `schema` Custom Resource Definition (CRD).
* `DiscoveryRule Reconciler`: Oversees the lifecycle of the `discoveryRule` CRD.
* `TargetDatastore Reconciler`: Controls the lifecycle of the `datastore` within the data-server.
* `TargetConfigServer Reconciler`: Orchestrates the lifecycle of the `config` KRM resource in response to target state changes.
* `TargetConfigSet Server Reconciler`: Orchestrates the lifecycle of the `configSet` KRM resource in response to target state changes.
* `Config Server`: Coordinates the lifecycle of the `config` and `configSet` KRM resources in the data-server

## Schema Reconciler

The Schema Reconciler is tasked with managing `yang` schemas in the schema-server through the `schema` CRD. This reconciler handles the addition and deletion of `yang` schemas. Notably, the schema CRD remains immutable to simplify updates. It assumes that yang schemas are validated offline before integration into the system. Upon adding a `schema` CR, the reconciler downloads the referenced git repository, extracts the referenced Schema files and loads the Schema into the schema-server. Deleting a schema CR results in the deletion of the corresponding schema from the schema-server. The reconciler employs the `READY` condition to signal the reconciliation status of the `schema` CR.

## Discovery Reconciler

The Discovery Reconciler is responsible for managing the lifecycle of the `discoveryRule` CRD. It monitors the availability and alterations of referenced profiles in the `discoveryRule` CR. Additionally, it initiates or halts a discovery goroutine for each `discoveryRule` CR, regardless of whether discovery is `enabled` or `disabled`. Based on the discovery outcomes, it manages the lifecycle of the respective `target` CR. A successful discovery results in the creation of a `target` CR with a `READY` condition set to `True`.

## TargetDatastore Reconciler

The TargetDatastore Reconciler oversees the lifecycle of the datastore of a target within the [`Data-Server`](../system-architecture/data-server.md). It creates or deletes a datastore in the `Data-Server` based on updates to the `target` CR or changes in the target state within the datastore. Its status is reflected in the `DATASTORE` condition (`DSReady` in yaml / json) of the `target` CR and should be `READY` in case of normal operation.

## TargetConfigServer Reconciler

The TargetConfigServer Reconciler manages the lifecycle of the `config` KRM resources based on `target` transitions. To ensure consistent results when a target transitions from `NotReady` to `Ready`, it reapplies the original configurations before handling new ones. Consequently, the reconciler reapplies previously applied configs, and upon successful completion, declares the `CONFIG` condition (`ConfigReady` in json / yaml output) state with reason `Ready` as `True` in the `target` CR .

## TargetConfigSetServer Reconciler

The TargetConfigSetServer Reconciler oversees the lifecycle of the `configSet` KRM resources based on `target` transitions. It updates the status of the `configSet` KRM resource when a `target` CR changes state.

## Config Resources

The Config resources are implemented as an aggregated API server, as Config resources may exceed the constraints of the etcd storage limits. It manages the `config` and `configSet` KRM resources based on the `target` `READY` conditions and communicates with the data-server through the intent RPC(s).