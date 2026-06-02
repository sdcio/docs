# Troubleshooting

<!-- Source of truth: this template. Run make generate-template before mkdocs; it writes docs/user-guide/troubleshooting.md (gitignored). Substitutes SDCTL_VERSION from versions.env. -->


This section contains information on how to troubleshoot an SDC instance that is causing some trouble.

## Config-Server
The Config-Server provides the extension kubernetes apiserver and can therefor be mainly throubleshooted via `kubectl`.

### API Registration
The Config-Server hooks in to the kubernetes apiserver by registering its APIs. If the apiregistration does not show up as AVAILABLE == True, then further investigation is required.
```bash
kubectl get apiservices.apiregistration.k8s.io | grep "sdcio.dev\|NAME"
```

The two services should be available.
```
NAME                                   SERVICE                        AVAILABLE   AGE
v1alpha1.config.sdcio.dev              sdc-system/spi-server          True        6d
v1alpha1.inv.sdcio.dev                 Local                          True        6d
```

### Deployment
The sdc components are deployed in the `sdc-system` namespace. 
Check if they are running.

```bash
kubectl get pods -n sdc-system
```
There should be a 3 pods in Running state
```
NAME                          READY   STATUS    RESTARTS   AGE
api-server-6d7db47894-xj8wg   1/1     Running   0          38h
controller-59c99fff54-j62bh   1/1     Running   0          38h
data-server-controller-0      2/2     Running   0          38h
```

### Service
For the APIServer a Service is referenced, this reference must resolve to the api-server .
Via the Endpoints the association to the pod can be verified.
```bash
kubectl get -n sdc-system endpoints api-server  -o yaml
```

The Subsets addresses must list the config-server pod.
```yaml
apiVersion: v1
kind: Endpoints
metadata:
  annotations:
    endpoints.kubernetes.io/last-change-trigger-time: "2026-02-14T05:57:20Z"
  creationTimestamp: "2026-02-14T05:57:08Z"
  labels:
    app.kubernetes.io/name: sdc-api-server
    endpoints.kubernetes.io/managed-by: endpoint-controller
  name: api-server
  namespace: sdc-system
  resourceVersion: "721"
  uid: 97db9945-73a8-401a-ae5d-25f4851c6f7a
subsets:
- addresses:
  - ip: 10.244.0.9
    nodeName: kubenet-control-plane
    targetRef:
      kind: Pod
      name: api-server-6d7db47894-xj8wg
      namespace: sdc-system
      uid: d72741ae-8906-4dc1-9d08-967a4f98a2c6
  ports:
  - name: api-service
    port: 6443
    protocol: TCP
```

## Log retrieval

SDC workloads run in the `sdc-system` namespace. Use `kubectl logs` against the deployment or StatefulSet that matches the component you need. If your install uses another namespace, substitute it for `-n sdc-system`.

The `data-server-controller` pod runs **two** containers (`controller` and `data-server`); always pass **`-c`** with the container name, as in the examples below.

**Kubernetes API aggregated extension** (from the [config-server](https://github.com/sdcio/config-server) repository):

```bash
kubectl logs -n sdc-system deployments/api-server
```

**Central config-server controller** (config-server):

This controller performs **CRD-to-CRD** reconciliation—for example expanding a `ConfigSet` (and its label selector) into `Config` resources per matching target, and driving **discovery**-related custom resources so desired state on the cluster matches how targets and schemas are wired up.

```bash
kubectl logs -n sdc-system deployments/controller
```

**Colocated data-server controller** (sidecar in the data-server StatefulSet, shipped with config-server):

This controller **bridges the Kubernetes API and the data-server API**: the data-server speaks **gRPC**, while cluster users and operators interact through Kubernetes resources; this component translates and synchronizes between those two worlds for the colocated data-server instance.

```bash
kubectl logs -n sdc-system statefulsets/data-server-controller -c controller
```

**Data-server** ([data-server](https://github.com/sdcio/data-server) repository, same pod as the controller above):

```bash
kubectl logs -n sdc-system statefulsets/data-server-controller -c data-server
```

For **data-server** logs, [Log Analyzer](https://github.com/steiler/loganalyzer) (`steiler/loganalyzer`) is a separate tool aimed at parsing and browsing structured application logs (JSON lines, nested payloads, and related decoding). See the project README for installation and usage—for example streaming logs to a file with `kubectl logs … -f` and opening them in the tool’s web UI.

Useful `kubectl logs` options in practice:

- **`-f` / `--follow`** — stream new lines (pairs well with Log Analyzer’s follow mode on a file).
- **`--tail=N`** or **`--since=…`** — cap volume on noisy or long-running pods.
- **`--previous`** — logs from the **last terminated** container instance (helpful after a crash loop restart).
- **`--timestamps`** — prefix each line with time, easier when correlating api-server, controller, and data-server around the same incident.

### Log levels and verbosity

Components generally emit **structured JSON** lines to **stderr** (what `kubectl logs` shows). How you turn the volume up depends on which binary you are running.

**`data-server`** ([data-server](https://github.com/sdcio/data-server) image, `data-server` container):

- **Default:** info-level structured logs (omit extra flags).
- **`--debug`** / **`-d`:** debug-level logs.
- **`--trace`** / **`-t`:** trace-level logs (very verbose; use only while investigating).
- These flags are **CLI arguments** on `/app/data-server`, after the existing `--config=…` argument in your StatefulSet (or Helm/Kustomize overlay). Restart the StatefulSet after changing `args`.
- Optional environment variable **`EXTRA_LOG_FILE`:** set to a path inside the container to **append the same log stream** to a file as well as stdout (for example when you mount a volume for analysis). See also the [local dev example](../dev/2_local.md#run-data-server-locally) for the same flags when running the binary outside the cluster.

**`api-server`** (aggregated extension, `/app/api-server`):

- Built with Kubernetes **RecommendedOptions**; many standard aggregated-apiserver and **klog**-style flags apply. The exact set can change between releases—inspect the image you deploy with **`/app/api-server --help`** (for example from a short-lived debug pod using the same image and entrypoint). Operators often add **`-v=<n>`** / **`--v=<n>`** (non‑negative integer, higher values request more detail from Kubernetes client machinery) when chasing low-level API or storage issues—append supported flags to the deployment **`args`** list and roll out.

**`controller`** (`/app/controller`, central deployment and colocated sidecar):

- Emits structured application logs at default severity. Extra verbosity is **release-specific**; check **`/app/controller --help`** on your image for supported flags and append any you need to the workload **`args`** (today’s chart may only set `command` with no `args`—you can add an `args` list alongside it). For CPU/heap investigation without raising log noise, use **pprof** as in [Profiling](../dev/3_pprof.md) (the default controller manifest often sets **`PPROF_PORT`**).

## SDCTL

sdctl is a binary available for gRPC interaction with the schema-server, data-server and cache.
In a kubernetes environment, it can be launched by executing a container image.

```bash
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:${SDCTL_VERSION} --restart=Never --command -- /bin/bash
```

## Schema-Server

```bash
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:${SDCTL_VERSION} --restart=Never --command -- /app/sdctl -a data-server.sdc-system.svc.cluster.local:56000 schema list
```
/// details | schema list

```
request:

response:
+------+----------------------+---------+
| Name |        Vendor        | Version |
+------+----------------------+---------+
|      | srl.nokia.sdcio.dev  | 23.10.1 |
|      | sros.nokia.sdcio.dev | 23.10.2 |
+------+----------------------+---------+
pod "sdctl" deleted
```
///

```bash
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:${SDCTL_VERSION} --restart=Never --command -- /app/sdctl -a data-server.sdc-system.svc.cluster.local:56000 schema get --vendor sros.nokia.sdcio.dev --version 23.10.2 --path /configure
```

/// details | schema get 
```
sdctl:/app$ /app/sdctl -a data-server.sdc-system.svc.cluster.local:56000 schema get --vendor sros.nokia.sdcio.dev --version 23.10.2 --path /configure
request:
path: {
  elem: {
    name: "configure"
  }
}
schema: {
  vendor: "sros.nokia.sdcio.dev"
  version: "23.10.2"
}

response:
schema: {
  container: {
    name: "configure"
    description: "Configure system configuration"
    namespace: "urn:nokia.com:sros:ns:yang:sr:conf"
    prefix: "conf"
    leaflists: {
      name: "apply-groups"
      description: "Apply a configuration group at this level"
      namespace: "urn:nokia.com:sros:ns:yang:sr:conf"
      prefix: "conf"
      type: {
        type: "leafref"
        type_name: "leafref"
        leafref: "../groups/group/name"
      }
      max_elements: 8
      is_user_ordered: true
    }
    children: "aaa"
    children: "anysec"
    children: "application-assurance"
    children: "aps"
    children: "bfd"
    children: "bmp"
    children: "call-trace"
    children: "card"
    children: "cflowd"
    children: "chassis"
    children: "connection-profile"
    children: "esa"
    children: "eth-cfm"
    children: "eth-ring"
    children: "filter"
    children: "fwd-path-ext"
    children: "group-encryption"
    children: "groups"
    children: "ipsec"
    children: "isa"
    children: "lag"
    children: "log"
    children: "macsec"
    children: "mcac"
    children: "mirror"
    children: "multicast-management"
    children: "oam-pm"
    children: "openflow"
    children: "policy-options"
    children: "port"
    children: "port-policy"
    children: "port-xc"
    children: "pw-port"
    children: "python"
    children: "qos"
    children: "redundancy"
    children: "router"
    children: "routing-options"
    children: "saa"
    children: "satellite"
    children: "service"
    children: "sfm"
    children: "subscriber-mgmt"
    children: "system"
    children: "test-oam"
    children: "vrrp"
  }
}

sdctl:/app$
```
///
/// details | schema get 2
```
sdctl:/app$ /app/sdctl -a data-server.sdc-system.svc.cluster.local:56000 schema get --vendor srl.nokia.sdcio.dev --version 23.10.1 --path /srl_nokia-interfaces
request:
path: {
  elem: {
    name: "srl_nokia-interfaces"
  }
}
schema: {
  vendor: "srl.nokia.sdcio.dev"
  version: "23.10.1"
}

response:
schema: {
  container: {
    name: "srl_nokia-interfaces"
    description: "Model for managing network interfaces and subinterfaces.\n\nThis model reuses data items defined in the IETF YANG model for\ninterfaces described by RFC 7223"
    namespace: "urn:srl_nokia/interfaces"
    prefix: "srl_nokia-if"
    children: "interface"
  }
}

```
///

## Data-Server

Listing data-stores
```bash
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:${SDCTL_VERSION} --restart=Never --command -- /app/sdctl -a data-server.sdc-system.svc.cluster.local:56000 datastore list
```
/// details | datastore list

```
datastores: {
  name: "default.dev1"
  datastore: {
    name: "default.dev1"
  }
  schema: {
    vendor: "srl.nokia.sdcio.dev"
    version: "23.10.1"
  }
  target: {
    type: "gnmi"
    address: "172.18.0.4:57400"
  }
}
datastores: {
  name: "default.sr1"
  datastore: {
    name: "default.sr1"
  }
  schema: {
    vendor: "sros.nokia.sdcio.dev"
    version: "23.10.2"
  }
  target: {
    type: "netconf"
    address: "172.22.1.11:830"
    status: CONNECTED
  }
}
datastores: {
  name: "default.dev2"
  datastore: {
    name: "default.dev2"
  }
  schema: {
    vendor: "srl.nokia.sdcio.dev"
    version: "23.10.1"
  }
  target: {
    type: "gnmi"
    address: "172.18.0.3:57400"
  }
}
datastores: {
  name: "default.sr2"
  datastore: {
    name: "default.sr2"
  }
  schema: {
    vendor: "sros.nokia.sdcio.dev"
    version: "23.10.2"
  }
  target: {
    type: "netconf"
    address: "172.22.1.12:830"
    status: CONNECTED
  }
}

pod "sdctl" deleted
```
///

Fetching config from the data-store
```bash
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:${SDCTL_VERSION} --restart=Never --command -- /app/sdctl -a data-server.sdc-system.svc.cluster.local:56000 data get --ds default.sr1 --path /configure/service
```
/// details | data get

```
request:
name: "default.sr1"
path: {
  elem: {
    name: "configure"
  }
  elem: {
    name: "service"
  }
}

notification: {
  timestamp: 1708694690324217499
  update: {
    path: {
      elem: {
        name: "configure"
      }
      elem: {
        name: "service"
      }
      elem: {
        name: "vprn"
        key: {
          key: "service-name"
          value: "vprn123"
        }
      }
      elem: {
        name: "admin-state"
      }
    }
    value: {
      string_val: "enable"
    }
  }
}

notification: {
  timestamp: 1708694690324355878
  update: {
    path: {
      elem: {
        name: "configure"
      }
      elem: {
        name: "service"
      }
      elem: {
        name: "vprn"
        key: {
          key: "service-name"
          value: "vprn123"
        }
      }
      elem: {
        name: "customer"
      }
    }
    value: {
      string_val: "1"
    }
  }
}

notification: {
  timestamp: 1708694690324481720
  update: {
    path: {
      elem: {
        name: "configure"
      }
      elem: {
        name: "service"
      }
      elem: {
        name: "vprn"
        key: {
          key: "service-name"
          value: "vprn123"
        }
      }
      elem: {
        name: "service-id"
      }
    }
    value: {
      uint_val: 101
    }
  }
}

notification: {
  timestamp: 1708694690324648209
  update: {
    path: {
      elem: {
        name: "configure"
      }
      elem: {
        name: "service"
      }
      elem: {
        name: "vprn"
        key: {
          key: "service-name"
          value: "vprn123"
        }
      }
      elem: {
        name: "service-name"
      }
    }
    value: {
      string_val: "vprn123"
    }
  }
}
```
///