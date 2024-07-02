<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

## Pre-requisites

Ensure the [pre-requisites](../install/2_prereq.md) are met

### Install containerlab

SDC will need to interact with a device that talks `YANG`. You can use physical, virtual or containers. In this example we use [containerlab][containerlab] a tool to ease deploying labs with container images.

[containerlab]: (https://containerlab.dev/install/)

## SDC on kubernetes

Install the [k8s-collocated](../install/3_k8s_collocated.md) environment using a [kind][kind] cluster 

## Devices

Once the sdc components are up and running, you can proceed to deploy devices, configuring them using YANG schemas. To do this we deploy [containerlab][containerlab] using a simple topology as shown below. 

!!!warning "Container connectivity"
    Ensure the network and kind cluster containers can communicate. In this example this is accomplished by configuring containerlab to use the kind docker bridge for its management network `mgmt.network: kind`.

```yaml
name: sros-lab

mgmt:
  mtu: 1500
  network: kind

topology:
  kinds:
    vr-sros:
      image: registry.srlinux.dev/pub/vr-sros:23.10.R1
      license: license-sros23.txt
  nodes:
    dev1:
      kind: vr-sros
      mgmt-ipv4: 172.20.20.11
      mgmt-ipv6: 2001:172:20:20::11
    dev2:
      kind: vr-sros
      mgmt-ipv4: 172.20.20.12
      mgmt-ipv6: 2001:172:20:20::12
```

Record the ip addresses containerlab provided to both containers. You will need them in the target discovery step.

## Schema's

Once the devices/targets are up and running you need to install the corresponding device schema's. In this example we use Nokia SRLinux version 23.10.1


```yaml
kubectl apply -f - <<EOF
apiVersion: inv.sdcio.dev/v1alpha1
kind: Schema
metadata:
  name: sros.nokia.sdcio.dev-23.10.1
  namespace: default
spec:
  repoURL: https://github.com/nokia/7x50_YangModels
  provider: sros.nokia.sdcio.dev
  version: 23.10.1
  kind: tag
  ref: sros_23.10.r1
  dirs:
  - src: YANG
    dst: .
  schema:
    models:
    - nokia-combined
    includes:
    - ietf
    - nokia-sros-yang-extensions.yang
EOF
```

you can valdate the schema loading using the following command.

```shell
kubectl get schema sros.nokia.sdcio.dev-23.10.1

```

If successfull you should see the `READY` state being `True`

```
NAME                          READY   URL                                            REF        PROVIDER              VERSION
sros.nokia.sdcio.dev-23.10.1   True    https://github.com/nokia/7x50_YangModels   sros_23.10.r1   sros.nokia.sdcio.dev   23.10.1
```

## Discovering targets

To discover a device/target, you first need to deploy some profiles which informs the discovery controller how to authenticate to the target and which sync and connectivity profiles to use.

- Secret: used to authenticate the system.

Ensure you update the username and password for your environment

```yaml
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: sros.nokia.sdcio.dev 
  namespace: default
type: kubernetes.io/basic-auth
stringData:
  username: ######
  password: ######
EOF
```

- TargetConnectionProfile: provides the connectivity information, which protocol and port to use towards the device

In this example we use `netconf` with port `830` and skip-verify because we use self-signed certificates

```yaml
kubectl apply -f - <<EOF
apiVersion: inv.sdcio.dev/v1alpha1
kind: TargetConnectionProfile
metadata:
  name: netconf
  namespace: default
  labels:
    dummy: dummy
spec:
  port: 830
  protocol: netconf
  encoding: ASCII
  skipVerify: true
  includeNS: true
  operationWithNS: true
EOF
```

- TargetSyncProfile: provides the sync information we use to sync the config from the device.

In this example we use `netconf` using a PERIOD retrieval.

```yaml
kubectl apply -f - <<EOF
apiVersion: inv.sdcio.dev/v1alpha1
kind: TargetSyncProfile
metadata:
  name: netconf-getconfig
  namespace: default
spec:
  buffer: 0
  workers: 10
  validate: true
  sync:
  - name: config
    protocol: netconf
    paths:
    - /
    mode: sample
    encoding: config
    interval: 10
EOF
```
Once profiles are up installed, you can now deploy a `DiscoveryRule`. In this example we use static ip discovery (or better no discovery). It means the `ip address/prefix`  containerlab returned should be used as the ip prefix in the following CRD.

The default schema should match the schema you loaded in the schema section.

```yaml
kubectl apply -f - <<EOF
apiVersion: inv.sdcio.dev/v1alpha1
kind: DiscoveryRule
metadata:
  name: dr-static
  namespace: default
spec:
  period: 1m
  concurrentScans: 2
  defaultSchema:
    provider: sros.nokia.sdcio.dev  
    version: 23.10.1
  addresses:
  - address: 172.20.20.11
    hostName: dev1
  - address: 172.20.20.12
    hostName: dev2
  targetConnectionProfiles:
  - credentials: sros.nokia.sdcio.dev
    connectionProfile: netconf
    syncProfile: netconf-getconfig
  targetTemplate:
    labels:
      sdcio.dev/region: us-east
EOF
```

The discovery of the target can be observed using the following comamnd

```
kubectl get targets.inv.sdcio.dev
```

When target are successfully discovered you should see both `READY` and `DATASTORE` set to `True`.

```
NAME   READY   DATASTORE   PROVIDER              ADDRESS             PLATFORM   SERIALNUMBER   MACADDRESS
dev1   True    True        sros.nokia.sdcio.dev   172.20.20.11:57400
dev2   True    True        sros.nokia.sdcio.dev   172.20.20.12:57400
```

## Configure Intents

Now that targets are ready to be comsumed we can provision the targets with configuration data in a declarative way.

The following parameters are important
- metadata.name: name of the intent
- metadata.labels: config.sdcio.dev/targetName and config.sdcio.dev/targetNamespace tell the config-server which device this configuration applies to
- priority: defines the priority of the intent if overlapping intents apply to the target
- Config has a:
  - path: relative to the root
  - value: the config you apply to the device in `yaml` format

```yaml
kubectl apply -f - <<EOF
apiVersion: config.sdcio.dev/v1alpha1
kind: Config
metadata:
  name: intent1-sros
  namespace: default
  labels:
    config.sdcio.dev/targetName: dev1
    config.sdcio.dev/targetNamespace: default
spec:
  priority: 10
  config:
  - path: /
    value:
      configure:
        service:
          vprn:
            service-name: "vprn123"
            customer: "1"
            service-id: "200"
            admin-state: "enable"
EOF
```

[containerlab]: (https://containerlab.dev/install/)
[kind]: (https://kind.sigs.k8s.io/)
