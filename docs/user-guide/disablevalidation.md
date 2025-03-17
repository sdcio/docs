# Disable Validation
 

Data/Configuration which is transacted towards the data-server is YANG validated before we even attempt to push any changes towards the device.

By Default we validate Mandatory statements, leafrefs (including min/max attributes), patterns, must statements, length, range and max-elements.

However, in some cases, the YANG schema which is uploaded to schema-server might be incomplete/incorrect/...

While a valid workaround may be to create YANG deviations to fix the schema issues, another might be to turn off certain knobs in the validation process.

## data-server configuration

the data-server (yaml) configuration exposes such knobs.

By default (either implicit or explicit) the follow configuration is applied:

```yaml
validation-defaults:
  disabled-validators:
    mandatory: false
    leafref: false
    leafref-min-max-attributes: false
    pattern: false
    must-statements: false
    length: false
    range: false
    max-elements: false
```

Should you want to disable validation for all (or some), then the following should be applied:

```yaml
validation-defaults:
  disabled-validators:
    mandatory: true
    leafref: true
    leafref-min-max-attributes: true
    pattern: true
    must-statements: true
    length: true
    range: true
    max-elements: true
```

## existing k8s cluster

Apply/update the following ConfigMap 

```bash
kubectl apply -f configmap-data-server.yaml
```

/// details | data-server ConfigMap
    type: note

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: data-server
  namespace: network-system
data: 
  data-server.yaml: |
    grpc-server:
      schema-server:
        enabled: true
        schemas-directory: ./schemas

      data-server:
        max-candidates: 16

      max-recv-msg-size: 25165824 # 24 * 1024 * 1024 (24MB)

    datastores: # this specifies MAIN datastores

    schema-store:
      # type is either memory or persistent (default)
      type: persistent
      path: "/schemadb"

    cache: 
      type: local
      store-type: badgerdb
      dir: "/cached/caches"

    prometheus:
      address: ":56090"

    validation-defaults:
      disabled-validators:
        mandatory: true
        leafref: true
        leafref-min-max-attributes: true
        pattern: true
        must-statements: true
        length: true
        range: true
        max-elements: true
```
///

Subsequently, delete the existing POD to force restart config-server/data-server with the updated configuration.

```bash
kubectl delete pod $(kubectl get pod -n network-system --no-headers -o custom-columns=":metadata.name") -n network-system
```
