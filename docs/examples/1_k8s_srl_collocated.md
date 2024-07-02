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
name: srl-lab

mgmt:
  mtu: 1500
  network: kind

topology:
  kinds:
    srl:
      type: ixrd3
      image: ghcr.io/nokia/srlinux:23.10.1-218
  nodes:
    dev1:
      kind: srl
    dev2:
      kind: srl
  links:
```

Record the ip addresses containerlab provided to both containers. You will need them in the target discovery step.

## Schema's

Once the devices/targets are up and running you need to install the corresponding device schema's. In this example we use Nokia SRLinux version 23.10.1


```yaml
kubectl apply -f - <<EOF
apiVersion: inv.sdcio.dev/v1alpha1
kind: Schema
metadata:
  name: srl.nokia.sdcio.dev-23.10.1
  namespace: default
spec:
  repoURL: https://github.com/nokia/srlinux-yang-models
  provider: srl.nokia.sdcio.dev
  version: 23.10.1
  kind: tag
  ref: v23.10.1
  dirs:
  - src: srlinux-yang-models
    dst: .
  schema:
    models:
    - srl_nokia/models
    includes:
    - ietf
    - openconfig/extensions
    - openconfig/openconfig-extensions.yang
    excludes:
    - .*tools.*
EOF
```

you can valdate the schema loading using the following command.

```shell
kubectl get schema srl.nokia.sdcio.dev-23.10.1

```

If successfull you should see the `READY` state being `True`

```
NAME                          READY   URL                                            REF        PROVIDER              VERSION
srl.nokia.sdcio.dev-23.10.1   True    https://github.com/nokia/srlinux-yang-models   v23.10.1   srl.nokia.sdcio.dev   23.10.1
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
  name: srl.nokia.sdcio.dev 
  namespace: default
type: kubernetes.io/basic-auth
stringData:
  username: ######
  password: ######
EOF
```

- TargetConnectionProfile: provides the connectivity information, which protocol and port to use towards the device

In this example we use `gnmi` with port `57400` and skip-verify because we use self-signed certificates

```yaml
kubectl apply -f - <<EOF
apiVersion: inv.sdcio.dev/v1alpha1
kind: TargetConnectionProfile
metadata:
  name: gnmi-skipverify
  namespace: default
spec:
  port: 57400
  protocol: gnmi
  encoding: ASCII
  skipVerify: true
  insecure: false
EOF
```

- TargetSyncProfile: provides the sync information we use to sync the config from the device.

In this example we use `gnmi` using an ON-CHANGE subscription.

```yaml
kubectl apply -f - <<EOF
apiVersion: inv.sdcio.dev/v1alpha1
kind: TargetSyncProfile
metadata:
  name: gnmi-onchange
  namespace: default
spec:
  buffer: 0
  workers: 10
  validate: true
  sync:
  - name: config
    protocol: gnmi
    paths:
    - /
    mode: onChange
    encoding: config
    interval: 0
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
    provider: srl.nokia.sdcio.dev  
    version: 23.10.1
  addresses:
  - address: 172.20.20.3
    hostName: dev1
  - address: 172.20.20.2
    hostName: dev2
  targetConnectionProfiles:
  - credentials: srl.nokia.sdcio.dev 
    connectionProfile: gnmi-skipverify
    syncProfile: gnmi-onchange
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
dev1   True    True        srl.nokia.sdcio.dev   172.20.20.3:57400
dev2   True    True        srl.nokia.sdcio.dev   172.20.20.2:57400
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
  name: intent1
  namespace: default
  labels:
    config.sdcio.dev/targetName: dev1
    config.sdcio.dev/targetNamespace: default
spec:
  priority: 10
  config:
  - path: /
    value:
      interface:
      - name: ethernet-1/1
        admin-state: "enable"
        description: "intent1"
        vlan-tagging: true
        subinterface:
        - index: 2
          type: bridged
          vlan:
            encap:
              single-tagged:
                vlan-id: 2
        - index: 3
          type: bridged
          vlan:
            encap:
              single-tagged:
                vlan-id: 3
        - index: 4
          type: bridged
          vlan:
            encap:
              single-tagged:
                vlan-id: 4
EOF
```

[containerlab]: (https://containerlab.dev/install/)
[kind]: (https://kind.sigs.k8s.io/)
