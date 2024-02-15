The following examples demonstrate the basic usage of SDCIO in a scenario where a Nokia SR Linux node is being configured via SDCIO installed in a Kind based Kubernetes cluster.

# Kind
[kind](https://kind.sigs.k8s.io/) is a tool for running local Kubernetes clusters using Docker container “nodes”. kind was primarily designed for testing Kubernetes itself, but may be used for local development or CI.

## Installation

```bash
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.21.0/kind-$(uname)-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

## Cluster Creation
To create a Kind based Kubernetes Cluster, issue the following command.
```bash
kind create cluster
```

# kubectl
`kubectl` is a command-line tool used to control and manage Kubernetes clusters. It allows developers and administrators to execute commands to create, monitor, and manage resources such as pods, services, deployments, and more within a Kubernetes cluster.

## Installation
To install `kubectl` issue the following command.
```bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```

# SDCIO

## Installation
To install SDCIO, copy the following snippet into a shell and execute it.
```yaml
kubectl apply -f https://docs.sdcio.dev/artifacts/colocated.yaml
```


