<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

## kubectl

First install [kubectl][kubectl] if not already installed

## Auto completions for kubectl (optional)

/// tab | bash

```
source <(kubectl completion bash)
alias k=kubectl
complete -o default -F __start_kubectl k
```
///

/// tab | zsh
```
source <(kubectl completion zsh)
alias k=kubectl
complete -F _start_kubectl k
```
///

## Install Kubernetes (optional)

To install `sdc` on a kubernetes cluster we first need to install a `kubernetes` cluster. 
Other than the minimum version being `v1.29`[ˆ1], `Sdc` has no special requirements on the `k8s` cluster, so any `k8s` flavor should work, bearing in mind the minimum version[ˆ1] 

/// tab | kind

First install kind using [kind][kind-install]

In this example we install a [`kind`][kind] cluster with name `sdc`. 

```
kind create cluster --name sdc
```
///

/// tab | other
///

## Install Cert-Manager
The config-server (extension api-server) requires a certificate, which is created via cert-manager. The corresponding CA cert needs to be injected into the cabundle spec field of the `api-service` resource.

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.3/cert-manager.yaml
# If the SDCIO resources, see below are being applied to fast, the webhook of the cert-manager is not already there.
# Hence we need to wait for the resource be become Available
kubectl wait -n cert-manager --for=condition=Available=True --timeout=300s deployments.apps cert-manager-webhook
```

[kind-install]: https://kind.sigs.k8s.io/docs/user/quick-start/#installation
[kind]: https://kind.sigs.k8s.io/
[kubectl]: https://kubernetes.io/docs/tasks/tools/

[^1]: A minimum kubernetes version of v1.29 is required to support [API Priority and Fairness](https://kubernetes.io/docs/concepts/cluster-administration/flow-control/)