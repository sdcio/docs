# Deviation

A deviation is a report indicating differences between the actual device or system configuration and the configuration specified in one or more Config CRs managed by SDC.

There are three types of deviations:

1.	UNHANDLED

    - No matching Config CR exists in the system.
	- Treated as a Target-type deviation.
	- SDC only reports these deviations; no corrective action is taken.

2.	NOT-APPLIED

	- A matching Config CR exists, but the actual configuration differs from what is defined in the Config CR.
	- SDC will act on these deviations based on the configured mode: revertive or non-revertive.

3.	OVERRULED

	- A matching Config CR exists, but the actual configuration has been overridden by a higher-priority intent.
	- SDC reports these deviations but does not attempt to change the overriding configuration.

SDC automatically creates a deviation per target CR and one for each config CR. By default when no config CR exists all brownfield configuration is reported as a UNHANDLED deviation per target.

## Revertive vs. Non-Revertive Behavior

- Revertive mode
    
SDC will automatically reapply the Config CR when a NOT-APPLIED deviation is detected, restoring the intended configuration.

- Non-revertive mode

SDC will treat the deviation as part of the active configuration. 

!!!note "we are working on a capability to allow for the clearing of deviations. If this is something you need, you need to wait for the release the accomodates this."

To change revertive or non revetive behavior can be done:
- globally: as part of the deployment environment variables of the config-server

```yaml
        - name: REVERTIVE
          value: "true"
```

- per config CR: see [config CR](../configuration/config/config/) section


## Example:

```
kubectl get deviations.config.sdcio.dev 
```


```bash
NAME                                           TYPE     TARGET           DEVIATIONS
deviation.config.sdcio.dev/configset1-core01   config   default/core01   0
deviation.config.sdcio.dev/configset1-edge01   config   default/edge01   0
deviation.config.sdcio.dev/configset1-edge02   config   default/edge02   0
deviation.config.sdcio.dev/core01              target   default/core01   600
deviation.config.sdcio.dev/edge01              target   default/edge01   602
deviation.config.sdcio.dev/edge02              target   default/edge02   602
deviation.config.sdcio.dev/test                config   default/core01   0
```

