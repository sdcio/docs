# Development
## Environment
The following provides details on how to run any of the SDC components locally on the developers machine, allowing to use e.g. the debugging mode.


### Setup
Telepresence is used to "hijack" the TCP connection endpoints and redirect it to the development machine.
Hence, [install Telepresence](https://www.telepresence.io/docs/latest/quick-start/) on the development machine.


#### Install Telepresence on Dev machine

```
sudo curl -fL https://github.com/telepresenceio/telepresence/releases/latest/download/telepresence-linux-amd64 -o /usr/local/bin/telepresence

sudo chmod a+x /usr/local/bin/telepresence
sudo bash -c "/usr/local/bin/telepresence completion bash > /etc/bash_completion.d/telepresence"
. /etc/bash_completion.d/telepresence
```

#### Install Telepresence in K8s cluster

```
telepresence helm install
```

### Connect 
Connect to the telepresence service in the cluster, using the namespace sdc-system.
```
telepresence connect -n sdc-system
```

### Intercept Service Traffic

#### Config Server
```
telepresence replace api-server
telepresence replace controller
```

/// details | mounts
telepresence allows for the mounts of the config-server pod to be forwarded via sshfs to the dev machine.

It might be necessary to set the `user_allow_other` in the fuse config file `/etc/fuse.conf`.
///

#### Data Server
```
telepresence replace data-server-controller --container data-server
telepresence replace data-server-controller --container controller
```

/// details | iptables error
Telepresence allows also to intercept only traffic, without adding an init-container.
[To do that](https://www.telepresence.io/docs/troubleshooting/#injected-init-container-doesnt-function-properly&gsc.tab=0), it is necessary to have named ports, not only numbered ones. Therefore, adding a name to the data-server ports and adding the same name to the data-service will resolve the problem.
///

### Retrieve Config-Server Api-Service Certificate

```
kubectl get secrets -n sdc-system api-server-cert -o jsonpath="{.data['tls\.crt']}" | base64 -d | tee tls.crt
kubectl get secrets -n sdc-system api-server-cert -o jsonpath="{.data['tls\.key']}" | base64 -d | tee tls.key
```

### Prepare kubeconfig
```
# copy actual ~/.kube/config
cp ~/.kube/config ./kubeconfig

# delete the users section via yq
yq -i 'del(.users)' kubeconfig
```

### Retrieve ServiceAccount Token
Retrieve a 30-day valid ServiceAccount token and put it into the kubeconfig.
```
kubectl config --kubeconfig ./kubeconfig set-credentials kind-kind --token=$(kubectl create token -n sdc-system --duration 720h api-server)
```

### Run config-server locally
The VS Code configuration is as follows. 
The Data-Server has to be started first, then the Config-Server can be started.
```
        {
            "name": "Launch Package",
            "type": "go",
            "request": "launch",
            "mode": "debug",
            "program": "${workspaceFolder}/main.go",
            "cwd": "${workspaceFolder}",
            "args": [
                "--tls-cert-file=./tls.crt",
                "--tls-private-key-file=./tls.key",
                "--audit-log-path=-",
                "--audit-log-maxage=0",
                "--audit-log-maxbackup=0",
                "--secure-port=6443",
                "--kubeconfig=./kubeconfig",
                "--authorization-kubeconfig=./kubeconfig",
                "--authentication-kubeconfig=./kubeconfig",
            ],
            "env": {
                "SDC_SCHEMA_SERVER_BASE_DIR": "/tmp/SDC/SchemaBase",
                "SDC_CONFIG_DIR": "/tmp/SDC/Config",
                "SDC_WORKSPACE_DIR": "/tmp/SDC/Workspace",
                "PPROF_PORT": "8081",
                "REVERTIVE": "true",
                "ENABLE_SUBSCRIPTION": "true",
                "ENABLE_TARGET": "true",
                "ENABLE_TARGETDATASTORE": "true",
                "ENABLE_TARGETCONFIGSERVER": "true",
                "ENABLE_TARGETRECOVERYSERVER": "true",
                "ENABLE_DISCOVERYRULE": "true",
                "ENABLE_SCHEMA": "true",
                "ENABLE_CONFIGSET": "true",
                "ENABLE_WORKSPACE": "true",
                "ENABLE_ROLLOUT": "true"
            },
            "console": "integratedTerminal",
        }
```

