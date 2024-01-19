# Device discovery using Addresses (IPs or DNS names)

### Examples

Example of a `DiscoveryRule`

```yaml
apiVersion: inv.sdcio.dev/v1alpha1
kind: DiscoveryRule
metadata:
  name: dr-static
  namespace: default
spec:
  period: 1m
  concurrentScans: 2
  defaultSchema:
    provider: srl.nokia.sdcio.dev  
    version: 23.10.1
  addresses:
  - address: 172.18.0.4
    hostName: dev1
  - address: 172.18.0.3
    hostName: dev2
  targetConnectionProfiles:
  - credentials: srl.nokia.sdcio.dev 
    connectionProfile: gnmi-skipverify
    syncProfile: gnmi-onchange
  targetTemplate:
    labels:
      sdcio.dev/region: us-east
```