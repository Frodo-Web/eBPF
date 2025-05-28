# BCC tools
![image](https://github.com/user-attachments/assets/ad2fba74-4723-4bed-a64d-6542c57e3561)
## execsnoop
```
# execsnoop
PCOMM PID RET ARGS
supervise 9660 0 ./run
supervise 9661 0 ./run
mkdir 9662 0 /bin/mkdir -p ./main
run 9663 0 ./run
[...]
```
## opensnoop
```
# opensnoop
PID COMM FD ERR PATH
1565 redis-server 5 0 /proc/1565/stat
1603 snmpd 9 0 /proc/net/dev
1603 snmpd 11 0 /proc/net/if_inet6
1603 snmpd -1 2 /sys/class/net/eth0/device/vendor
1603 snmpd 11 0 /proc/sys/net/ipv4/neigh/eth0/retrans_time_ms
1603 snmpd 11 0 /proc/sys/net/ipv6/neigh/eth0/retrans_time_ms
1603 snmpd 11 0 /proc/sys/net/ipv6/conf/eth0/forwarding
[...]
```
## ext4slower
```
# ext4slower
Tracing ext4 operations slower than 10 ms
TIME COMM PID T BYTES OFF_KB LAT(ms) FILENAME
06:35:01 cron 16464 R 1249 0 16.05 common-auth
06:35:01 cron 16463 R 1249 0 16.04 common-auth
06:35:01 cron 16465 R 1249 0 16.03 common-auth
06:35:01 cron 16465 R 4096 0 10.62 login.defs
06:35:01 cron 16464 R 4096 0 10.61 login.defs
[...]
```
## biolatency -m
```
# biolatency -m
Tracing block device I/O... Hit Ctrl-C to end.
^C
msecs : count distribution
0 -> 1 : 16335 |****************************************|
2 -> 3 : 2272 |***** |
4 -> 7 : 3603 |******** |
8 -> 15 : 4328 |********** |
16 -> 31 : 3379 |******** |
32 -> 63 : 5815 |************** |
64 -> 127 : 0 | |
128 -> 255 : 0 | |
256 -> 511 : 0 | |
512 -> 1023 : 1 | |
```
## biosnoop
```
biosnoop
TIME(s) COMM PID DISK T SECTOR BYTES LAT(ms)
0.000004001 supervise 1950 xvda1 W 13092560 4096 0.74
0.000178002 supervise 1950 xvda1 W 13092432 4096 0.61
0.001469001 supervise 1956 xvda1 W 13092440 4096 1.24
0.001588002 supervise 1956 xvda1 W 13115128 4096 1.09
1.022346001 supervise 1950 xvda1 W 13115272 4096 0.98
[...]
```
## cachestat
```
# cachestat
HITS MISSES DIRTIES HITRATIO BUFFERS_MB CACHED_MB
53401 2755 20953 95.09% 14 90223
49599 4098 21460 92.37% 14 90230
16601 2689 61329 86.06% 14 90381
15197 2477 58028 85.99% 14 90522
[...]
```
## tcpconnect
```
# tcpconnect
PID COMM IP SADDR DADDR DPORT
1479 telnet 4 127.0.0.1 127.0.0.1 23
1469 curl 4 10.201.219.236 54.245.105.25 80
1469 curl 4 10.201.219.236 54.67.101.145 80
1991 telnet 6 ::1 ::1 23
2015 ssh 6 fe80::2000:bff:fe82:3ac fe80::2000:bff:fe82:3ac 22
[...]
```
## tcpaccept
```
# tcpaccept
PID COMM IP RADDR LADDR LPORT
907 sshd 4 192.168.56.1 192.168.56.102 22
907 sshd 4 127.0.0.1 127.0.0.1 22
5389 perl 6 1234:ab12:2040:5020:2299:0:5:0 1234:ab12:2040:5020:2299:0:5:0 7001
[...]
```
## tcpretrans
```
# tcpretrans
TIME PID IP LADDR:LPORT T> RADDR:RPORT STATE
01:55:05 0 4 10.153.223.157:22 R> 69.53.245.40:34619 ESTABLISHED
01:55:05 0 4 10.153.223.157:22 R> 69.53.245.40:34619 ESTABLISHED
01:55:17 0 4 10.153.223.157:22 R> 69.53.245.40:22957 ESTABLISHED
[...]
```
## runqlat
```
runqlat
Tracing run queue latency... Hit Ctrl-C to end.
^C
usecs : count distribution
0 -> 1 : 233 |*********** |
2 -> 3 : 742 |************************************ |
4 -> 7 : 203 |********** |
8 -> 15 : 173 |******** |
16 -> 31 : 24 |* |
32 -> 63 : 0 | |
64 -> 127 : 30 |* |
128 -> 255 : 6 | |
256 -> 511 : 3 | |
512 -> 1023 : 5 | |
1024 -> 2047 : 27 |* |
2048 -> 4095 : 30 |* |
4096 -> 8191 : 20 | |
8192 -> 16383 : 29 |* |
16384 -> 32767 : 809 |****************************************|
32768 -> 65535 : 64 |*** |
```
## profile
```
# profile
Sampling at 49 Hertz of all threads by user + kernel stack... Hit Ctrl-C to end.
^C
[...]
copy_user_enhanced_fast_string
copy_user_enhanced_fast_string
_copy_from_iter_full
tcp_sendmsg_locked
tcp_sendmsg
inet_sendmsg
sock_sendmsg
sock_write_iter
new_sync_write
__vfs_write
vfs_write
SyS_write
do_syscall_64
entry_SYSCALL_64_after_hwframe
[unknown]
[unknown]
- iperf (24092)
58
```
