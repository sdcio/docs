# Basic Usage
The following examples demonstrate the basic usage of SDCIO in a scenario where a Nokia SR Linux node is being configured via SDCIO installed in a Kind based Kubernetes cluster.

## Kind
[kind](https://kind.sigs.k8s.io/) is a tool for running local Kubernetes clusters using Docker container “nodes”. kind was primarily designed for testing Kubernetes itself, but may be used for local development or CI.

### Installation

```bash
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.21.0/kind-$(uname)-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

### Cluster Creation
To create a Kind based Kubernetes Cluster, issue the following command.
```bash
kind create cluster
```

## kubectl
`kubectl` is a command-line tool used to control and manage Kubernetes clusters. It allows developers and administrators to execute commands to create, monitor, and manage resources such as pods, services, deployments, and more within a Kubernetes cluster.

### Installation
To install `kubectl` issue the following command.
```bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```

## Containerlab

[Containerlab](https://containerlab.dev) is a tool for creating virtual network topologies using container-based network emulation. It is particularly useful for testing and validating network configurations and automation workflows in a lab environment.

### Installation
To install Containerlab follow the instruction at https://containerlab.dev/install/ or simply run the following.

```bash
bash -c "$(curl -sL https://get.containerlab.dev)"
```

## SDCIO

### Installation
To install SDCIO, copy the following snippet into a shell and execute it.
```yaml
kubectl apply -f https://docs.sdcio.dev/artifacts/colocated.yaml
```

### Verification
To verify that the installation did succeed, the following resources can be checked.

#### API Registration
Checking the api-registrations exist.
```bash
kubectl get apiservices.apiregistration.k8s.io | grep "sdcio.dev|NAME"
```

The two services should be available.
```
NAME                                   SERVICE                        AVAILABLE   AGE
v1alpha1.config.sdcio.dev              network-system/config-server   True        6d
v1alpha1.inv.sdcio.dev                 Local                          True        6d
```

#### Deployment
Check for the deployment to be ready.
```bash
kubectl get -n network-system deployments.apps
```
There should be a config-server in the Ready state.
```
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
config-server   1/1     1            1           6d
```

#### Service
For the APIServer a Service is referenced, this reference must resolve to the config-server.
Via the Endpoints the association to the pod can be verified.
```bash
kubectl get -n network-system endpoints config-server -o yaml
```

The Subsets addresses must list the config-server pod.
```
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

## Infrastructure

Deploy a Nokia SR Linux device via [Containerlab](https://containerlab.dev).

```bash
containerlab deploy -t https://docs.sdcio.dev/artifacts/basic-usage.clab.yaml
```

Following is the topology definition:

```yaml
--8<--
docs/getting-started/basic-usage.clab.yaml
--8<--
```
