# Schema

The initial step in integrating a device with SDC involves importing the device's schema.
SDC is equipped to handle YANG schemas, provided all necessary model files and their respective dependencies are available in a git repository.
This process is facilitated through the Schema CustomResource, detailed [here](link to CRD).

The Schema CustomResource is configured using three main parameter groups:

1. __Source of Schema__: Determined by `repoURL`, `kind`, and `ref` parameters.
2. __Schema Identification__: Specified using `provider` and `version` parameters.
3. __Schema Parsing Method__: Configured through `models`, `includes`, and `excludes` parameters.

## Source of Schema: Repository Configuration

To successfully retrieve the schema, it is essential for users to provide four key parameters: `repoURL`, `kind`, `ref` and `credentials`.
These parameters jointly establish the methodology for schema acquisition:

* `repoURL`: This parameter is pivotal as it specifies the repository's URL where the schema is located.
* `kind`: It determines the nature of the reference point within the repository, offering options between a "tag" or a "branch".
* `ref`: This parameter is closely linked to kind and pinpoints the exact tag or branch name within the repository.
* `credentials`: This parameter is point to a secret name in the same namespace as the `schema` CR. It is required if your repository requires authentication e.g. a private repo.

Following the identification of schema directories and files for download, the `dirs` attribute plays a crucial role. It allows users to map each source directory to a corresponding local storage location. Essentially, dirs is an array comprising pairs of `src` (source directory) and `dst` (destination path). This setup facilitates the organization of downloaded schema files, ensuring they are stored in designated local directories for easy access and management.

If the dirs attribute is not set, it defaults to `$pwd` for both `src` and `dst`.

## Repository authentication

If your schema repository requires authentication a secret of type `kubernetes.io/basic-auth` is referenced in the schema CR. An Example of such secret is provided below.

!!!note "username/password"

  Please fill out your own username and password/token

!!!note "namespace"

  The secret MUST use the same namespace as the schema CR that is referencing it.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: personal-access-token
data:
  username: <base64-encoded-username>
  password: <base64-encoded-password>
type: kubernetes.io/basic-auth
```

## Schema Identification: Naming Conventions

The schema is uniquely identified through `provider` and `version`.

* `provider`: Contains details about the schema issuer, typically including vendor and chassis type.
* `version`: Represents the specific version of the schema.

## Schema Parsing Method: Handling YANG Models

YANG schemas are comprised of several implemented models, some of which may have dependencies on other models.
The `Schema`` CustomResource accommodates this complexity with specific parameters:

* `models`: Defines paths to files or directories containing the models implemented by the schema.
* `includes`: Specifies paths to models that are imported as dependencies by the implemented models.
* `excludes`: An optional list of regular expression parameters. It filters out specific models during the loading process based on matching criteria.

By carefully setting these parameters, users can seamlessly onboard devices into the SDC framework, ensuring that the schemas are accurately loaded and parsed.

## Examples

### SR Linux v23.10.1

The below CR defines an SR Linux `Schema` version 23.10.1.

The YANG files will be retrieved from the github repo `https://github.com/nokia/srlinux-yang-models` tag `v23.10.1`.
The remote directory `srlinux-yang-models` at the roo level of the git repository will be mapped to `$pwd` (`dst: .`) in the local file system

```yaml
--8<--
config-server-repo/example/schemas/schema-nokia-srl-23.10.1.yaml
--8<--
```

To apply the CR, store the above content in a file (e.g: `srlinux_23.10.1_schema.yaml`) and run the command:

```shell
kubectl apply -f srlinux23.10.1_schema.yaml
```

After applying the previous CR to a kubernetes cluster, the `Schema` can be viewed with the commands:

```shell
kubectl get schemas.inv.sdcio.dev
```

```shell
kubectl get schemas srl.nokia.sdcio.dev-23.10.1 -o yaml
```

Sample outputs:

```shell
$ kubectl get schemas.inv.sdcio.dev
NAME                           READY   URL                                            REF             PROVIDER               VERSION
srl.nokia.sdcio.dev-23.10.1    True    https://github.com/nokia/srlinux-yang-models   v23.10.1        srl.nokia.sdcio.dev    23.10.1
```

```shell
$ kubectl get schemas srl.nokia.sdcio.dev-23.10.1 -o yaml
apiVersion: inv.sdcio.dev/v1alpha1
kind: Schema
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"inv.sdcio.dev/v1alpha1","kind":"Schema","metadata":{"annotations":{},"name":"srl.nokia.sdcio.dev-23.10.1","namespace":"default"},"spec":{"dirs":[{"dst":".","src":"srlinux-yang-models"}],"kind":"tag","provider":"srl.nokia.sdcio.dev","ref":"v23.10.1","repoURL":"https://github.com/nokia/srlinux-yang-models","schema":{"excludes":[".*tools.*"],"includes":["ietf","openconfig/extensions","openconfig/openconfig-extensions.yang"],"models":["srl_nokia/models"]},"version":"23.10.1"}}
  creationTimestamp: "2024-01-09T23:05:13Z"
  finalizers:
  - schema.inv.sdcio.dev/finalizer
  generation: 1
  name: srl.nokia.sdcio.dev-23.10.1
  namespace: default
  resourceVersion: "872"
  uid: 8b533cc2-38fa-4487-965d-3877beb455fc
spec:
  dirs:
  - dst: .
    src: srlinux-yang-models
  kind: tag
  provider: srl.nokia.sdcio.dev
  ref: v23.10.1
  repoURL: https://github.com/nokia/srlinux-yang-models
  schema:
    excludes:
    - .*tools.*
    includes:
    - ietf
    - openconfig/extensions
    - openconfig/openconfig-extensions.yang
    models:
    - srl_nokia/models
  version: 23.10.1
status:
  conditions:
  - lastTransitionTime: "2024-01-09T23:05:16Z"
    message: ""
    reason: Ready
    status: "True"
    type: Ready
```

### SROS 23.10.2

```yaml
--8<--
config-server-repo/example/schemas/schema-nokia-sros-23.10.yaml
--8<--
```

### Juniper MX 23.2R1

```yaml
--8<--
config-server-repo/example/schemas/schema-juniper-mx-23.2R1.yaml
--8<--
```

### Juniper QFX 23.2R1

```yaml
--8<--
config-server-repo/example/schemas/schema-juniper-qfx-23.2R1.yaml
--8<--
```

### Juniper EX 23.2R1

```yaml
--8<--
config-server-repo/example/schemas/schema-juniper-ex-23.2R1.yaml
--8<--
```

### Juniper NFX 23.2R1

```yaml
--8<--
config-server-repo/example/schemas/schema-juniper-nfx-23.2R1.yaml
--8<--
```