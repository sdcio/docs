# Troubleshooting
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
SDC is deployed in the `sdc-system` namespace. If successful, you should see 3 running containers similar to this:

```bash
kubectl get pods -n sdc-system
```
There should be a config-server in the Ready state.
```
NAME                          READY   STATUS    RESTARTS   AGE
api-server-6d7db47894-xj8wg   1/1     Running   0          38h
controller-59c99fff54-j62bh   1/1     Running   0          38h
data-server-controller-0      2/2     Running   0          38h
```

### Service
For the APIServer a Service is referenced, this reference must resolve to the config-server.
Via the Endpoints the association to the pod can be verified.
```bash
kubectl get -n sdc-system endpoints api-server -o yaml
```

The Subsets addresses must list the api-server pod.
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

## SDCTL

sdctl is a binary available for gRPC interaction with the schema-server, data-server and cache.
In a kubernetes environment, it can be launched by executing a container image.

```bash
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:v0.0.9 --restart=Never --command -- /bin/bash
```

## Schema-Server

```bash
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:v0.0.9 --restart=Never --command -- /app/sdctl -a data-server.sdc-system.svc.cluster.local:56000 schema list
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
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:v0.0.9 --restart=Never --command -- /app/sdctl -a data-server.sdc-system.svc.cluster.local:56000 schema get --vendor sros.nokia.sdcio.dev --version 23.10.2 --path /configure
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
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:v0.0.9 --restart=Never --command -- /app/sdctl -a data-server.sdc-system.svc.cluster.local:56000 datastore list
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
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:v0.0.9 --restart=Never --command -- /app/sdctl -a data-server.sdc-system.svc.cluster.local:56000 data get --ds default.sr1 --path /configure/service
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