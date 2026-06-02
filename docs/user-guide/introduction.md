# User guide

This section describes how to **configure and operate SDC** on Kubernetes: which Custom Resources exist, what fields mean, and how they fit together. It assumes you have a cluster running the SDC components (or are reading ahead while planning a deployment).

## Before you start

- **New to SDC?** Work through [Basic usage](../getting-started/basic-usage.md) for an end-to-end example, then return here for the full configuration surface.
- **Installing or upgrading?** Use the [Installation](../install/1_overview.md) docs for prerequisites, layout, and deployment steps.
- **How the pieces connect?** The [home page](../index.md) and [System architecture](../system-architecture/architecture.md) explain schema-server, data-server, cache, and config-server; this guide stays closer to **Kubernetes resources and day‑two configuration**.

## How the topics build on each other

SDC configures **targets** (devices or emulated nodes) using **YANG schemas** and **declarative** `Config` / `ConfigSet` objects. A practical order that matches how the system is usually brought up:

1. **[Schema](configuration/schemas.md)** — Load vendor YANG from a git source so validation and tooling know your models.
2. **Discovery** — Rules that find endpoints (addresses, prefixes, services, pods) and materialize **Target** objects.
3. **[Target](configuration/target/target.md)** — Binds a discovered or static endpoint to protocol options, profiles, and datastore behaviour.
4. **Configuration** — **[Config](configuration/config/config.md)** / **[ConfigSet](configuration/config/configset.md)** and **[Subscription](configuration/subscription/subscription.md)** for intent, sync, and subscriptions (including Prometheus-oriented examples where relevant).

After that, the guide covers **[Deviation](deviation.md)**, **[Disable validation](disablevalidation.md)**, **[Monitoring](../monitoring/prometheus-operator.md)** (metrics and Prometheus Operator lab setup), and **[Troubleshooting](troubleshooting.md)** for operational issues.

If something here disagrees with behaviour you see on cluster, treat [Troubleshooting](troubleshooting.md) and issue trackers as the next step; this guide tracks the intended contract of the CRDs and APIs.
