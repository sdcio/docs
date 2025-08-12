# ConfigSet
ConfigSets are partial or complete pieces of configuration that are intended to be deployed to a selected set of targets. Typically used to apply the same configuration to a set of targets using the targetSelector

## Attributes

* `target`: Is a list of configuration pieces that consist of a `targetSelector` attributes.
    * `targetSelector`: The rules used to select the targets on which this config object gets applied to
* `config`: Is a list of configuration pieces that consist of a `path` and a `value` attribute.
    * `path`: The path describes where the configuration (`value`) part is rooted. This can either by `/` to indicate the configuration root level or any valid path within the schema.
    * `value`: The canfiguration in yaml format that is meant to go under the `path` in the target device.
* `priority`: The priority field is used as a tie-breaker, when multiple Config intents try to set overlapping configurations.
* `lifecycle`: Lifecycle determines the lifecycle policies of the resource e.g. delete orphan or delete
    * `deletionPolicy`: DeletionPolicy defines the deletion policy of the resource.  
        * `delete`: (default) deletes the config from the target
        * `orphan`: does NOT delete the config from the target
* `revertive`: defines the revertive or non revertive behavior. if not defined the global configuration applies.

## Example

```yaml
--8<--
config-server-repo/example/config/configset.yaml
--8<--
```