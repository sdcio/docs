<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

First ensure the [pre-requisites](2_prereq.md) are met

## Install SDC Components

Once the cluster is deployed we install the `sdc` components. These manifests deploy `sdc` as a deployment where the pod contains 2 containers:

1. the config-server container with the various controllers
2. the data-server/schema-server/cache collocated in a single container

To install SDCIO, copy the following snippet into a shell and execute it.
```yaml
kubectl apply -f https://docs.sdcio.dev/artifacts/basic-usage/colocated.yaml
```

/// details | Artifact Content

```yaml
--8<--
config-server-repo/artifacts/out/artifacts.yaml
--8<--
```

///

if successful you should see a running container similar to this

```
kubectl get pods -n network-system
```

output

```
NAME                             READY   STATUS    RESTARTS   AGE
config-server-7fcd95b976-p2pn7   2/2     Running   0          3d5h
```