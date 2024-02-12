# Config server system architecture

The config-server comprises 6 essential components:

* `Schema Reconciler`: Manages the lifecycle of a `yang` schema via the `schema` Custom Resource Definition (CRD).
* `DiscoveryRule Reconciler`: Oversees the lifecycle of the `discoveryRule` CRD.
* `TargetDatastore Reconciler`: Controls the lifecycle of the `datastore` within the data-server.
* `TargetConfigServer Reconciler`: Orchestrates the lifecycle of the `config` KRM resource in response to target state changes.
* `TargetConfigSet Server Reconciler`: Orchestrates the lifecycle of the `configSet` KRM resource in response to target state changes.
* `Config Server`: Coordinates the lifecycle of the `config` and `configSet` KRM resources in the data-server

## Schema reconciler

The Schema Reconciler is tasked with managing `yang` schemas in the schema-server through the `schema` CRD. This reconciler handles the addition and deletion of `yang` schemas. Notably, the schema CRD remains immutable to simplify updates. It assumes that yang schemas are validated offline before integration into the system. Upon adding a `schema` CR, the reconciler downloads the schema from Git and loads it into the schema-server. Deleting a schema CR removes the corresponding schema from the schema-server. The reconciler employs the `READY` condition to signal the reconciliation status of the `schema` CR.

## Discovery reconciler

The Discovery Reconciler is responsible for managing the lifecycle of the `discoveryRule` CRD. It monitors the availability and alterations of referenced profiles in the discoveryRule CR. Additionally, it initiates or halts a discovery goroutine for each discoveryRule CR, regardless of whether discovery is `enabled` or `disabled`. Based on the discovery outcomes, it manages the lifecycle of the respective `target` CR. A successful discovery results in the creation of a `target` CR with a `READY` condition set to `True`.

## TargetDatastore reconciler

The Target Datastore Reconciler oversees the lifecycle of the datastore of a target within the data-server. It creates or deletes a datastore in the data-server based on updates to the `target` CR or changes in the target state within the data-store. Its status is reflected in the DataStore `READY` condition of the `target` CR.

## TargetConfigServer reconciler

The Target Config Server Reconciler manages the lifecycle of the `config` KRM resources based on `target` transitions. To ensure consistent results when a target transitions from `NotReady` to `Ready`, it reapplies the original configurations before handling new ones. Consequently, the reconciler reapplies previously applied configs, and upon successful completion, declares the `Config Ready` state in the `target` CR.

## TargetConfigSetServer reconciler

The Target Config Set Server Reconciler oversees the lifecycle of the `configSet` KRM resources based on `target` transitions. It updates the status of the `configSet` KRM resource when a Target changes state.

## Config server

The Config Server is implemented as an aggregated API server, as Config Resources may exceed the constraints of etcd. It manages the `config` and `configSet` KRM resources based on the `target` `READY` conditions and communicates with the data-server through the intent RPC(s).