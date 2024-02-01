# Config
Configs are partial or complete pieces of configuration that are intended to be deployed to the referenced target.

## Example
```yaml
--8<--
config/config.yaml
--8<--
```

## Attributes

* `config`: Is a list of configuration pieces that consist of a `path` and a `value` attribute.
    * `path`: The path describes where the configuration (`value`) part is rooted. This can either by `/` to indicate the configuration root level or any valid path within the schema.
    * `value`: The canfiguration in yaml format that is meant to go under the `path` in the target device.
* `priority`: The priority field is used as a tie-breaker, when multiple Config intents try to set overlapping  <<< TODO >>>