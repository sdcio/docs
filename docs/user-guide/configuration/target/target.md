# Target
The Target CR is what defines a system thats managed by SDC. The Target CRs are however not explicitly created by an enduser.
The creation of Targets is the job of the DiscoveryRule Controller. It will take the defined DiscoveryRules perform discovery and create the target CRs with all the information configured or discovered by the Discovery Controller.

```yaml
apiVersion: inv.sdcio.dev/v1alpha1
kind: Target
metadata:
  name: dev-man
  namespace: default
spec:
  address: 172.18.0.5
  connectionProfile: gnmi-skipverify
  credentials: srl.nokia.sdcio.dev
  provider: srl.nokia.sdcio.dev
  syncProfile: gnmi-get
```

## Attributes
* `address`: The mgmt address of the Target.
* `connectionProfile`: The name of the connection profile (_targetconnectionprofiles.inv.sdcio.dev_) used to connect to the Target.
* `syncProfile`: The name of the connection profile (_targetsyncprofiles.inv.sdcio.dev_) used to sync  config from the Target into SDC.
* `credentials`: The name of the secret that contains the login creadentials for the Target.
* `provider`: A string that defines the connection provider that is to be used. The format is "`<MODEL/NOS>.<VENDOR>.sdcio.dev`"
