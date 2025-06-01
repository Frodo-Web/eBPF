# CPU
## Commands to generate CPU load
openssl
```
openssl speed -multi $(grep -ci processor /proc/cpuinfo)
```
stress-ng
```
stress-ng --cpu 2 --io 0 --vm 1 --vm-bytes 1G --timeout 360s
stress-ng --cpu 4 --vm 2 --fork 8 --switch 4 --timeout 1m
```
