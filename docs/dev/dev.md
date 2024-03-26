# Development
## Environment
The following provides details on how to run any of the SDC components locally on the developers machine, allowing to use e.g. the debugging mode.

### Setup
Telepresence is used to "highjack" the tcp connection endpoints and redirect it to the development machine.
Hence [install Telepresence](https://www.telepresence.io/docs/latest/quick-start/) on the development machine.


#### Install Telepresence on Dev machine

```
sudo curl -fL https://app.getambassador.io/download/tel2oss/releases/download/v2.18.0/telepresence-linux-amd64 -o /usr/local/bin/telepresence

sudo chmod a+x /usr/local/bin/telepresence
sudo bash -c "/usr/local/bin/telepresence completion bash > /etc/bash_completion.d/telepresence"
```

#### Install Telepresence in K8s cluster

```
telepresence helm install
```

### Connect 
Connect to the telepresence service in the cluster, using the namespace network-system.
```
telepresence connect -n network-system
```

### Intercept Service Traffic

#### Config Server
```
telepresence intercept config-server --port 6443:api-service
```

/// details | mounts
telepresence allows for the mounts of the config-server pod to be forwarded via sshfs to the dev machine.

It might be necessary to set the `user_allow_other` in the fuse config file `/etc/fuse.conf`.
///

### Retrieve Config-Server Api-Service Certificate

```
kubectl get secrets -n network-system config-server-cert -o jsonpath="{.data['tls\.crt']}" | base64 -d | tee tls.crt
kubectl get secrets -n network-system config-server-cert -o jsonpath="{.data['tls\.key']}" | base64 -d | tee tls.key
```

### Prepare kubeconfig
```
# copy actual ~/.kube/config
cp ~/.kube/config ./kubeconfig

# delete the users section via yq
yq -i 'del(.users)' kubeconfig
```

### Retrieve ServiceAccount Token
Retrieve a 30 day valid ServiceAccount token and put it into the kubeconfig.
```
kubectl config --kubeconfig ./kubeconfig set-credentials kind-kind --token=$(kubectl create token -n network-system --duration 720h config-server)
```

### Run config-server locally
The VSCode configuration is as follows. 
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
                "--feature-gates=APIPriorityAndFairness=false",
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
                "SDC_CONFIG_DIR": "/tmp/SDC/Config"
            },
            "console": "integratedTerminal",
        }
```