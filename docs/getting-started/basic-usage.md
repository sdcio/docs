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

### Allow communication between containers attached to different network
Find the linux bridge interface dedicated to `basic-usage` container. 
```
docker network inspect -f '{{ printf "%.12s" .ID }}' basic-usage
37e8bb64ef43
```

Find the linux bridge interface dedicated to `kind` container.
```
docker network inspect -f '{{ printf "%.12s" .ID }}' kind
e4d20d240e19
```


Allow traffic back and forth issued from host belonging to each of these bridges respectively.    
(Otherwise traffic will be blocked DOCKER-ISOLATION-STAGE-[x])
```
sudo iptables -I DOCKER-USER -i br-e4d20d240e19 -o br-37e8bb64ef43 -j ACCEPT
sudo iptables -I DOCKER-USER -i br-37e8bb64ef43 -o br-e4d20d240e19 -j ACCEPT
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

## Infrastructure
The following contains information on how to deploy a Nokia SR Linux NOS container, which will consecutively be managed via sdcio.

### Installation
Deploy a [Nokia SR Linux](https://learn.srlinux.dev/) device called `dev1`via [Containerlab](https://containerlab.dev).

```bash
sudo containerlab deploy -t https://docs.sdcio.dev/artifacts/basic-usage/basic-usage.clab.yaml
```

/// details | Topology Content

```yaml
--8<--
docs/getting-started/artifacts/basic-usage.clab.yaml
--8<--
```

///

### Verification

The output of the containerlab deploy from above should indicate, that the node `clab-basic-usage-dev1` is in the running state.

```
sudo clab inspect -t basic-usage.clab.yaml
INFO[0000] Parsing & checking topology file: basic-usage.clab.yaml
+---+-----------------------+--------------+-------------------------------+---------------+---------+-----------------+--------------+
| # |         Name          | Container ID |             Image             |     Kind      |  State  |  IPv4 Address   | IPv6 Address |
+---+-----------------------+--------------+-------------------------------+---------------+---------+-----------------+--------------+
| 1 | clab-basic-usage-dev1 | c76bb71b56a8 | ghcr.io/nokia/srlinux:23.10.1 | nokia_srlinux | running | 172.21.0.200/16 | N/A          |
+---+-----------------------+--------------+-------------------------------+---------------+---------+-----------------+--------------+
```


/// details | Connectivity verification 

Spin a basic linux pod in kind cluster such as the one below:
```
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu
  labels:
    app: ubuntu
spec:
  containers:
  - image: ubuntu
    command:
      - "sleep"
      - "604800"
    imagePullPolicy: IfNotPresent
    name: ubuntu
  restartPolicy: Always
```

log into the pod
```
kubectl exec -it ubuntu -- /bin/bash
```

install ping
```
apt install inetutils-ping
```

ping SRL `dev1` node (should work after having applied iptables rules above)
```
root@ubuntu:/# ping 172.21.0.200 -c 5
PING 172.21.0.200 (172.21.0.200): 56 data bytes
64 bytes from 172.21.0.200: icmp_seq=0 ttl=62 time=13.209 ms
64 bytes from 172.21.0.200: icmp_seq=1 ttl=62 time=13.391 ms
64 bytes from 172.21.0.200: icmp_seq=2 ttl=62 time=12.021 ms
64 bytes from 172.21.0.200: icmp_seq=3 ttl=62 time=11.237 ms
64 bytes from 172.21.0.200: icmp_seq=4 ttl=62 time=19.536 ms
--- 172.21.0.200 ping statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max/stddev = 11.237/13.879/19.536/2.937 ms
root@ubuntu:/#
```

///

## Cert-Manager
The config-server (extension api-server) requires a certificate, which is created via cert-manager. The corresponding CA cert needs to be injected into the cabundle spec field of the `api-service` resource.

### Installation
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.3/cert-manager.yaml
# If the SDCIO resources, see below are being applied to fast, the webhook of the cert-manager is not already there.
# Hence we need to wait for the resource be become Available
kubectl wait -n cert-manager --for=condition=Available=True --timeout=300s deployments.apps cert-manager-webhook
```

## SDCIO

### Installation
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

### Verification
To verify that the installation did succeed, the following resources can be checked.

#### API Registration
Checking the api-registrations exist.
```bash
kubectl get apiservices.apiregistration.k8s.io | grep "sdcio.dev\|NAME"
```

The two services should be available.
```
NAME                                   SERVICE                        AVAILABLE   AGE
v1alpha1.config.sdcio.dev              network-system/config-server   True        6d
v1alpha1.inv.sdcio.dev                 Local                          True        6d
```
If the apiservices do not appear or do not show up as available, follow the [Troubleshooting](../user-guide/troubleshooting.md#config-server) section.

## Basic Usage Scenario
In the following the different kubernetes resources will be created, which are needed to manage the previousely deployed SR Linux instance.

### Installation
```bash
# Nokia SR Linux Yang Schema
kubectl apply -f https://docs.sdcio.dev/artifacts/basic-usage/schema-nokia-srl-23.10.1.yaml
# Connection Profile
kubectl apply -f https://docs.sdcio.dev/artifacts/basic-usage/target-conn-profile-gnmi.yaml
# Sync Profile
kubectl apply -f https://docs.sdcio.dev/artifacts/basic-usage/target-sync-profile-gnmi.yaml
# SRL Secret
kubectl apply -f https://docs.sdcio.dev/artifacts/basic-usage/secret-srl.yaml
# Discovery Rule
kubectl apply -f https://docs.sdcio.dev/artifacts/basic-usage/discovery_address.yaml
```

/// details | Nokia SR Linux Yang Schema Content

```yaml
--8<--
config-server-repo/example/schemas/schema-nokia-srl-23.10.1.yaml
--8<--
```

///

/// details | Discovery Rule Content

```yaml
--8<--
docs/getting-started/artifacts/discovery_address.yaml
--8<--
```

///

/// details | Connection Profile Content

```yaml
--8<--
config-server-repo/example/connection-profiles/target-conn-profile-gnmi.yaml
--8<--
```

///

/// details | Sync Profile Content

```yaml
--8<--
config-server-repo/example/sync-profiles/target-sync-profile-gnmi.yaml
--8<--
```

///

/// details | Nokia SR Linux Secret Content

```yaml
--8<--
docs/getting-started/artifacts/secret-srl.yaml
--8<--
```

///

### Verification
```bash
kubectl get sdc
```

The output provides an overview of all the SDCIO originating CRs.


First of all the `Ready` flag of the `Schema` CR is expected to be `True`. Which indicates, that the provided Yang Schema was successfully downloaded.
Next, the `DiscoveryRule` is supposed to be `Ready=True`, which is a pre-requisite for the `Target` to be created by the `DiscoverRule` controller.
On the Target, all three Fields (`Ready`, `Datastore` and `Config`) have to be `True` and in successfull connection the additional fields like Address, Platform, Serialnumber and MAC Address will be populated.
```
NAME                                       READY
discoveryrule.inv.sdcio.dev/dev1-address   True

NAME                                               READY   URL                                            REF        PROVIDER              VERSION
schema.inv.sdcio.dev/srl.nokia.sdcio.dev-23.10.1   True    https://github.com/nokia/srlinux-yang-models   v23.10.1   srl.nokia.sdcio.dev   23.10.1

NAME                                                    AGE
targetconnectionprofile.inv.sdcio.dev/gnmi-skipverify   21m

NAME                       READY   DATASTORE   CONFIG   PROVIDER              ADDRESS              PLATFORM      SERIALNUMBER     MACADDRESS
target.inv.sdcio.dev/srl   True    True        True     srl.nokia.sdcio.dev   172.21.0.200:57400   7220 IXR-D3   Sim Serial No.   1A:AB:00:FF:00:00

NAME                                            AGE
targetsyncprofile.inv.sdcio.dev/gnmi-onchange   21m
```


### Retrieve Configuration
To retrieve the running configuration from the device, the `RunningConfig` CR can be queried.
It contains an empty spec, but the config is presented in the `status` -> `value` field.

```bash
# node name is dev1
kubectl get runningconfigs.config.sdcio.dev dev1
NAME
dev1
```

The output of:
```
kubectl get runningconfigs.config.sdcio.dev dev1 -ojsonpath="{.status}" | jq
```

is quite extensive so lets just take a look at the *network-instance* configuration.

```bash
kubectl get runningconfigs.config.sdcio.dev dev1 -ojsonpath="{.status.value.network-instance}" | jq
```

Output:
```json
[
  {
    "description": "Management network instance",
    "name": "mgmt",
    "protocols": {
      "linux": {
        "export-routes": true,
        "import-routes": true
      }
    },
    "type": "ip-vrf"
  }
]
```

### Apply Config
To apply configuration for the `dev1` device apply the following [`Config`](../user-guide/configuration/config/config.md) CR.

```bash
kubectl apply -f https://docs.sdcio.dev/artifacts/basic-usage/config.yaml
```

/// details | Config Content
```yaml
--8<--
config-server-repo/example/config/config.yaml
--8<--
```
///


### Apply ConfigSet
To apply a [`ConfigSet`](../user-guide/configuration/config/configset.md), that is a configuration template that can be applied to multiple devices, apply the following `ConfigSet`.

```bash
kubectl apply -f https://docs.sdcio.dev/artifacts/basic-usage/configset.yaml
```

/// details | ConfigSet Content
```yaml
--8<--
config-server-repo/example/config/configset.yaml
--8<--
```
///
