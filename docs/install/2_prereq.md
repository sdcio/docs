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

To install `sdc` on a kubernetes cluster we first need to install a `kubernetes` cluster. `Sdc` has no special requirements on the `k8s` cluster, so any `k8s` distribution should work. 

/// tab | kind

First install kind using [kind][kind-install]

In this example we install a [`kind`][kind] cluster with name `sdc`. 

```
kind create cluster --name sdc
```
///

/// tab | other
///

[kind-install]: (https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
[kind]: (https://kind.sigs.k8s.io)
[kubectl]: (https://kubernetes.io/docs/tasks/tools/)

## install containerlab (optional)

SDC will need to interact with a device that talks `YANG`. You can use physical, virtual or containers. For containers we could use [containerlab][containerlab] a tool to ease deploying labs with container images.

[containerlab]: (https://containerlab.dev/install/)