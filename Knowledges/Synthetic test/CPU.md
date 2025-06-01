# CPU
## Commands to generate CPU load
openssl
```
openssl speed -multi $(grep -ci processor /proc/cpuinfo)
```
