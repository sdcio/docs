# Cache

## Overview

The cache is a multi-instance, intent-blob store. Each cache instance corresponds to one datastore (target device) and holds a set of named intent blobs — serialised [`tree_persist.Intent`](https://github.com/sdcio/sdc-protos/blob/main/tree_persist.proto) protobuf messages.

The cache is a **pure persistence layer**. It has no understanding of config tree structure, priority resolution, or candidate/running separation. All of that logic lives in data-server's `pkg/tree` package. In production, data-server embeds the cache directly via the `LocalCache` adapter (an in-process Go call), making the standalone gRPC server unnecessary for the current deployment.

A standalone gRPC server is provided for out-of-process or experimental deployments but is not used by default.

---

## Data Model: Config Trees

### Cache instances

One cache instance maps to one datastore. The instance name equals the datastore name. Instances are managed by `pkg/cache.Cache` and kept in an internal `map[string]*cacheInstance`.

### Intent blobs

Each named intent is stored as a raw `[]byte` — the result of `proto.Marshal` applied to a `tree_persist.Intent` message. A blob contains:

- `intent_name` — string key (e.g. `"my-interface-config"`, `"running"`)
- `priority` — int32; lower value = higher precedence
- All path+value updates belonging to this intent, encoded as a tree

There is no partial update: every write replaces the entire blob for that intent name.

---

## Intent Ownership & Priority

Priority is an `int32` embedded in the `tree_persist.Intent` blob. The cache stores this value as-is without interpretation. Intent ownership, priority semantics, and conflict resolution are managed by data-server, not the cache.

---

## Write Path

All writes originate in data-server.

1. data-server computes new intent content in `pkg/tree` using a deep-copied candidate tree derived from `syncTree`.
2. Calls `ops.TreeExport(root.Entry, intentName, priority, onlyIntended)` to serialise the intent subtree to a `tree_persist.Intent` proto.
3. Calls `cacheClient.IntentModify(ctx, intent)`.
4. `LocalCache.InstanceIntentModify` marshals the proto: `proto.Marshal(intent)` → `[]byte`.
5. `cache.InstanceIntentModify(ctx, name, bytes)` → `store.IntentModify(ctx, intentName, bytes)` → `os.WriteFile(...)`.


### Running-config writeback

After every successful `TransactionSet`, data-server calls `writeBackSyncTree`:

1. Exports the entire `syncTree` as intent `"running"` via `ops.TreeExport`.
2. Writes it to cache with `IntentModify("running", ...)`.

This keeps the persisted `"running"` blob aligned with the committed in-memory tree for fast follow-up operations (for example replace-intent baselining); cold-start still rebuilds state from user intents and excludes `"running"` from bulk load.

---

## Read Path & Subscriptions

### Cold-start / datastore startup

On datastore initialisation, data-server calls `LoadAllButRunningIntents`:

1. `cacheClient.IntentGetAll(ctx, []string{"running"}, intentChan, errChan)` — streams all intent blobs except `"running"`.
2. Each blob is unmarshalled (`proto.Unmarshal` → `tree_persist.Intent`) and loaded into a working tree (deep-copied from `syncTree`) via `root.ImportConfig()` using `treeproto.NewProtoTreeImporter`.

The `"running"` blob is excluded from the bulk load because the running config is recomputed from the deep-copied `syncTree` after the loaded user intents have been imported into it.

### Replace-intent transactions

Before applying a replace-intent, data-server calls `cacheClient.IntentGet(ctx, "running")` to retrieve the current running snapshot. This is used to populate the base tree so the replace diff can be computed correctly.

---

## Persistence

### Filesystem store (default)

Implemented in `pkg/store/filesystem/filesystem.go`.

```
<basepath>/
  <cacheName>/
    intents/
      <intentName>/
        data    ← raw proto bytes (tree_persist.Intent)
```

- One directory per intent; the file is always named `data`.
- Writes use `os.WriteFile` under a mutex. There is no write-ahead log.
- Delete removes the entire `<intentName>` directory via `os.RemoveAll`.


### Volume and durability

The `cache` volume in the data-server StatefulSet is an **`emptyDir`**. All persisted intent blobs are lost on pod restart.

On cold start, config-server detects the empty state and re-applies all `Config` and `ConfigSet` resources. This drives data-server to rebuild every intent blob, restoring the cache to the pre-restart state.

---

## Configuration & Deployment

### Embedded (data-server) configuration

| Key | Default | Description |
|---|---|---|
| `cache.type` | `local` | `local` — embedded via `LocalCache`; `remote` — standalone gRPC server |
| `cache.store-type` | `filesystem` | `filesystem` or `badgerdb` |
| `cache.dir` | `./cached/caches` | Base path for the filesystem store |
| `cache.address` | `:50100` | Address of the remote cache server (only used when `type: remote`) |

### Standalone server flags

Relevant when running the cache as an independent process:

| Flag | Default | Description |
|---|---|---|
| `--config` / `-c` | `cache.yaml` | Path to config file |
| `--debug` / `-d` | — | Enable debug log level |
| `--trace` / `-t` | — | Enable trace log level |
| `--version` / `-v` | — | Print version and exit |

The standalone gRPC service listens on `:50100` (overridable via `grpc-server.address`).

### Adapter layer (data-server)

data-server never calls `pkg/cache.Cache` directly. It uses two adapter types:

- **`LocalCache`** (`data-server/pkg/cache/local.go`) — implements the `Client` interface by calling `cache.Cache` in-process. Responsible for `proto.Marshal` / `proto.Unmarshal` of [`tree_persist.Intent`](https://github.com/sdcio/sdc-protos/blob/main/tree_persist.proto).
- **`CacheClientBound`** (`data-server/pkg/cache/cacheClientBound.go`) — wraps `Client` with a fixed `cacheName`, exposing short-form methods (`IntentGet`, `IntentModify`, etc.) that datastore code calls directly.

---

## Interactions

| Direction | Component | Mechanism | Purpose |
|---|---|---|---|
| Inbound | data-server | Direct Go calls via `LocalCache` → `cache.Cache` | All intent read / write / delete operations |
| Inbound (standalone) | External clients | gRPC `:50100` | Standalone mode — not used in current deployment |
| Outbound | Filesystem | `os.WriteFile` / `os.ReadFile` | Durable intent storage at `/cached/caches/` |
| Outbound (optional) | BadgerDB | `badger.DB.*` | Alternative storage backend — not default |

### gRPC API reference ([`cache.proto`](https://github.com/sdcio/cache/blob/main/proto/cache.proto))

| RPC | Description |
|---|---|
| `InstanceCreate` | Create a new cache instance |
| `InstanceDelete` | Delete a cache instance and all its intents |
| `InstancesList` | List all cache instance names |
| `InstanceIntentsList` | List all intent names in an instance |
| `InstanceIntentGet` | Retrieve a single intent blob by name |
| `InstanceIntentModify` | Write or overwrite a single intent blob |
| `InstanceIntentDelete` | Delete a single intent by name |
| `InstanceIntentExists` | Check whether an intent exists |
| `InstanceIntentsGetAll` | Stream all intents, optionally excluding named ones |

`InstanceClose` and `InstanceExists` exist in data-server's `Client` interface but are adapter-only methods — they have no corresponding gRPC RPC definition.
