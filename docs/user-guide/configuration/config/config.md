# Config
Configs are partial or complete pieces of configuration that are intended to be deployed to the referenced target.


## Attributes

* `config`: Is a list of configuration pieces that consist of a `path` and a `value` attribute.
    * `path`: The path describes where the configuration (`value`) part is rooted. This can either by `/` to indicate the configuration root level or any valid path within the schema.
    * `value`: The canfiguration in yaml format that is meant to go under the `path` in the target device.
* `priority`: The priority field is used as a tie-breaker, when multiple Config intents try to set overlapping configurations
* `lifecycle`: Lifecycle determines the lifecycle policies of the resource e.g. delete orphan or delete
    * `deletionPolicy`: DeletionPolicy defines the deletion policy of the resource.  
        * `delete`: (default) deletes the config from the target
        * `orphan`: does NOT delete the config from the target
* `revertive`: defines the revertive or non revertive behavior. If not defined the global configuration applies (the environment variable `REVERTIVE` will apply).

## Example

```yaml
--8<--
config-server-repo/example/config/config.yaml
--8<--
```

## Example with deletion policy orphan

```yaml
--8<--
config-server-repo/example/config/config-orphan.yaml
--8<--
```
