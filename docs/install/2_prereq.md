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

To install `sdc` on a Kubernetes cluster we first need to install a Kubernetes cluster. 
Other than the minimum version being `v1.29`[^1], `sdc` has no special requirements on the `k8s` cluster, so any `k8s` flavor should work, bearing in mind the minimum version[^1] 

/// tab | kind

First install kind using [kind][kind-install]

In this example we install a [`kind`][kind] cluster with name `sdc`. 

```
kind create cluster --name sdc
```
///

/// tab | other
///

## Install cert-manager

SDC depends on [cert-manager](https://cert-manager.io) to issue the TLS
certificate served by the config-server's aggregated API server and to keep
the `APIService` `caBundle` in sync with the SDC root CA via `cainjector`.
cert-manager **must be installed and ready before** the SDC manifests are
applied. See [Cert-Manager & TLS Trust Chain](4_cert-manager.md) for how the
chain is built and rotated.

Install cert-manager (tested with `v1.20.2`):

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.20.2/cert-manager.yaml
```

Wait for all three cert-manager components to be Available — the controller
issues certificates, the `cainjector` populates the `APIService` `caBundle`,
and the webhook validates cert-manager CRs. SDC needs all three before its
resources are applied:

```bash
kubectl wait -n cert-manager --for=condition=Available=True --timeout=300s \
  deployment/cert-manager \
  deployment/cert-manager-cainjector \
  deployment/cert-manager-webhook
```

[kind-install]: https://kind.sigs.k8s.io/docs/user/quick-start/#installation
[kind]: https://kind.sigs.k8s.io/
[kubectl]: https://kubernetes.io/docs/tasks/tools/

[^1]: A minimum Kubernetes version of v1.29 is required to support [API Priority and Fairness](https://kubernetes.io/docs/concepts/cluster-administration/flow-control/)