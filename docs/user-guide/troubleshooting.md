# Troubleshooting
This section contains information on how to troubleshoot an SDCIO instance that is causing some trouble.

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
v1alpha1.config.sdcio.dev              network-system/config-server   True        6d
v1alpha1.inv.sdcio.dev                 Local                          True        6d
```

### Deployment
The Config-Server is deployed in the network-system namespace via a Deployment. 
Check for it to be READY.
If it is not ready follow the basic troubleshooting for Deployments.

```bash
kubectl get -n network-system deployments.apps config-server
```
There should be a config-server in the Ready state.
```
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
config-server   1/1     1            1           6d
```

### Service
For the APIServer a Service is referenced, this reference must resolve to the config-server.
Via the Endpoints the association to the pod can be verified.
```bash
kubectl get -n network-system endpoints config-server -o yaml
```

The Subsets addresses must list the config-server pod.
```yaml
apiVersion: v1
kind: Endpoints
metadata:
  annotations:
    endpoints.kubernetes.io/last-change-trigger-time: "2024-02-09T13:13:34Z"
  creationTimestamp: "2024-02-09T13:13:34Z"
  labels:
    sdcio.dev/config-server: "true"
  name: config-server
  namespace: network-system
  resourceVersion: "439928"
  uid: 8f849512-6021-4c7e-a08b-c3cff25ed68b
subsets:
- addresses:
  - ip: 10.244.0.8
    nodeName: api-server-control-plane
    targetRef:
      kind: Pod
      name: config-server-84465fd854-bm258
      namespace: network-system
      uid: b6986782-4055-431a-9742-f074d88febb5
  ports:
  - port: 6443
    protocol: TCP
```

## SDCTL

sdctl is a binary available for gRPC interaction with the schema-server, data-server and cache.
In a kubernetes environment, it can be launched by executing a container image.

```bash
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:{{ environment.SDCTL_VERSION }} --restart=Never --command -- /bin/bash
```

## Schema-Server

```bash
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:{{ environment.SDCTL_VERSION }} --restart=Never --command -- /app/sdctl -a data-server.network-system.svc.cluster.local:56000 schema list
```

## Data-Server

Listing data-stores
```bash
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:{{ environment.SDCTL_VERSION }} --restart=Never --command -- /app/sdctl -a data-server.network-system.svc.cluster.local:56000 datastore list
```

Fetching config from the data-store
```bash
kubectl run -ti --rm sdctl --image=ghcr.io/sdcio/sdctl:{{ environment.SDCTL_VERSION }} --restart=Never --command -- /app/sdctl -a data-server.network-system.svc.cluster.local:56000 data get --ds default.sr1 --candidate default --path /configure/service
```