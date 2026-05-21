# CLI Tools

SDC ships two official command-line tools that complement the Kubernetes-based control plane.

| | [sdc-lite](sdc-lite.md) | [kubectl-sdc](kubectl-sdc.md) |
|---|---|---|
| **What it is** | Standalone CLI for YANG-based config work | `kubectl` plugin for SDC on Kubernetes |
| **Requires Kubernetes** | No | Yes |
| **Requires a live device** | No | No (reads from data-server) |
| **Primary audience** | Network engineers, CI pipelines, offline workflows | Operators managing live SDC-managed targets |
| **Key capabilities** | Schema loading, config validation, format conversion, diffing, blame | Running config retrieval, blame, deviation inspection and revert |

## When to use which

Use **`sdc-lite`** when you want to work with YANG schemas and device configurations without a running Kubernetes cluster — for example, to validate a config file in CI, convert between formats (JSON, XML, JSON-IETF), or explore what a set of intents produces before pushing them.

Use **`kubectl-sdc`** when you have a live cluster with SDC installed and want to inspect the state of managed targets — for example, to trace which intent owns a given config leaf, retrieve the running config from a device, or detect and revert deviations.
