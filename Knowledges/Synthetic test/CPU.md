# CPU
## Commands to generate CPU load
openssl
```
openssl speed -multi $(grep -ci processor /proc/cpuinfo)
```
stress-ng
```
stress-ng --cpu 2 --io 0 --vm 1 --vm-bytes 1G --timeout 360s
```
