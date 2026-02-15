# pprof

## Introduction

`pprof` is a powerful profiling tool for Go applications that helps analyze CPU usage, memory allocation, and other performance characteristics. This guide explains how to collect and analyze profiling data from a running Go service using `pprof`.

## Enabling pprof

`pprof` is enabled using the following arguments in the config-server

```yaml
- name: PPROF_PORT
  value: "8081"
```

## Setting Up pprof

### 1. Forwarding the pprof Port

To access the pprof endpoint of a running pod in a Kubernetes cluster, use the following command to set up port forwarding:

```sh
kubectl port-forward pod/<pod> -n sdc-system 8081:8081
```

Replace `<pod>` with the actual pod name running your Go application.

### 2. Collecting Profiles

#### CPU Profile
To collect a CPU profile, execute:

```sh
curl -s "http://127.0.0.1:8081/debug/pprof/profile" > test/cpu-profile.out
```

This records CPU usage for 30 seconds and saves the profile in `test/cpu-profile.out`.

#### Heap Profile

To capture a heap profile, run:

```sh
curl -s "http://127.0.0.1:8081/debug/pprof/heap" > test/heap-profile.out
```

This saves the heap allocation profile in `test/heap-profile.out`.

## Analyzing the Profiles

### 1. Analyzing the CPU Profile

To visualize the CPU profile in an interactive web interface:

```sh
go tool pprof -http=:8080 test/cpu-profile.out
```

This opens a web-based interface showing the CPU usage breakdown.

### 2. Analyzing the Heap Profile

To view a summary of memory allocation:

```sh
go tool pprof -top test/heap-profile.out
```

To open the heap profile in a web interface:

```sh
go tool pprof -http=:8080 test/heap-profile.out
```

### 3. Live Heap Profiling

Instead of saving the heap profile first, you can analyze it directly from the running service:

```sh
go tool pprof http://127.0.0.1:8081/debug/pprof/heap
```

This fetches the heap profile and starts an interactive session where you can run commands like `top`, `list <function>`, and `web` to inspect memory allocation.

## Conclusion

By leveraging `pprof`, you can effectively diagnose performance bottlenecks in Go applications running in Kubernetes. The combination of CPU and heap profiling provides deep insights into resource consumption, helping optimize application performance.

