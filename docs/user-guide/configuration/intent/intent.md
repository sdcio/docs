# Intent
Intents are partial or complete pieces of configuration that are intended to be deployed to the referenced target.

## Example
```yaml
apiVersion: config.sdcio.dev/v1alpha1
kind: Config
metadata:
  name: dev1-interface-system0
  namespace: default
  labels:
    targetName: dev1
    targetNamespace: default
spec:
  priority: 10
  config:
  - path: /
    value:
      interface:
      - name: "system0"
        admin-state: "enable"
        description: "k8s-system0-dummy"
```

## Attributes

* `config`: 
* `priority`: The priority field is used as a tie-breaker, when multiple Config intents try to set overlapping 