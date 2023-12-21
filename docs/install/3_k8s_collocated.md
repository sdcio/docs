<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

First ensure the [pre-requisites](2_prereq.md) are met

## Install SDC Components

Once the cluster is deployed we install the `sdc` components. These manifests deploy sdc as a deployment where the pod contains 2 containers:

1. the config-server container with the various controllers
2. the data-server/schema-server/cache collocated in a single container

```yaml
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: network-system
---
kind: ServiceAccount
apiVersion: v1
metadata:
  name: config-apiserver
  namespace: network-system
---
apiVersion: v1
kind: Service
metadata:
  name: capis
  namespace: network-system
spec:
  ports:
  - port: 6443
    protocol: TCP
    targetPort: 6443
  selector:
    config-apiserver: "true"
---
apiVersion: v1
kind: Secret
type: kubernetes.io/tls
metadata:
  name: capis
  namespace: network-system
  labels:
    config-apiserver: "true"
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURZekNDQWt1Z0F3SUJBZ0lJSC9mSFZHenZ3cnN3RFFZSktvWklodmNOQVFFTEJRQXdaVEVMTUFrR0ExVUUKQmhNQ2RXNHhDekFKQmdOVkJBZ01Bbk4wTVFvd0NBWURWUVFIREFGc01Rb3dDQVlEVlFRS0RBRnZNUXN3Q1FZRApWUVFMREFKdmRURWtNQ0lHQTFVRUF3d2JZbUZ6YVdNdFkyVnlkR2xtYVdOaGRHVXRZWFYwYUc5eWFYUjVNQjRYCkRUSXlNRE16TVRBNU1UYzFNMW9YRFRNeU1ETXlPREE1TVRjMU5Gb3dIREVhTUJnR0ExVUVBeE1SWW1GemFXTXUKWkdWbVlYVnNkQzV6ZG1Nd2dnRWlNQTBHQ1NxR1NJYjNEUUVCQVFVQUE0SUJEd0F3Z2dFS0FvSUJBUUN0TUt0eApjc3Rjdk8rdDVMazZRQkRBZ3g1akZCL2F1dStVb3BDR2Z6VitaRW5obldpaC8xMVZ2ek44cjhmdGZuUkZGTVZ6CmJqYlVhSXNDOFc1eGJDNXNpc2VrdnVBWDlpanUzMlFybEU0RTR1UzNYREdVZkhGSFhMcWxBRU9RclUvRzQ0RGgKa0I3ajJOcDRzbk9IckF0aDA3TStvbXBmVklhSTlkQmdYY3hsUE5QRkNNamlOb1VweVM4eXNha3RQRXFjZTBpawpmNDBYVERmN1YwekFFelI0QkE4Yzh0b05UMVNnSXFIV0xueERKcnZRempDaTVFN2NMNkpmTmhlZDQ5MUVNWlEwCmVnbkV5bXd6d1Jya3BYTkZ4RHJzSXpOZmhHelB6RGJLdmFIUHh5NUwvM3h3clZ3VHllbklaOVExK0tjemtCSksKRXZIaVVKL1BML0VYZkloakFnTUJBQUdqWURCZU1BNEdBMVVkRHdFQi93UUVBd0lGb0RBZEJnTlZIU1VFRmpBVQpCZ2dyQmdFRkJRY0RBUVlJS3dZQkJRVUhBd0l3TFFZRFZSMFJCQ1l3SklJSmJHOWpZV3hvYjNOMGdoRmlZWE5wCll5NWtaV1poZFd4MExuTjJZNGNFZndBQUFUQU5CZ2txaGtpRzl3MEJBUXNGQUFPQ0FRRUFEa1hsbGZMTlpzWDEKYmp1b0h4RXVUWitaODlMWUxPUDBMM0dHMFgwdVdkZzJFcXY1bmZNRHVRVmJIRmt5dVo3ZDlDY01QYk12MTdDWgoxZGwwQk1GQTJkTkJzK3V1UXFIUFh3RkI4SFdPSDhBc1pMMnYvbG91T3g2dU1QQk9uWUhuQ3pFY21FQXZoR2dLCkpXMDNkd2QwNlJPeUdLT29qSklFTlRnd0xnQ1dZSytPWmIzQklyMUJqS012Q2dHN3pJVDFUUVNna3hGN1NGNzUKYk5BaEdOa0NWMGVrSnNXQWk1UGhzVS9IdWthdGVHUGNMS3hia0RGdHpSV2tRNmdKUXhkZmVuOVBKTjVJVCt4RQpFci8wYUkrOFM5Y1FPUnk0VTNDSFRodmlnOGFyZ3FucmFWMU92OXZNTWxzZ3pnYXc3SjdaeGtkWWwrSkMyWUcvCjJrUThVd1IzQnc9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
  tls.key: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBclRDcmNYTExYTHp2cmVTNU9rQVF3SU1lWXhRZjJycnZsS0tRaG44MWZtUko0WjFvCm9mOWRWYjh6ZksvSDdYNTBSUlRGYzI0MjFHaUxBdkZ1Y1d3dWJJckhwTDdnRi9Zbzd0OWtLNVJPQk9Ma3Qxd3gKbEh4eFIxeTZwUUJEa0sxUHh1T0E0WkFlNDlqYWVMSnpoNndMWWRPelBxSnFYMVNHaVBYUVlGM01aVHpUeFFqSQo0amFGS2Nrdk1yR3BMVHhLbkh0SXBIK05GMHczKzFkTXdCTTBlQVFQSFBMYURVOVVvQ0toMWk1OFF5YTcwTTR3Cm91Uk8zQytpWHpZWG5lUGRSREdVTkhvSnhNcHNNOEVhNUtWelJjUTY3Q016WDRSc3o4dzJ5cjJoejhjdVMvOTgKY0sxY0U4bnB5R2ZVTmZpbk01QVNTaEx4NGxDZnp5L3hGM3lJWXdJREFRQUJBb0lCQUJWWU16ajNLZU1URWdMLwpkbWljYnJRYk5NcUhOMm5Rc2loQ1pNZCt0QXdRdGg1Tk5SRUtGT20xZDlYOUlBbkFGUHBTbGdjazVUTUdjMk40CmQrRVlzUndGZXBkdVF0WVJLM2hOSmQ1TkY5UjRWakhXOWZGVDZPNGZtbzB0WENaZmhiNkFXV2p6Unl0VGxaRmMKaE9xS3BKaDQ2OVZqVlBMTXl3dmtKN3RJdENFaHl4b0t0VVhwcm45SXBLNnNUa051OTFmMVA4czJNbDd1RlVqYwpJdGhMb3JnMEYyU3RaeEJmVDJGaFRYaFZxRlRJS1pmazFGbnRpbUwyWlQrRXZzQlpnZHYwa2Z1Q2hFdE5jRW1PCnRZc2dKT3ExTWF5M2d0dlk3VDB6WkRtTTIrOVpKQ0JLcm8yV2IxdGw0RHNnaWNkR0I2SlhnTi81aklSMTNmbDUKMTRJd1hza0NnWUVBemtQb1MrTko0QkJkR3RYem5tZWVhRFFQVVU0dkF1R3YyU2VtajR3RG1KRXB6aDdoMWlQZAprVWxmYjcxZ1VMbmk0SDVkVFlyVFpwOElUaXZvM3A1bUNrV3lFV09wMmx4VUZoM3JnVWN6NWt0RUhkejl1bjNoCnFYNVJpTWlkM0Y3dWRIODdqYTdJVi9mUEFGSnlremQrWHNaZGFuT0tPK1UvV0t2ek0rSFEzUThDZ1lFQTF2TWoKdml3dnFxM0FBa0VpN2RlOUxLUE1uS1N5VE9BdHQzS2dqV1RLNU5aQUdqeWpoSGxEbjRCempSS25DWk8xY0lJZwo0Wnl1VzQrUlB5aGQreEFubzVoMVh0Ny9LYzNFaW1ucjBLU0ZmRWVza2NORFIyVHNTdCtjYTl6aFFPTFJ0TWRCCnE5OWZDeFprK1pmcEhpSzJCK0pHVExNdVJRY0tDYU43RldKTkIyMENnWUJhc2k5bGx3WjMySm9uMzZYa3BDbGEKSm5JSnpUZ01xMUlZU1VBSzVJVDhRL0ErNndOZ2xwcXBkTHJiTmtrd2xkdjEzSHFJU3gvVGd1QXpCMG01QWF0YQpudlRDZ3JGQUM5TUplcFNBWHQrcVJyUW44WEU3M0hncWdCbTM3SWJGVEpUTGN0cXIzUXZJNm5VQjdqN2xEc1NwClJjM3pyZVE5bS9yenNZQVo4eFJVN3dLQmdRQ0JYTjg4Q3JlOVRzaHFFdTJFbXZ4ZEswOXZUcWVJSUxzaTFyZk4Kb01XREozWjQwOW5OVm5YZVBwNU1YdGRzcWhyZVZWS1l0WVV4MFp1bW1STEdrSmhxbXN5NGhoaW0vaEcxQTc1SwpXVm1FekZZTmU2aTRCUU00cEk4dFUwZTFsMHlDTWhGUjhTTHdOMUFaN3RUN3NBUkJobXFzcW9IRVJWSkRMc0phCndraDltUUtCZ0NYR2xoZzY4aVMzMldmSWVtYUFRMTJpNFRUUk1FNWppTFl0ZlkyREJTMDBWV3NxY0l1OEFUWm0KVHVoZHBRVG9mKzE3LzFyU0cyYnFaWFA2L0h3ak14OTVIdWlXbjVKSjA3RTduOUVCUDlkQTY0K0lHdWlvd0h5RAo2a3g3VVhuTUtTYXdiV2JxZ1JGZTFOZEdLbkh0ZE5GOGxndEdjdytxUTk3YkIreXFreXMxCi0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0tCg==
---
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  annotations:
    controller-gen.kubebuilder.io/version: v0.12.1
  name: discoveryrules.inv.sdcio.dev
spec:
  group: inv.sdcio.dev
  names:
    categories:
    - sdc
    - inv
    kind: DiscoveryRule
    listKind: DiscoveryRuleList
    plural: discoveryrules
    singular: discoveryrule
  scope: Namespaced
  versions:
  - additionalPrinterColumns:
    - jsonPath: .status.conditions[?(@.type=='Ready')].status
      name: READY
      type: string
    name: v1alpha1
    schema:
      openAPIV3Schema:
        description: DiscoveryRule is the Schema for the DiscoveryRule API
        properties:
          apiVersion:
            description: 'APIVersion defines the versioned schema of this representation
              of an object. Servers should convert recognized schemas to the latest
              internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources'
            type: string
          kind:
            description: 'Kind is a string value representing the REST resource this
              object represents. Servers may infer this from the endpoint the client
              submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds'
            type: string
          metadata:
            type: object
          spec:
            description: DiscoveryRuleSpec defines the desired state of DiscoveryRule
            properties:
              concurrentScans:
                default: 10
                description: number of concurrent IP scan
                format: int64
                type: integer
              discover:
                description: Discovery rule defines the profiles and templates generic
                  to any discovery rule class/type Discover defines if discovery is
                  enabled or not
                type: boolean
              discoveryProfile:
                description: DiscoveryProfile define the profiles the discovery controller
                  uses to discover targets
                properties:
                  connectionProfiles:
                    description: ConnectionProfiles define the list of profiles the
                      discovery controller uses to discover the target. The order
                      in which they are specified is the order in which discovery
                      is executed.
                    items:
                      type: string
                    type: array
                  credentials:
                    description: Credentials defines the name of the secret that holds
                      the credentials to connect to the target
                    type: string
                  tlsSecret:
                    description: TLSSecret defines the name of the TLS secret to connect
                      to the target if mtls is used
                    type: string
                required:
                - connectionProfiles
                - credentials
                type: object
              kind:
                default: ip
                enum:
                - unknown
                - ip
                - pod
                - svc
                type: string
              period:
                default: 1m
                description: Period defines the wait period between discovery rule
                  runs
                type: string
              prefixes:
                description: IP Prefixes for which this discovery rule applies
                items:
                  properties:
                    excludes:
                      description: IP Prefixes to be excluded
                      items:
                        type: string
                      type: array
                    hostName:
                      description: HostName of the ip prefix; used for /32 or /128
                        addresses with discovery disabled
                      type: string
                    prefix:
                      description: Prefix of the target/target(s)
                      type: string
                  required:
                  - prefix
                  type: object
                type: array
              selector:
                description: Selector defines the selector used to select which POD/SVC
                  are subject to this discovery rule
                properties:
                  matchExpressions:
                    description: matchExpressions is a list of label selector requirements.
                      The requirements are ANDed.
                    items:
                      description: A label selector requirement is a selector that
                        contains values, a key, and an operator that relates the key
                        and values.
                      properties:
                        key:
                          description: key is the label key that the selector applies
                            to.
                          type: string
                        operator:
                          description: operator represents a key's relationship to
                            a set of values. Valid operators are In, NotIn, Exists
                            and DoesNotExist.
                          type: string
                        values:
                          description: values is an array of string values. If the
                            operator is In or NotIn, the values array must be non-empty.
                            If the operator is Exists or DoesNotExist, the values
                            array must be empty. This array is replaced during a strategic
                            merge patch.
                          items:
                            type: string
                          type: array
                      required:
                      - key
                      - operator
                      type: object
                    type: array
                  matchLabels:
                    additionalProperties:
                      type: string
                    description: matchLabels is a map of {key,value} pairs. A single
                      {key,value} in the matchLabels map is equivalent to an element
                      of matchExpressions, whose key field is "key", the operator
                      is "In", and the values array contains only "value". The requirements
                      are ANDed.
                    type: object
                type: object
                x-kubernetes-map-type: atomic
              targetConnectionProfiles:
                description: TargetConnectionProfiles define the profile the discovery
                  controller uses to create targets once discovered
                items:
                  properties:
                    connectionProfile:
                      description: ConnectionProfile define the profile used to connect
                        to the target once discovered
                      type: string
                    credentials:
                      description: Credentials defines the name of the secret that
                        holds the credentials to connect to the target
                      type: string
                    defaultSchema:
                      description: DefaultSchema define the default schema used to
                        connect to a target Used when discovery is disabled or when
                        discovery is unsuccessful.
                      properties:
                        provider:
                          description: Provider specifies the provider of the schema.
                          type: string
                        version:
                          description: Version defines the version of the schema
                          type: string
                      required:
                      - provider
                      - version
                      type: object
                    syncProfile:
                      description: SyncProfile define the profile used to sync to
                        the target config once discovered
                      type: string
                    tlsSecret:
                      description: TLSSecret defines the name of the TLS secret to
                        connect to the target if mtls is used
                      type: string
                  required:
                  - connectionProfile
                  - credentials
                  type: object
                type: array
              targetTemplate:
                description: TargetTemplate defines the template the discovery controller
                  uses to create the targets as a result of the discovery
                properties:
                  annotations:
                    additionalProperties:
                      type: string
                    description: Annotations is a key value map to be copied to the
                      target CR.
                    type: object
                  labels:
                    additionalProperties:
                      type: string
                    description: Labels is a key value map to be copied to the target
                      CR.
                    type: object
                  nameTemplate:
                    description: target name template
                    type: string
                    x-kubernetes-validations:
                    - message: nameTemplate is immutable
                      rule: self == oldSelf
                type: object
            required:
            - discover
            - kind
            - period
            - targetConnectionProfiles
            type: object
          status:
            description: DiscoveryRuleStatus defines the observed state of DiscoveryRule
            properties:
              conditions:
                description: Conditions of the resource.
                items:
                  properties:
                    lastTransitionTime:
                      description: lastTransitionTime is the last time the condition
                        transitioned from one status to another. This should be when
                        the underlying condition changed.  If that is not known, then
                        using the time when the API field changed is acceptable.
                      format: date-time
                      type: string
                    message:
                      description: message is a human readable message indicating
                        details about the transition. This may be an empty string.
                      maxLength: 32768
                      type: string
                    observedGeneration:
                      description: observedGeneration represents the .metadata.generation
                        that the condition was set based upon. For instance, if .metadata.generation
                        is currently 12, but the .status.conditions[x].observedGeneration
                        is 9, the condition is out of date with respect to the current
                        state of the instance.
                      format: int64
                      minimum: 0
                      type: integer
                    reason:
                      description: reason contains a programmatic identifier indicating
                        the reason for the condition's last transition. Producers
                        of specific condition types may define expected values and
                        meanings for this field, and whether the values are considered
                        a guaranteed API. The value should be a CamelCase string.
                        This field may not be empty.
                      maxLength: 1024
                      minLength: 1
                      pattern: ^[A-Za-z]([A-Za-z0-9_,:]*[A-Za-z0-9_])?$
                      type: string
                    status:
                      description: status of the condition, one of True, False, Unknown.
                      enum:
                      - "True"
                      - "False"
                      - Unknown
                      type: string
                    type:
                      description: type of condition in CamelCase or in foo.example.com/CamelCase.
                        --- Many .condition.type values are consistent across resources
                        like Available, but because arbitrary conditions can be useful
                        (see .node.status.conditions), the ability to deconflict is
                        important. The regex it matches is (dns1123SubdomainFmt/)?(qualifiedNameFmt)
                      maxLength: 316
                      pattern: ^([a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*/)?(([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9])$
                      type: string
                  required:
                  - lastTransitionTime
                  - message
                  - reason
                  - status
                  - type
                  type: object
                type: array
              startTime:
                description: StartTime identifies when the dr got started
                format: date-time
                type: string
            type: object
        type: object
    served: true
    storage: true
    subresources:
      status: {}
---
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  annotations:
    controller-gen.kubebuilder.io/version: v0.12.1
  name: schemas.inv.sdcio.dev
spec:
  group: inv.sdcio.dev
  names:
    categories:
    - sdc
    - inv
    kind: Schema
    listKind: SchemaList
    plural: schemas
    singular: schema
  scope: Namespaced
  versions:
  - additionalPrinterColumns:
    - jsonPath: .status.conditions[?(@.type=='Ready')].status
      name: READY
      type: string
    - jsonPath: .spec.repoURL
      name: URL
      type: string
    - jsonPath: .spec.ref
      name: REF
      type: string
    - jsonPath: .spec.provider
      name: PROVIDER
      type: string
    - jsonPath: .spec.version
      name: VERSION
      type: string
    name: v1alpha1
    schema:
      openAPIV3Schema:
        description: Schema is the Schema for the Schema API
        properties:
          apiVersion:
            description: 'APIVersion defines the versioned schema of this representation
              of an object. Servers should convert recognized schemas to the latest
              internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources'
            type: string
          kind:
            description: 'Kind is a string value representing the REST resource this
              object represents. Servers may infer this from the endpoint the client
              submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds'
            type: string
          metadata:
            type: object
          spec:
            description: SchemaSpec defines the desired state of Schema
            properties:
              dirs:
                description: Dirs defines the list of directories that identified
                  the provider schema in src/dst pairs relative within the repository
                items:
                  description: SrcDstPath provide a src/dst pair for the loader to
                    download the schema from a specific src in the repository to a
                    given destination in the schema server
                  properties:
                    dst:
                      description: Dst is the relative directory in the schema server
                      type: string
                    src:
                      description: Src is the relative directory in the repository
                        URL
                      type: string
                  required:
                  - dst
                  - src
                  type: object
                maxItems: 10
                type: array
                x-kubernetes-validations:
                - message: dirs is immutable
                  rule: oldSelf.all(x, x in self)
              kind:
                description: Kind defines the that the BranchOrTag string is a repository
                  branch or a tag
                enum:
                - branch
                - tag
                type: string
              provider:
                description: Provider specifies the provider of the schema.
                type: string
                x-kubernetes-validations:
                - message: provider is immutable
                  rule: self == oldSelf
              ref:
                description: Ref defines the branch or tag of the repository corresponding
                  to the provider schema version
                type: string
                x-kubernetes-validations:
                - message: ref is immutable
                  rule: self == oldSelf
              repoURL:
                description: URL specifies the base URL for a given repository
                type: string
                x-kubernetes-validations:
                - message: url is immutable
                  rule: self == oldSelf
              schema:
                description: Schema provides the details of which files must be used
                  for the models and which files/directories cana be excludes
                properties:
                  excludes:
                    description: Excludes defines the list of files/directories to
                      be excluded
                    items:
                      type: string
                    maxItems: 64
                    type: array
                    x-kubernetes-validations:
                    - message: excludes is immutable
                      rule: oldSelf.all(x, x in self)
                  includes:
                    description: Excludes defines the list of files/directories to
                      be excluded
                    items:
                      type: string
                    maxItems: 64
                    type: array
                    x-kubernetes-validations:
                    - message: includes is immutable
                      rule: oldSelf.all(x, x in self)
                  models:
                    description: Models defines the list of files/directories to be
                      used as a model
                    items:
                      type: string
                    maxItems: 64
                    type: array
                    x-kubernetes-validations:
                    - message: models is immutable
                      rule: oldSelf.all(x, x in self)
                required:
                - excludes
                - includes
                - models
                type: object
              version:
                description: Version defines the version of the schema
                type: string
                x-kubernetes-validations:
                - message: version is immutable
                  rule: self == oldSelf
            required:
            - dirs
            - kind
            - provider
            - ref
            - repoURL
            - schema
            - version
            type: object
          status:
            description: SchemaStatus defines the observed state of Schema
            properties:
              conditions:
                description: Conditions of the resource.
                items:
                  properties:
                    lastTransitionTime:
                      description: lastTransitionTime is the last time the condition
                        transitioned from one status to another. This should be when
                        the underlying condition changed.  If that is not known, then
                        using the time when the API field changed is acceptable.
                      format: date-time
                      type: string
                    message:
                      description: message is a human readable message indicating
                        details about the transition. This may be an empty string.
                      maxLength: 32768
                      type: string
                    observedGeneration:
                      description: observedGeneration represents the .metadata.generation
                        that the condition was set based upon. For instance, if .metadata.generation
                        is currently 12, but the .status.conditions[x].observedGeneration
                        is 9, the condition is out of date with respect to the current
                        state of the instance.
                      format: int64
                      minimum: 0
                      type: integer
                    reason:
                      description: reason contains a programmatic identifier indicating
                        the reason for the condition's last transition. Producers
                        of specific condition types may define expected values and
                        meanings for this field, and whether the values are considered
                        a guaranteed API. The value should be a CamelCase string.
                        This field may not be empty.
                      maxLength: 1024
                      minLength: 1
                      pattern: ^[A-Za-z]([A-Za-z0-9_,:]*[A-Za-z0-9_])?$
                      type: string
                    status:
                      description: status of the condition, one of True, False, Unknown.
                      enum:
                      - "True"
                      - "False"
                      - Unknown
                      type: string
                    type:
                      description: type of condition in CamelCase or in foo.example.com/CamelCase.
                        --- Many .condition.type values are consistent across resources
                        like Available, but because arbitrary conditions can be useful
                        (see .node.status.conditions), the ability to deconflict is
                        important. The regex it matches is (dns1123SubdomainFmt/)?(qualifiedNameFmt)
                      maxLength: 316
                      pattern: ^([a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*/)?(([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9])$
                      type: string
                  required:
                  - lastTransitionTime
                  - message
                  - reason
                  - status
                  - type
                  type: object
                type: array
            type: object
        type: object
    served: true
    storage: true
    subresources:
      status: {}
---
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  annotations:
    controller-gen.kubebuilder.io/version: v0.12.1
  name: targetconnectionprofiles.inv.sdcio.dev
spec:
  group: inv.sdcio.dev
  names:
    categories:
    - sdc
    - inv
    kind: TargetConnectionProfile
    listKind: TargetConnectionProfileList
    plural: targetconnectionprofiles
    singular: targetconnectionprofile
  scope: Namespaced
  versions:
  - name: v1alpha1
    schema:
      openAPIV3Schema:
        description: TargetConnectionProfile is the Schema for the TargetConnectionProfile
          API
        properties:
          apiVersion:
            description: 'APIVersion defines the versioned schema of this representation
              of an object. Servers should convert recognized schemas to the latest
              internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources'
            type: string
          kind:
            description: 'Kind is a string value representing the REST resource this
              object represents. Servers may infer this from the endpoint the client
              submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds'
            type: string
          metadata:
            type: object
          spec:
            description: TargetConnectionProfileSpec defines the desired state of
              TargetConnectionProfile
            properties:
              connectRetry:
                default: 0
                description: A Duration represents the elapsed time between two instants
                  as an int64 nanosecond count. The representation limits the largest
                  representable duration to approximately 290 years.
                format: int64
                type: integer
                x-kubernetes-validations:
                - message: connectRetry is immutable
                  rule: self == oldSelf
              encoding:
                default: ASCII
                enum:
                - unknown
                - JSON
                - JSON_IETF
                - bytes
                - protobuf
                - ASCII
                - config
                type: string
                x-kubernetes-validations:
                - message: encoding is immutable
                  rule: self == oldSelf
              includeNS:
                default: false
                type: boolean
                x-kubernetes-validations:
                - message: includeNS is immutable
                  rule: self == oldSelf
              insecure:
                default: false
                type: boolean
                x-kubernetes-validations:
                - message: insecure is immutable
                  rule: self == oldSelf
              operationWithNS:
                default: false
                type: boolean
                x-kubernetes-validations:
                - message: operationWithNS is immutable
                  rule: self == oldSelf
              port:
                default: 57400
                description: Port defines the port on which the scan runs
                type: integer
                x-kubernetes-validations:
                - message: port is immutable
                  rule: self == oldSelf
              preferredNetconfVersion:
                default: "1.0"
                enum:
                - "1.0"
                - "1.1"
                type: string
                x-kubernetes-validations:
                - message: preferredNetconfVersion is immutable
                  rule: self == oldSelf
              protocol:
                default: gnmi
                enum:
                - unknown
                - gnmi
                - netconf
                - noop
                type: string
                x-kubernetes-validations:
                - message: protocol is immutable
                  rule: self == oldSelf
              skipVerify:
                default: true
                type: boolean
                x-kubernetes-validations:
                - message: skipVerify is immutable
                  rule: self == oldSelf
              timeout:
                default: 10
                description: A Duration represents the elapsed time between two instants
                  as an int64 nanosecond count. The representation limits the largest
                  representable duration to approximately 290 years.
                format: int64
                type: integer
                x-kubernetes-validations:
                - message: timeout is immutable
                  rule: self == oldSelf
              useOperationRemove:
                default: false
                type: boolean
                x-kubernetes-validations:
                - message: UseOperationRemove is immutable
                  rule: self == oldSelf
            required:
            - port
            - protocol
            type: object
        type: object
    served: true
    storage: true
---
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  annotations:
    controller-gen.kubebuilder.io/version: v0.12.1
  name: targets.inv.sdcio.dev
spec:
  group: inv.sdcio.dev
  names:
    categories:
    - sdc
    - inv
    kind: Target
    listKind: TargetList
    plural: targets
    singular: target
  scope: Namespaced
  versions:
  - additionalPrinterColumns:
    - jsonPath: .status.conditions[?(@.type=='Ready')].status
      name: READY
      type: string
    - jsonPath: .status.conditions[?(@.type=='DSReady')].status
      name: DATASTORE
      type: string
    - jsonPath: .spec.provider
      name: PROVIDER
      type: string
    - jsonPath: .spec.address
      name: ADDRESS
      type: string
    - jsonPath: .status.discoveryInfo.platform
      name: PLATFORM
      type: string
    - jsonPath: .status.discoveryInfo.serialNumber
      name: SERIALNUMBER
      type: string
    - jsonPath: .status.discoveryInfo.macAddress
      name: MACADDRESS
      type: string
    name: v1alpha1
    schema:
      openAPIV3Schema:
        description: Target is the Schema for the Target API
        properties:
          apiVersion:
            description: 'APIVersion defines the versioned schema of this representation
              of an object. Servers should convert recognized schemas to the latest
              internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources'
            type: string
          kind:
            description: 'Kind is a string value representing the REST resource this
              object represents. Servers may infer this from the endpoint the client
              submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds'
            type: string
          metadata:
            type: object
          spec:
            description: TargetSpec defines the desired state of Target
            properties:
              address:
                description: Address defines the address to connect to the target
                type: string
              connectionProfile:
                description: ConnectionProfile define the profile used to connect
                  to the target once discovered
                type: string
              credentials:
                description: Credentials defines the name of the secret that holds
                  the credentials to connect to the target
                type: string
              provider:
                description: Provider specifies the provider using this target.
                type: string
              syncProfile:
                description: SyncProfile define the profile used to sync to the target
                  config once discovered
                type: string
              tlsSecret:
                description: TLSSecret defines the name of the TLS secret to connect
                  to the target if mtls is used
                type: string
            required:
            - address
            - connectionProfile
            - credentials
            - provider
            type: object
          status:
            description: TargetStatus defines the observed state of Target
            properties:
              conditions:
                description: Conditions of the resource.
                items:
                  properties:
                    lastTransitionTime:
                      description: lastTransitionTime is the last time the condition
                        transitioned from one status to another. This should be when
                        the underlying condition changed.  If that is not known, then
                        using the time when the API field changed is acceptable.
                      format: date-time
                      type: string
                    message:
                      description: message is a human readable message indicating
                        details about the transition. This may be an empty string.
                      maxLength: 32768
                      type: string
                    observedGeneration:
                      description: observedGeneration represents the .metadata.generation
                        that the condition was set based upon. For instance, if .metadata.generation
                        is currently 12, but the .status.conditions[x].observedGeneration
                        is 9, the condition is out of date with respect to the current
                        state of the instance.
                      format: int64
                      minimum: 0
                      type: integer
                    reason:
                      description: reason contains a programmatic identifier indicating
                        the reason for the condition's last transition. Producers
                        of specific condition types may define expected values and
                        meanings for this field, and whether the values are considered
                        a guaranteed API. The value should be a CamelCase string.
                        This field may not be empty.
                      maxLength: 1024
                      minLength: 1
                      pattern: ^[A-Za-z]([A-Za-z0-9_,:]*[A-Za-z0-9_])?$
                      type: string
                    status:
                      description: status of the condition, one of True, False, Unknown.
                      enum:
                      - "True"
                      - "False"
                      - Unknown
                      type: string
                    type:
                      description: type of condition in CamelCase or in foo.example.com/CamelCase.
                        --- Many .condition.type values are consistent across resources
                        like Available, but because arbitrary conditions can be useful
                        (see .node.status.conditions), the ability to deconflict is
                        important. The regex it matches is (dns1123SubdomainFmt/)?(qualifiedNameFmt)
                      maxLength: 316
                      pattern: ^([a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*/)?(([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9])$
                      type: string
                  required:
                  - lastTransitionTime
                  - message
                  - reason
                  - status
                  - type
                  type: object
                type: array
              discoveryInfo:
                description: Discovery info defines the information retrieved during
                  discovery
                properties:
                  hostname:
                    description: HostName associated with the target
                    type: string
                  lastSeen:
                    description: Last discovery time
                    format: date-time
                    type: string
                  macAddress:
                    description: MacAddress associated with the target
                    type: string
                  platform:
                    description: Platform associated with the target
                    type: string
                  protocol:
                    description: Protocol used for discovery
                    type: string
                  provider:
                    description: Type associated with the target
                    type: string
                  serialNumber:
                    description: SerialNumber associated with the target
                    type: string
                  supportedEncodings:
                    description: Supported Encodings of the target
                    items:
                      type: string
                    type: array
                  version:
                    description: Version associated with the target
                    type: string
                type: object
              usedReferences:
                description: UsedReferences track the resource used to reconcile the
                  cr
                properties:
                  connectionProfileResourceVersion:
                    type: string
                  secretResourceVersion:
                    type: string
                  syncProfileResourceVersion:
                    type: string
                  tlsSecretResourceVersion:
                    type: string
                required:
                - connectionProfileResourceVersion
                - syncProfileResourceVersion
                type: object
            type: object
        type: object
    served: true
    storage: true
    subresources:
      status: {}
---
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  annotations:
    controller-gen.kubebuilder.io/version: v0.12.1
  name: targetsyncprofiles.inv.sdcio.dev
spec:
  group: inv.sdcio.dev
  names:
    categories:
    - sdc
    - inv
    kind: TargetSyncProfile
    listKind: TargetSyncProfileList
    plural: targetsyncprofiles
    singular: targetsyncprofile
  scope: Namespaced
  versions:
  - name: v1alpha1
    schema:
      openAPIV3Schema:
        description: TargetSyncProfile is the Schema for the TargetSyncProfile API
        properties:
          apiVersion:
            description: 'APIVersion defines the versioned schema of this representation
              of an object. Servers should convert recognized schemas to the latest
              internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources'
            type: string
          kind:
            description: 'Kind is a string value representing the REST resource this
              object represents. Servers may infer this from the endpoint the client
              submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds'
            type: string
          metadata:
            type: object
          spec:
            description: TargetSyncProfileSpec defines the desired state of TargetSyncProfile
            properties:
              buffer:
                default: 0
                format: int64
                type: integer
                x-kubernetes-validations:
                - message: buffer is immutable
                  rule: self == oldSelf
              sync:
                items:
                  description: TargetSyncProfileSync defines the desired state of
                    TargetSyncProfileSync
                  properties:
                    encoding:
                      default: ASCII
                      enum:
                      - unknown
                      - JSON
                      - JSON_IETF
                      - bytes
                      - protobuf
                      - ASCII
                      - config
                      type: string
                    interval:
                      default: 0
                      format: int64
                      type: integer
                    mode:
                      enum:
                      - unknown
                      - onChange
                      - sample
                      - once
                      type: string
                    name:
                      type: string
                    paths:
                      items:
                        type: string
                      maxItems: 10
                      type: array
                    protocol:
                      default: gnmi
                      enum:
                      - unknown
                      - gnmi
                      - netconf
                      - noop
                      type: string
                  required:
                  - mode
                  - name
                  - paths
                  - protocol
                  type: object
                maxItems: 10
                type: array
                x-kubernetes-validations:
                - message: sync may only be added
                  rule: oldSelf.all(x, x in self)
              validate:
                default: true
                type: boolean
                x-kubernetes-validations:
                - message: validate is immutable
                  rule: self == oldSelf
              workers:
                default: 10
                format: int64
                type: integer
                x-kubernetes-validations:
                - message: workers is immutable
                  rule: self == oldSelf
            type: object
            x-kubernetes-validations:
            - message: sync is required once set
              rule: '!has(oldSelf.sync) || has(self.sync)'
        type: object
    served: true
    storage: true

---
apiVersion: apiregistration.k8s.io/v1
kind: APIService
metadata:
  name: v1alpha1.config.sdcio.dev
spec:
  insecureSkipTLSVerify: true
  group: config.sdcio.dev
  groupPriorityMinimum: 1000
  versionPriority: 15
  service:
    name: capis
    namespace: network-system
    port: 6443
  version: v1alpha1
  #caBundle: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURZekNDQWt1Z0F3SUJBZ0lKQUtKY0FOZ3htSG1TTUEwR0NTcUdTSWIzRFFFQkN3VUFNR1V4Q3pBSkJnTlYKQkFZVEFuVnVNUXN3Q1FZRFZRUUlEQUp6ZERFS01BZ0dBMVVFQnd3QmJERUtNQWdHQTFVRUNnd0JiekVMTUFrRwpBMVVFQ3d3Q2IzVXhKREFpQmdOVkJBTU1HMkpoYzJsakxXTmxjblJwWm1sallYUmxMV0YxZEdodmNtbDBlVEFlCkZ3MHlNakF6TXpFd09URTNOVE5hRncweU16QXpNekV3T1RFM05UTmFNR1V4Q3pBSkJnTlZCQVlUQW5WdU1Rc3cKQ1FZRFZRUUlEQUp6ZERFS01BZ0dBMVVFQnd3QmJERUtNQWdHQTFVRUNnd0JiekVMTUFrR0ExVUVDd3dDYjNVeApKREFpQmdOVkJBTU1HMkpoYzJsakxXTmxjblJwWm1sallYUmxMV0YxZEdodmNtbDBlVENDQVNJd0RRWUpLb1pJCmh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBTUJwMHRhNU92Vy9VcVlsR1RMZnVsam9HYkFwVnB4MW1CbUwKR0dHOUhOZmJkVWxoQ1FtMVNYK3V6dllyQ05EZEJRMWdBYWVEa1lxOWNMbnN4YU92R25peHJ1WllUV1gyaU9maQpjRTZxRUVRTm05MmxRRnBvbnBneXI2dFc3dDhkMGRNcEVVNTlYUlQzdXRGZGhHRVJUYi94clR0c1RpaUp4Vk1jCmxFSzh3ajZjLytONitHNHZEcVBydkF5cFBJaUJtbkhwVE9tbmhOdjhSeXVXc3VXVEJwb0JTMUVjbTg1VlY3MEUKUGFpYSs3bDczLzArWmFzcTBHeklCdkx4S0ZiVHVYZHh2a0REY1M5c0FuTytVcHg1YUxhbjgrR25UTWd6NzR6Vgp3WDRuSFU1blFxYkZSSC9TQzVXeGNYczJXL0JNZllBRUk2ckhnUTBKNjJiMTBSZk0vQmNDQXdFQUFhTVdNQlF3CkVnWURWUjBUQVFIL0JBZ3dCZ0VCL3dJQkFUQU5CZ2txaGtpRzl3MEJBUXNGQUFPQ0FRRUFxUXM5eUdsalBFcUgKVHF6REpEa29DbXlTWmQ0S3VVSEpPcjY1QmhmYmppKzBsSC9Rbk9mdHdpd1FvajhwSFlnejVmZGZJa3JMTFU1KwpwMzh0cSs5QllsOFNudXd6U2EzQ2VpYUlncHUvL05xaCtieDRad1liNFJmVnZmSU5NdUZJaUhLUFBJUm1QRmlECjZJQjl0WFNrSmNmanhHd1NLRmhLSGszYU9EbmsxNUlyTDA0U040S0ZER1dncnI0WkJoL1RYT25XVmRpMHRBN3kKT2lmRkpRdWt1anhNVDRUU3ZtcmtjZW5Ubk84VEZTMk03SGVPZDRLYm14QUJFR3ZzaGZ0V2tXUGh0ZW1IYVJXYwpVOEh2SG8xS1M4cGdyYVdxMU5jMjErdHJoQS9uaGRtaWRDbW1DOHZSQ1MwU1cxZE90Q3ZJRzhpVUpIeDVKMklGCnhjUGt3aHYrN1E9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg=="
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: config:system:auth-delegator
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:auth-delegator
subjects:
- kind: ServiceAccount
  name: config-apiserver
  namespace: network-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: config-auth-reader
  namespace: kube-system
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: extension-apiserver-authentication-reader
subjects:
- kind: ServiceAccount
  name: config-apiserver
  namespace: network-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: config-apiserver-clusterrolebinding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: config-apiserver-clusterrole
subjects:
- kind: ServiceAccount
  name: config-apiserver
  namespace: network-system
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: config-apiserver-clusterrole
rules:
- apiGroups: [""]
  resources: ["namespaces", "secrets"]
  verbs: ["get", "watch", "list"]
- apiGroups: ["admissionregistration.k8s.io"]
  resources: ["mutatingwebhookconfigurations", "validatingwebhookconfigurations"]
  verbs: ["get", "watch", "list"]
- apiGroups: ["flowcontrol.apiserver.k8s.io"]
  resources: ["flowschemas", "prioritylevelconfigurations"]
  verbs: ["get", "watch", "list"]
- apiGroups: ["config.sdcio.dev"]
  resources: ["configs", "configs/status"]
  verbs: ["get", "watch", "list", "create", "update", "patch", "delete"]
- apiGroups: ["inv.sdcio.dev"]
  resources: ["targets", "targets/status"]
  verbs: ["get", "watch", "list", "create", "update", "patch", "delete"]
- apiGroups: ["inv.sdcio.dev"]
  resources: ["targetconnectionprofiles", "targetsyncprofiles"]
  verbs: ["get", "watch", "list"]
- apiGroups: ["inv.sdcio.dev"]
  resources: ["discoveryrules", "discoveryrules/status"]
  verbs: ["get", "watch", "list", "create", "update", "patch", "delete"]
- apiGroups: ["inv.sdcio.dev"]
  resources: ["schemas", "schemas/status"]
  verbs: ["get", "watch", "list", "create", "update", "patch", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: config-apiserver-clusterrolebinding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: config-apiserver-clusterrole
subjects:
- kind: ServiceAccount
  name: config-apiserver
  namespace: network-system
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: aggregated-apiserver-role
  namespace: network-system
rules:
  - apiGroups: [""]
    resources: ["serviceaccounts"]
    verbs: ["get"]
  - apiGroups: [""]
    resources: ["serviceaccounts/token"]
    verbs: ["create"]
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: dataserver
  namespace: network-system
data: 
  data-server.yaml: |
    grpc-server:
      # gRPC listening address
      # address: ":56000"

      ## TLS config
      # tls:
      #   ca:
      #   cert:
      #   key:
      #   skip-verify:
      #   client-auth:

      # expose local schema store over gRPC
      schema-server:
        # enables the schema gRPC server
        enabled: true
        # directory to store the uploaded schemas
        schemas-directory: ./schemas

      # data-server attributes
      data-server:
        # max number of candidates per DS
        max-candidates: 16

      # max message size in bytes the server can receive.
      # If this is not set, it defaults to 4 * 1024 * 1024 (4MB)
      max-recv-msg-size: 25165824 # 24 * 1024 * 1024 (24MB)

    datastores: # this specifies MAIN datastores

    schemas: []

    # remote schema server
    # schema-server:
    #   address: localhost:55000
      # TLS config
      # tls:
      #   ca:
      #   cert:
      #   key:
      #   skip-verify:

    # cache config, defaults to
    # type: local
    # store-type: badgerdb
    # dir: ./cached/caches
    cache: 
      # type: remote
      type: local
      # store-type if type == local
      store-type: badgerdbsingle
      # local directory for caches if type == local
      dir: "./cached/caches"
      # remote cache address, if type == remote
      # address: localhost:50100

    # expose a prometheus server with cpu, mem and grpc metrics
    prometheus:
      address: ":56090"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: config-apiserver
  namespace: network-system
  labels:
    config-apiserver: "true"
spec:
  replicas: 1
  selector:
    matchLabels:
      config-apiserver: "true"
  template:
    metadata:
      labels:
        config-apiserver: "true"
    spec:
      serviceAccountName: config-apiserver
      containers:
      - name: capis
        image: ndd.artifactory-espoo2.int.net.nokia.com/yndd/capis-x86:v0.0.1
        imagePullPolicy: Always
        command:
        - /app/capis
        args:
        - "--tls-cert-file=/apiserver.local.config/certificates/tls.crt"
        - "--tls-private-key-file=/apiserver.local.config/certificates/tls.key"
        - "--feature-gates=APIPriorityAndFairness=false"
        - "--audit-log-path=-"
        - "--audit-log-maxage=0"
        - "--audit-log-maxbackup=0"
        - "--secure-port=6443"
        env:
        - name: POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
        - name: "NODE_NAME"
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: spec.nodeName
        - name: "NODE_IP"
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: status.hostIP
        - name: ENABLE_TARGET
          value: "true"
        - name: ENABLE_DISCOVERYRULE
          value: "true"
        - name: ENABLE_SCHEMA
          value: "true"
        volumeMounts:
        - name: apiserver-certs
          mountPath: /apiserver.local.config/certificates
          readOnly: true
        - name: config-store
          mountPath: /config
        - name: schema-store
          mountPath: /schemas
      - name: data-server
        image: ndd.artifactory-espoo2.int.net.nokia.com/yndd/data-server:v0.0.20
        imagePullPolicy: Always
        command:
        - /app/data-server
        args:
        - "--config=/config/data-server.yaml"
        volumeMounts:
        - name: dataserver-config
          mountPath: /config
        - name: cache
          mountPath: /cached/caches
        - name: schema-store
          mountPath: /schemas
      volumes:
      - name: dataserver-config
        configMap:
          name: dataserver
      - name: apiserver-certs
        secret:
          secretName: capis
      - name: cache
        emptyDir:
          sizeLimit: 10Gi
      - name: config-store
        persistentVolumeClaim:
          claimName: pvc-config-store
      - name: schema-store
        persistentVolumeClaim:
          claimName: pvc-schema-store
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-config-store
  namespace: network-system
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-schema-store
  namespace: network-system
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
EOF
```

if successfull you should see a running container similar to this

```
kubectl get pods -n network-system
```

output

```
NAME                                READY   STATUS    RESTARTS        AGE
config-apiserver-5d56bf5776-kktst   2/2     Running   1 (6m49s ago)   6m55s
```