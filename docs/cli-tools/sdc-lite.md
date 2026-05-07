# sdc-lite

[`sdc-lite`](https://github.com/sdcio/sdc-lite) is a standalone CLI tool for working with network operating system (NOS) configurations based on YANG schemas. It runs entirely on your local machine — no Kubernetes cluster or live device connection required.

## Use cases

- **Validate configs offline** — check a configuration file against a YANG schema before pushing it to a device or submitting it to a CI pipeline.
- **Convert between formats** — load a config in one format (e.g. `json_ietf`) and output it in another (e.g. `xml` or `json`).
- **Inspect and diff intents** — load multiple config intents at different priorities and see the merged result, or diff it against a baseline running config.
- **Trace intent ownership** — use `blame` to see which intent is the source of each config leaf in the merged result.

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/sdcio/sdc-lite/main/install.sh | bash
```

Alternatively, if you have Go installed:

```bash
go install github.com/sdcio/sdc-lite@latest
```

Shell completions (bash, zsh, fish) are installed automatically by the install script.

## Key commands

| Command | Description |
|---|---|
| `sdc-lite schema load -t <target> -f <schema.yaml>` | Load a YANG schema and associate it with a target |
| `sdc-lite schema list` | List all loaded schemas |
| `sdc-lite config load -t <target> --file <path> --file-format <fmt> --intent-name <name>` | Load a config file as a named intent |
| `sdc-lite config validate -t <target>` | Validate the merged config against the schema |
| `sdc-lite config diff -t <target>` | Show a diff between the intent config and the running baseline |
| `sdc-lite config show -t <target> -o json -a` | Show the full merged configuration |
| `sdc-lite config blame -t <target>` | Show which intent owns each config leaf |
| `sdc-lite target show -t <target>` | Show target details (schema, intents) |
| `sdc-lite target remove -t <target>` | Remove a target and its associated state |

## Workflow example

The following walkthrough loads a Nokia SR Linux schema, applies a running config as a baseline, overlays a config intent, and inspects the result.

```bash
# 1. Load the YANG schema for SR Linux 24.10.1 and associate it with "router1"
sdc-lite schema load -t router1 \
  -f https://raw.githubusercontent.com/sdcio/config-server/refs/heads/main/example/schemas/schema-nokia-srl-24.10.1.yaml

# 2. Load the device's running config as the lowest-priority baseline intent
sdc-lite config load -t router1 \
  --file https://raw.githubusercontent.com/sdcio/sdc-lite/refs/tags/v0.1.0/data/config/running/running_srl_01.json \
  --file-format json \
  --intent-name running

# 3. Load a config intent at higher priority (ethernet-1/1 VLAN config)
sdc-lite config load -t router1 \
  --file https://raw.githubusercontent.com/sdcio/sdc-lite/refs/tags/v0.1.0/data/config/additions/srl_01.json \
  --file-format json \
  --intent-name config1 \
  --priority 50

# 4. Validate the merged config against the schema
sdc-lite config validate -t router1

# 5. Diff the intent additions against the running baseline
sdc-lite config diff -t router1 --type patch

# 6. Blame — see which intent owns each config leaf under /interface
sdc-lite config blame -t router1 -p /interface

# 7. Clean up
sdc-lite target remove -t router1
```

## Further reference

Full command reference and additional examples are available in the [sdc-lite GitHub repository](https://github.com/sdcio/sdc-lite).
