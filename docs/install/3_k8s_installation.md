<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

First, ensure the [pre-requisites](2_prereq.md) are met.

## Install SDC Components

Once the cluster is deployed we install the `sdc` components. These manifests deploy 3 components
1. api-server deployment
2. controller deployment
3. data-server-controller statefulset

To install SDC, copy the following snippet into a shell and execute it.
```yaml
kubectl apply -f https://docs.sdcio.dev/artifacts/basic-usage/installation.yaml
```

/// details | Artifact Content

```yaml
--8<--
config-server-repo/artifacts/out/artifacts.yaml
--8<--
```

///

if successful you should see 3 running container similar to this

```
kubectl get pods -n sdc-system
```

output

```
NAME                          READY   STATUS    RESTARTS   AGE
api-server-6d7db47894-xj8wg   1/1     Running   0          38h
controller-59c99fff54-j62bh   1/1     Running   0          38h
data-server-controller-0      2/2     Running   0          38h
```