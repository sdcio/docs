# Basic Usage
The following examples demonstrate the basic usage of SDCIO in a scenario where a Nokia SR Linux node is being configured via SDCIO installed in a Kind based Kubernetes cluster.

## Kind
[kind](https://kind.sigs.k8s.io/) is a tool for running local Kubernetes clusters using Docker container “nodes”. kind was primarily designed for testing Kubernetes itself, but may be used for local development or CI.

### Installation

```bash
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.26.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

### Cluster Creation
To create a Kind based Kubernetes Cluster, issue the following command.
```bash
kind create cluster
# Allow the kind cluster to communicate with the later created containerlab topology
sudo iptables -I DOCKER-USER -o br-$(docker network inspect -f '{{ printf "%.12s" .ID }}' kind) -j ACCEPT
```

/// details | iptables command description

```
sudo iptables -I DOCKER-USER -o br-$(docker network inspect -f '{{ printf "%.12s" .ID }}' kind) -j ACCEPT
```

- `docker network inspect -f '{{ printf "%.12s" .ID }}' kind` - inspects the kind docker network, that the kind cluster is attached to. Extract from the json that is returned, the first 12 characters of the Id field.
- `sudo iptables -I DOCKER-USER -o br-$(...) -j ACCEPT` - as root insert a firewall rule to the DOCKER-USER chain, concerning the bridge with the name "br-<FIRST-12-CHAR-OF-THE-DOCKER-NETWORK-ID>" with the action ACCEPT.

///

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
Deploy a [Nokia SR Linux](https://learn.srlinux.dev/) device called `dev1` via [Containerlab](https://containerlab.dev).

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

The output of the containerlab deploy from above should indicate, that the node `clab-basic-usage-srl` is in the running state.

```
+---+----------------------+--------------+-----------------------+---------------+---------+-----------------+--------------+
| # |         Name         | Container ID |         Image         |     Kind      |  State  |  IPv4 Address   | IPv6 Address |
+---+----------------------+--------------+-----------------------+---------------+---------+-----------------+--------------+
| 1 | clab-basic-usage-srl | e84130ad8b49 | ghcr.io/nokia/srlinux | nokia_srlinux | running | 172.21.0.200/16 | N/A          |
+---+----------------------+--------------+-----------------------+---------------+---------+-----------------+--------------+
```
## Cert-Manager
The config-server (extension api-server) requires a certificate, which is created via cert-manager. The corresponding CA cert needs to be injected into the cabundle spec field of the `api-service` resource.

### Installation
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.16.2/cert-manager.yaml
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
kubectl apply -f https://docs.sdcio.dev/artifacts/basic-usage/schema-nokia-srl-24.10.1.yaml
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
config-server-repo/example/schemas/schema-nokia-srl-24.10.1.yaml
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

When running the below command you are provides with an overview of all the SDCIO originating CRs in the system


```bash
kubectl get sdc
```

First of all the `Ready` flag of the `Schema` CR is expected to be `True`. Which indicates, that the provided Yang Schema was successfully downloaded.
Next, the `DiscoveryRule` is supposed to be `Ready=True`, which is a pre-requisite for the `Target` to be created by the `DiscoverRule` controller.
On the Target, all three Fields (`Ready`, `Datastore` and `Config`) have to be `True` and in successfull connection the additional fields like Address, Platform, Serialnumber and MAC Address will be populated.
```
NAME                                       READY
discoveryrule.inv.sdcio.dev/dev1-address   True

NAME                                                READY   PROVIDER               VERSION      URL                                            REF
schema.inv.sdcio.dev/srl.nokia.sdcio.dev-24.10.1    True    srl.nokia.sdcio.dev    24.10.1      https://github.com/nokia/srlinux-yang-models   v24.10.1

NAME                                                    AGE
targetconnectionprofile.inv.sdcio.dev/gnmi-skipverify   21m

NAME                       READY   REASON    PROVIDER              ADDRESS              PLATFORM      SERIALNUMBER     MACADDRESS
target.inv.sdcio.dev/dev1   True    True     srl.nokia.sdcio.dev   172.21.0.200:57400   7220 IXR-D3   Sim Serial No.   1A:AB:00:FF:00:00

NAME                                            AGE
targetsyncprofile.inv.sdcio.dev/gnmi-get   21m
```


### Retrieve Configuration
To retrieve the running configuration from the device, the `RunningConfig` CR can be queried.
It contains an empty spec, but the config is presented in the `status` -> `value` field.

```bash
kubectl get runningconfigs.config.sdcio.dev dev1 
```

The output is quite extensive so lets just take a look at the *network-instance* configuration.

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
