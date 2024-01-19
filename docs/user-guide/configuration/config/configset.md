# ConfigSet
ConfigSets are partial or complete pieces of configuration that are intended to be deployed to a selected set of targets. Typically used to apply the same configuration to a set of targets using the targetSelector

## Example
```yaml
apiVersion: config.sdcio.dev/v1alpha1
kind: ConfigSet
metadata:
  name: intent1
  namespace: default
spec:
  target:
    targetSelector:
      matchLabels:
        sdcio.dev/region: us-east
  priority: 10
  config:
  - path: /
    value:
      interface:
      - name: ethernet-1/1
        admin-state: "enable"
        description: "intent1"
        vlan-tagging: true
```

## Attributes

* `target`: Is a list of configuration pieces that consist of a `targetSelector` attributes.
    * `targetSelector`: The rules used to select the targets on which this config object gets applied to
* `config`: Is a list of configuration pieces that consist of a `path` and a `value` attribute.
    * `path`: The path describes where the configuration (`value`) part is rooted. This can either by `/` to indicate the configuration root level or any valid path within the schema.
    * `value`: The canfiguration in yaml format that is meant to go under the `path` in the target device.
* `priority`: The priority field is used as a tie-breaker, when multiple Config intents try to set overlapping  <<< TODO >>>