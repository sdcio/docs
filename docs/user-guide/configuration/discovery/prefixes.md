# Device discovery using IP prefixes

### Examples

Example of a `DiscoveryRule`

```yaml
apiVersion: inv.sdcio.dev/v1alpha1
kind: DiscoveryRule
metadata:
  name: dr-dynamic
  namespace: default
spec:
  period: 1m
  concurrentScans: 2
  prefixes:
  - prefix: 172.18.0.0/24
    excludes:
    - 172.18.0.0
    - 172.18.0.1
    - 172.18.0.255
  discoveryProfile:
    credentials: srl.nokia.sdcio.dev 
    connectionProfiles:
    - gnmi-skipverify
  targetConnectionProfiles:
  - credentials: srl.nokia.sdcio.dev 
    connectionProfile: gnmi-skipverify
    syncProfile: gnmi-onchange
  targetTemplate:
    labels:
      sdcio.dev/region: us-east
```