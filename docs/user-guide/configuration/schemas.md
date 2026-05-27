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
* `credentials`: References the name of a `kubernetes.io/basic-auth` Secret in the same namespace as the Schema CR. Required when the repository requires authentication (for example, a private repository). See [Repository authentication](#repository-authentication).
* `proxy`: Optional object that routes git traffic through an HTTP/HTTPS proxy. It has two sub-fields:
    * `url`: The full URL of the proxy server (for example `http://proxy.example.com:3128`).
    * `credentials`: The name of a `kubernetes.io/basic-auth` Secret in the same namespace, required only when the proxy server itself needs authentication.

Following the identification of schema directories and files for download, the `dirs` attribute plays a crucial role. It allows users to map each source directory to a corresponding local storage location. Essentially, dirs is an array comprising pairs of `src` (source directory) and `dst` (destination path). This setup facilitates the organization of downloaded schema files, ensuring they are stored in designated local directories for easy access and management.

If the dirs attribute is not set, it defaults to `$pwd` for both `src` and `dst`.

Some vendors publish their primary YANG files in a central repository; however, included files may reside in separate repositories. To address this, the repository definition in the Schema Custom Resource Definition (CRD) allows for the specification of multiple repositories. This setup ensures that all components contributing to the schema are accessible and properly linked, even if they are stored across different locations.

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

Reference the secret by name in the Schema CR:

```yaml
  repositories:
  - repoURL: https://github.com/example/yang-models
    credentials: personal-access-token   # name of the Secret above
    kind: tag
    ref: v1.0.0
```

### Proxy authentication

If the proxy server itself requires authentication, create a second `kubernetes.io/basic-auth` Secret and reference it in the `proxy.credentials` field:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: proxy-credentials
data:
  username: <base64-encoded-username>
  password: <base64-encoded-password>
type: kubernetes.io/basic-auth
```

Then reference both secrets in the Schema CR:

```yaml
  repositories:
  - repoURL: https://github.com/example/yang-models
    credentials: personal-access-token
    proxy:
      url: http://proxy.example.com:3128
      credentials: proxy-credentials   # omit if proxy needs no auth
    kind: tag
    ref: v1.0.0
```

!!!note "namespace"

  Proxy credential Secrets MUST use the same namespace as the Schema CR.

## Schema Identification: Naming Conventions

The schema is uniquely identified through `provider` and `version`.

* `provider`: Contains details about the schema issuer, typically including vendor and chassis type.
* `version`: Represents the specific version of the schema.

## Schema Parsing Method: Handling YANG Models

YANG schemas are comprised of several implemented models, some of which may have dependencies on other models.
The `Schema` CustomResource accommodates this complexity with specific parameters:

* `models`: Defines paths to files or directories containing the models implemented by the schema.
* `includes`: Specifies paths to models that are imported as dependencies by the implemented models.
* `excludes`: An optional list of regular expression parameters. It filters out specific models during the loading process based on matching criteria.

By carefully setting these parameters, users can seamlessly onboard devices into the SDC framework, ensuring that the schemas are accurately loaded and parsed.

## Onboarding a New Vendor/Model Schema

If your vendor/model is not yet documented, use the workflow below.

### 1. Identify the YANG source and pin a version

Choose a repository and pin a specific `tag` or `branch`.

* Use `kind: tag` whenever possible for reproducibility.
* Use `ref` to pin the exact release (for example: `OcNOS-SP-7.0.0`).

### 2. Locate model roots and dependencies

Before writing the `Schema` CR, inspect the vendor repository layout:

* Which directory contains implemented models (your `models` values).
* Which directories/files contain imported modules (your `includes` values).
* Whether you need additional repositories (for example IETF or OpenConfig base models).

Tip: if one repository does not contain all imported modules, add another `repositories` entry.

### 3. Create the Schema CR

Start with a narrow scope, then expand:

* Begin with the model set you actually need (rather than every vendor module).
* Add `includes` for dependency folders/files.
* Use `excludes` to skip known unwanted trees.

### 4. Validate locally with `sdc-lite` (primary)

Use `sdc-lite` to validate that your Schema CR definition is functional before cluster apply.

Install `sdc-lite` using the official instructions in the sdc-lite repository: [Installation](https://github.com/sdcio/sdc-lite#installation).

Quick option (latest, macOS/Linux):

```shell
go install github.com/sdcio/sdc-lite@latest
```

Load your Schema CR definition (local file):

```shell
sdc-lite schema load -t <target-name> -f <path/to/your-schema-file>.yaml
```

This command is the primary validation gate: if the Schema CR cannot be loaded (for example due to missing imports or invalid model paths), `sdc-lite` exits with a non-zero status and prints the parsing/loading error.

Inspect target details:

```shell
sdc-lite target show -t <target-name>
```

Success criteria:

* Schema load command completes without error.
* `target show` displays the expected schema `Name` and `Version`.

Optional cleanup:

```shell
sdc-lite schema remove --vendor <provider> --version <version>
```

### 5. Apply to Kubernetes (after local validation)

```shell
kubectl apply -f <your-schema-file>.yaml
kubectl get schema <schema-name> -o yaml
```

Success criteria:

* `status.conditions[type=Ready].status` is `True`.
* `provider` and `version` match what you expect.

### 6. If loading fails, iterate quickly

Typical failure categories:

* Missing imports (for example `ietf-*` or `openconfig-*`).
* Wrong model path in `models`.
* Unwanted files getting parsed (solve with `excludes`).

Typical fixes:

* Add another repository containing missing dependencies.
* Add directories/files to `includes`.
* Reduce `models` scope and onboard incrementally.

## OcNOS SP-7.0.0 (IP Infusion)

This example onboards the native `ipi-*` YANG models for OcNOS SP-7.0.0.

Source repository details:

* Repository: `https://github.com/IPInfusion/OcNOS`
* Release tag: `OcNOS-SP-7.0.0`
* Native model path: `yang-files/ipi`

The OcNOS repository does not ship the IETF base types (`ietf-inet-types`, `ietf-yang-types`) that many `ipi-*` modules import.
A second `repositories` entry pulls those from [YangModels/yang](https://github.com/YangModels/yang), following the same pattern used for Arista.

```yaml
apiVersion: inv.sdcio.dev/v1alpha1
kind: Schema
metadata:
  name: ocnos-sp.ipinfusion.sdcio.dev-7.0.0
  namespace: default
spec:
  provider: ocnos-sp.ipinfusion.sdcio.dev
  version: 7.0.0
  repositories:
  - repoURL: https://github.com/IPInfusion/OcNOS
    kind: branch
    ref: OcNOS-SP-7.0.0
    dirs:
    - src: yang-files/ipi
      dst: ipi
    schema:
      models:
      - ipi
  - repoURL: https://github.com/YangModels/yang
    kind: branch
    ref: main
    dirs:
    - src: standard/ietf/RFC
      dst: ietf
    schema:
      includes:
      - ietf/ietf-inet-types.yang
      - ietf/ietf-yang-types.yang
```

To apply:

```shell
sdc-lite schema load -t ocnos-sp-7-0-0 -f config-server-repo/example/schemas/schema-ipinfusion-ocnos-sp-7.0.0.yaml
sdc-lite target show -t ocnos-sp-7-0-0
```

Cluster apply (optional after local validation):

```shell
kubectl apply -f schema-ipinfusion-ocnos-sp-7.0.0.yaml
kubectl get schema ocnos-sp.ipinfusion.sdcio.dev-7.0.0 -o yaml
```

!!!note "Platform-specific schemas"

    SDC uses a separate Schema CR per vendor release and platform type. For a different OcNOS platform, define a new Schema with a different `provider` value (for example `ocnos-otherplatform.ipinfusion.sdcio.dev`) and adjust `models` or `excludes` to match that platform's supported feature set.

## Examples

### SR Linux v24.10.1

The below CR defines an SR Linux `Schema` version 24.10.1.

The YANG files will be retrieved from the github repo `https://github.com/nokia/srlinux-yang-models` tag `v24.10.1`.
The remote directory `srlinux-yang-models` at the root level of the git repository will be mapped to `$pwd` (`dst: .`) in the local file system

```yaml
--8<--
config-server-repo/example/schemas/schema-nokia-srl-24.10.1.yaml
--8<--
```

To apply the CR, store the above content in a file (e.g: `srlinux_24.10.1_schema.yaml`) and run the command:

```shell
kubectl apply -f srlinux_24.10.1_schema.yaml
```

After applying the previous CR to a kubernetes cluster, the `Schema` can be viewed with the commands:

```shell
kubectl get schemas.inv.sdcio.dev
```

```shell
kubectl get schemas srl.nokia.sdcio.dev-24.10.1 -o yaml
```

Sample outputs:

```shell
$ kubectl get schemas.inv.sdcio.dev
NAME                          READY   PROVIDER              VERSION   URL                                            REF
srl.nokia.sdcio.dev-24.10.1   True    srl.nokia.sdcio.dev   24.10.1   https://github.com/nokia/srlinux-yang-models   v24.10.1
```

```shell
$ kubectl get schemas srl.nokia.sdcio.dev-24.10.1 -o yaml
apiVersion: inv.sdcio.dev/v1alpha1
kind: Schema
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"inv.sdcio.dev/v1alpha1","kind":"Schema","metadata":{"annotations":{},"name":"srl.nokia.sdcio.dev-24.10.1","namespace":"default"},"spec":{"provider":"srl.nokia.sdcio.dev","repositories":[{"dirs":[{"dst":".","src":"srlinux-yang-models"}],"kind":"tag","ref":"v24.10.1","repoURL":"https://github.com/nokia/srlinux-yang-models","schema":{"excludes":[".*tools.*"],"includes":["ietf","openconfig/extensions","openconfig/openconfig-extensions.yang"],"models":["srl_nokia/models"]}},{"dirs":[{"dst":"deviations","src":"."}],"kind":"branch","ref":"v24.10","repoURL":"https://github.com/sdcio/srlinux-yang-patch","schema":{"models":["deviations"]}}],"version":"24.10.1"}}
  creationTimestamp: "2025-01-14T13:44:35Z"
  finalizers:
  - schema.inv.sdcio.dev/finalizer
  generation: 1
  name: srl.nokia.sdcio.dev-24.10.1
  namespace: default
  resourceVersion: "1357"
  uid: 17eaf452-1cae-4286-afc6-a0c0e051e0c4
spec:
  provider: srl.nokia.sdcio.dev
  repositories:
  - dirs:
    - dst: .
      src: srlinux-yang-models
    kind: tag
    ref: v24.10.1
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
  - dirs:
    - dst: deviations
      src: .
    kind: branch
    ref: v24.10
    repoURL: https://github.com/sdcio/srlinux-yang-patch
    schema:
      models:
      - deviations
  version: 24.10.1
status:
  conditions:
  - lastTransitionTime: "2025-01-14T13:44:42Z"
    message: ""
    reason: Ready
    status: "True"
    type: Ready
```

### SROS 24.10.1

```yaml
--8<--
config-server-repo/example/schemas/schema-nokia-sros-24.10.yaml
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

### Arista EOS 4.31.1F

```yaml
--8<--
config-server-repo/example/schemas/schema-arista-4.31.1f.yaml
--8<--
```

### Arista EOS 4.33.0F

```yaml
--8<--
config-server-repo/example/schemas/schema-arista-4.33.0f.yaml
--8<--
```