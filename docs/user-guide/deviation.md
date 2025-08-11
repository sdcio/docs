# Deviation

A deviation is a report indicating differences between the actual device or system configuration and the configuration specified in one or more Config CRs managed by SDCIO.

There are three types of deviations:

1.	UNHANDLED

    - No matching Config CR exists in the system.
	- Treated as a Target-type deviation.
	- SDCIO only reports these deviations; no corrective action is taken.

2.	NOT-APPLIED

	- A matching Config CR exists, but the actual configuration differs from what is defined in the Config CR.
	- SDCIO will act on these deviations based on the configured mode: revertive or non-revertive.

3.	OVERRULED

	- A matching Config CR exists, but the actual configuration has been overridden by a higher-priority intent.
	- SDCIO reports these deviations but does not attempt to change the overriding configuration.

SDCIO automatically creates a deviation per target CR and one for each config CR. By default when no config CR exists all brownfield configuration is reported as a UNHANDLED deviation per target.

## Revertive vs. Non-Revertive Behavior

- Revertive mode
    
SDCIO will automatically reapply the Config CR when a NOT-APPLIED deviation is detected, restoring the intended configuration.

- Non-revertive mode

SDCIO will treat the deviation as part of the active configuration. When a user want to deny a deviation in non revertive mode, he/she can:

- Deny a full deviation – Delete the deviation CR. SDCIO will reapply the original Config CR without the deviation.
- Deny partial deviation – Delete only the relevant paths from the deviation CR. SDCIO will reapply the Config CR while preserving the accepted parts of the deviation.

To change revertive or non revetive behavior can be done:
- globally: as part of the deployment environment variabled of the config-server

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

