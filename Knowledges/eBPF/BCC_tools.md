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
## Specialized BCC tools (Многоцелевые инструменты)
### funccount
```
1. Вызывается ли функция tcp_drop()?
# funccount tcp_drop
Tracing 1 functions for "tcp_drop"... Hit Ctrl-C to end.
^C
FUNC COUNT
tcp_drop 3
Detaching...

2. Какая функция из подсистемы VFS в ядре вызывается чаще всего?
# funccount 'vfs_*'
Tracing 55 functions for "vfs_*"... Hit Ctrl-C to end.
^C
FUNC COUNT
vfs_rename 1
vfs_readlink 2
vfs_lock_file 2
vfs_statfs 3
vfs_fsync_range 3
vfs_unlink 5
vfs_statx 189
vfs_statx_fd 229
vfs_open 345
vfs_getattr_nosec 353
vfs_getattr 353
vfs_writev 1776
vfs_read 5533
vfs_write 6938
Detaching...

3. Сколько раз в секунду вызывается функция pthread_mutex_lock() в простран-
стве пользователя?
# funccount -i 1 c:pthread_mutex_lock
Tracing 1 functions for "c:pthread_mutex_lock"... Hit Ctrl-C to end.
FUNC COUNT
pthread_mutex_lock 1849
FUNC COUNT
pthread_mutex_lock 1761
FUNC COUNT
pthread_mutex_lock 2057
FUNC COUNT
pthread_mutex_lock 2261
[...]

4. Какая из строковых функций в libc вызывается чаще всего в системе в целом?
# funccount 'c:str*'
Tracing 59 functions for "c:str*"... Hit Ctrl-C to end.
^C
FUNC COUNT
strndup 3
strerror_r 5
strerror 5
strtof32x_l 350
strtoul 587
strtoll 724
strtok_r 2839
strdup 5788
Detaching...

5. Какой системный вызов вызывается чаще всего?
# funccount 't:syscalls:sys_enter_*'
Tracing 316 functions for "t:syscalls:sys_enter_*"... Hit Ctrl-C to end.
^C
FUNC COUNT
syscalls:sys_enter_creat 1
[...]
syscalls:sys_enter_read 6582
syscalls:sys_enter_write 7442
syscalls:sys_enter_mprotect 7460
syscalls:sys_enter_gettid 7589
syscalls:sys_enter_ioctl 10984
syscalls:sys_enter_poll 14980
syscalls:sys_enter_recvmsg 27113
syscalls:sys_enter_futex 42929
Detaching...
```
funccount [options] eventname

Синтаксис аргумента eventname:
 - name или p:name: инструментировать функцию ядра с именем name();
 - lib:name или p:lib:name: инструментировать функцию в пространстве пользо-
вателя с именем name(), находящуюся в библиотеке lib;
 - path:name: инструментировать функцию в пространстве пользователя с именем
name(), находящуюся в файле path;
 - t:system:name: инструментировать точку трассировки с именем system:name;
 - u:lib:name: инструментировать зонд USDT в библиотеке lib с именем name;
 - *: подстановочный символ, соответствующий любой строке. Вместо него можно
использовать параметр -r с регулярным выражением.

Однострочные сценарии
```
Подсчет вызовов функций виртуальной файловой системы в ядре:
funccount 'vfs_*'

Подсчет вызовов функций TCP в ядре:
funccount 'tcp_*'

Определение частоты вызовов в секунду функций TCP:
funccount -i 1 'tcp_send*'

Определение частоты операций блочного ввода/вывода в секунду:
funccount -i 1 't:block:*'

Определение частоты запуска новых процессов в секунду:
funccount -i 1 t:sched:sched_process_fork

Определение частоты вызовов в секунду функции getaddrinfo() (разрешение имен)
из библиотеки libc:
funccount -i 1 c:getaddrinfo

Подсчет вызовов всех функций «os.*” в библиотеке libgo:
funccount 'go:os.*'
```
### stackcount
Подсчитывает трассировки стека, которые привели к событию. Событием может быть функция в пространстве ядра или пользо-
вателя, точка трассировки или зонд USDT. 
```
# stackcount ktime_get
Tracing 1 functions for "ktime_get"... Hit Ctrl-C to end.
^C
[...]
ktime_get
nvme_queue_rq
__blk_mq_try_issue_directly
blk_mq_try_issue_directly
blk_mq_make_request
generic_make_request
dmcrypt_write
kthread
ret_from_fork
52
[...]
ktime_get
tick_nohz_idle_enter
do_idle
cpu_startup_entry
start_secondary
secondary_startup_64
1077
Detaching...

# stackcount -P ktime_get
[...]
ktime_get
tick_nohz_idle_enter
do_idle
cpu_startup_entry
start_secondary
secondary_startup_64
swapper/2 [0]
207
```
Creating flamegraphs
```
# stackcount -f -P -D 10 ktime_get > out.stackcount01.txt
$ wc out.stackcount01.txt
1586 3425 387661 out.stackcount01.txt
$ git clone http://github.com/brendangregg/FlameGraph
$ cd FlameGraph
$ ./flamegraph.pl --hash --bgcolors=grey < ../out.stackcount01.txt \
> out.stackcount01.svg
```
![image](https://github.com/user-attachments/assets/3c6ac46d-7514-47c6-aea0-08ecc2066d68)

Однострочные сценарии
```
Подсчет трассировок стека, приводящих к операции блочного ввода/вывода:
stackcount t:block:block_rq_insert

Подсчет трассировок стека, приводящих к отправке IP-пакетов:
stackcount ip_output

Подсчет трассировок стека, приводящих к отправке IP-пакетов, с разделением по
PID:
stackcount -P ip_output

Подсчет трассировок стека, приводящих к блокировке потока и переходу в режим
ожидания:
stackcount t:sched:sched_switch

Подсчет трассировок стека, приводящих к системному вызову read():
stackcount t:syscalls:sys_enter_read
```
### trace
Это многофункциональный инструмент BCC для трассировки отдельных
событий из разных источников: kprobes, uprobes, tracepoints и USDT.
```
# trace 'do_sys_open "%s", arg2'
PID TID COMM FUNC -
29588 29591 device poll do_sys_open /dev/bus/usb
29588 29591 device poll do_sys_open /dev/bus/usb/004
[...]
```

Однострочные сценарии
```
Трассировка вызовов функции do_sys_open() с выводом имен открываемых
файлов:
trace 'do_sys_open "%s", arg2'

Трассировка возврата из функции ядра do_sys_open() с выводом возвращаемого
значения:
trace 'r::do_sys_open "ret: %d", retval'

Трассировка функции do_nanosleep() с выводом аргумента режима и трассировкой
стека в пространстве пользователя:
trace -U 'do_nanosleep "mode: %d", arg2'

Трассировка запросов в библиотеку pam на аутентификацию:
trace 'pam:pam_start "%s: %s", arg1, arg2'

trace 'do_nanosleep(struct hrtimer_sleeper *t) "task: %x", t->task'
```
![image](https://github.com/user-attachments/assets/13215a79-41ab-4bcd-b5f7-e2a6c210e16a)
```
# trace -tKU 'r::sock_alloc "open %llx", retval' '__sock_release "close %llx", arg1'

TIME PID TID COMM FUNC -
1.093199 4182 7101 nf.dependency.M sock_alloc open ffff9c76526dac00
kretprobe_trampoline+0x0 [kernel]
sys_socket+0x55 [kernel]
do_syscall_64+0x73 [kernel]
entry_SYSCALL_64_after_hwframe+0x3d [kernel]
__socket+0x7 [libc-2.27.so]
Ljava/net/PlainSocketImpl;::socketCreate+0xc7 [perf-4182.map]
Ljava/net/Socket;::setSoTimeout+0x2dc [perf-4182.map]
Lorg/apache/http/impl/conn/DefaultClientConnectionOperator;::openConnectio...
Lorg/apache/http/impl/client/DefaultRequestDirector;::tryConnect+0x60c [pe...
Lorg/apache/http/impl/client/DefaultRequestDirector;::execute+0x1674 [perf...
[...]

[...]
6.010530 4182 6797 nf.dependency.M __sock_release close ffff9c76526dac00
__sock_release+0x1 [kernel]
__fput+0xea [kernel]
____fput+0xe [kernel]
task_work_run+0x9d [kernel]
exit_to_usermode_loop+0xc0 [kernel]
do_syscall_64+0x121 [kernel]
entry_SYSCALL_64_after_hwframe+0x3d [kernel]
dup2+0x7 [libc-2.27.so]
Ljava/net/PlainSocketImpl;::socketClose0+0xc7 [perf-4182.map]
Ljava/net/Socket;::close+0x308 [perf-4182.map]
Lorg/apache/http/impl/conn/DefaultClientConnection;::close+0x2d4 [perf-418...
[...]
```
### argdist
```
# argdist -H 'r::__tcp_select_window():int:$retval'
[21:50:03]
$retval : count distribution
0 -> 1 : 6100 |****************************************|
2 -> 3 : 0 | |
4 -> 7 : 0 | |
8 -> 15 : 0 | |
16 -> 31 : 0 | |
32 -> 63 : 0 | |
64 -> 127 : 0 | |
128 -> 255 : 0 | |
256 -> 511 : 0 | |
512 -> 1023 : 0 | |
1024 -> 2047 : 0 | |
2048 -> 4095 : 0 | |
4096 -> 8191 : 0 | |
8192 -> 16383 : 24 | |
16384 -> 32767 : 3535 |*********************** |
32768 -> 65535 : 1752 |*********** |
65536 -> 131071 : 2774 |****************** |
131072 -> 262143 : 1001 |****** |
262144 -> 524287 : 464 |*** |
524288 -> 1048575 : 3 | |
1048576 -> 2097151 : 9 | |
2097152 -> 4194303 : 10 | |
4194304 -> 8388607 : 2 | |
[21:50:04]
[...]
```
__tcp_select_window() is a low-level function in the Linux kernel's networking stack , specifically related to TCP (Transmission Control Protocol) flow control.

It helps determine how much data the receiver is willing to accept at any given time — known as the receive window (win field in TCP header) .

The receive window is advertised by the receiving side in each TCP segment to tell the sender how much buffer space is available. This mechanism prevents the sender from overwhelming the receiver with more data than it can handle.

Однострочные сценарии
```
Вывести гистограмму результатов (размеров), возвращаемых функцией ядра
vfs_read():
argdist.py -H 'r::vfs_read()'

Вывести гистограмму результатов (размеров), возвращаемых функцией read() из
библиотеки libc в пространстве пользователя для PID 1005:
argdist -p 1005 -H 'r:c:read()'

Подсчитать число обращений к системным вызовам по их идентификаторам с ис-
пользованием точки трассировки raw_syscalls:sys_enter:
argdist.py -C 't:raw_syscalls:sys_enter():int:args->id'

Подсчитать значения аргумента size для tcp_sendmsg():
argdist -C 'p::tcp_sendmsg(struct sock *sk, struct msghdr *msg,
size_t size):u32:size'

Вывести гистограмму распределения значений аргумента size в вызовах tcp_
sendmsg():
argdist -H 'p::tcp_sendmsg(struct sock *sk, struct msghdr *msg,
size_t size):u32:size'

Подсчитать количество вызовов функции write() из библиотеки libc для PID 181
по дескрипторам файлов:
argdist -p 181 -C 'p:c:write(int fd):int:fd'

Подсчитать операции чтения по процессам, для которых величина задержки была
> 0.1 мс:
argdist -C 'r::__vfs_read():u32:$PID:$latency > 100000
```
