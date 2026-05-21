# kubectl-sdc

[`kubectl-sdc`](https://github.com/sdcio/kubectl-sdc) is a `kubectl` plugin that extends the Kubernetes CLI with SDC-specific commands. It provides visibility into the state of SDC-managed targets directly from the command line, without needing to query raw Kubernetes resources.

## Use cases

- **Inspect running config** — retrieve the actual configuration present on a managed device, in a human-readable format.
- **Trace intent ownership** — use `blame` to see which Config CR (or the device itself) is the source of each configuration leaf, and detect where higher-priority intents are overriding others.
- **Detect and revert deviations** — list configuration paths where the device has drifted from its intended state, and selectively revert them.

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/sdcio/kubectl-sdc/main/install.sh | sh
```

Alternatively, if you have Go installed:

```bash
go install github.com/sdcio/kubectl-sdc/cmd/kubectl-sdc@main
```

Once installed, `kubectl sdc` is available as a `kubectl` plugin. The install script also installs `kubectl_complete-sdc` for tab-completion support.

## Key commands

| Command | Description |
|---|---|
| `kubectl sdc blame --target <name>` | Tree view of the running config showing which intent owns each leaf |
| `kubectl sdc runningconfig --target <name>` | Retrieve the running config from the data-server |
| `kubectl sdc deviation --target <name>` | List deviations (drifts between intended and actual config) for a target |
| `kubectl sdc apply -f <file>` | Apply a `TargetClearDeviation` manifest to revert selected deviations |

Both `blame` and `deviation` support `--filter-*` flags for narrowing output by path, leaf name, or owner, and an `--interactive` mode backed by a fuzzy finder.

## Workflow example

The following walkthrough inspects a live SDC-managed target, finds a deviation, and reverts it.

```bash
# 1. See the running config for a target in xpath format
kubectl sdc runningconfig --target srl1 --format xpath

# 2. Check which intent owns each config leaf — filter to just the interface subtree
kubectl sdc blame --target srl1 --filter-path /interface

# 3. List all deviations on the target
kubectl sdc deviation --target srl1

# 4. Narrow down to deviations under /interface only
kubectl sdc deviation --target srl1 --filter-path /interface

# 5. Render the selected deviations as a TargetClearDeviation manifest
kubectl sdc deviation --target srl1 --filter-path /interface --format resource-yaml

# 6. Apply the manifest to revert the deviations
kubectl sdc deviation --target srl1 --filter-path /interface --format resource-yaml \
  | kubectl sdc apply -f -
```

!!! note
    All commands use the current `kubectl` context and namespace.

## Further reference

Full command reference, filtering options, and interactive mode documentation are available in the [kubectl-sdc GitHub repository](https://github.com/sdcio/kubectl-sdc).
