# CPU
![image](https://github.com/user-attachments/assets/b62e93db-8274-456d-87b1-c462727fcf73)

## Источники событий
![image](https://github.com/user-attachments/assets/a438faca-2506-45e8-97c3-2a966c4c46be)
А также попадания в кеш (PMC) - можно связать с вызовом приложения.<br>
А также трассировка стека, нахождение что привело к событию
## Оверхед
При трассировке событий планировщика эффективность обретает особую важность,
так как некоторые события планировщика, например переключение контекста, могут происходить миллионы раз в секунду. В некоторых случаях трассировка планировщика увеличивает нагруз-
ку на систему более чем на 10%.

Трассировка планировщика с помощью BPF применяется для краткосрочного
и специализированного анализа, при этом нужно понимать, что она сопряжена
с оверхедом.

Инструментация редких событий, например запуска процессов и миграции потоков (происходящих не чаще
чем тысячу раз в секунду), порождает незначительный оверхед. Профилирование
(выборка по времени) тоже позволяет ограничить оверхед уменьшением частоты
выборки до незначительных пропорций.
## Стратегия
1. Прежде чем тратить время на инструменты анализа, убедитесь, что рабочая
нагрузка на CPU запущена. Проверьте загрузку CPU системы (например,
с помощью mpstat(1)) и убедитесь, что все CPU включены (иногда по какой-то
причине некоторые могут быть отключены).

2. Убедитесь, что рабочая нагрузка имеет вычислительный характер

 - a) определите наибольшую загрузку CPU в системе или на одном процессоре
(например, с помощью mpstat(1));

- b) определите наибольшую задержку в очереди на выполнение (например,
с помощью runqlat(1) из BCC). Программные ограничения, например,
в контейнерах, могут искусственно ограничивать доступ процессов к CPU,
поэтому производительность вычислительного приложения может быть
низкой, даже когда система практически простаивает. Этот нелогичный
сценарий можно опознать, изучив задержку в очереди на выполнение.

## PMC
В облачной среде счётчики PMC часто отключают
```
# dmesg | grep PMU
[ 2.827349] Performance Events: unsupported p6 CPU model 85 no PMU driver,
software events only.
```
### tlbstat
```
# tlbstat -C0 1
K_CYCLES K_INSTR IPC DTLB_WALKS ITLB_WALKS K_DTLBCYC K_ITLBCYC DTLB% ITLB%
2875793 276051   0.10 89709496  65862302   787913    650834    27.40 22.63
2860557 273767   0.10 88829158  65213248   780301    644292    27.28 22.52
2885138 276533   0.10 89683045  65813992   787391    650494    27.29 22.55
2532843 243104   0.10 79055465  58023221   693910    573168    27.40 22.63
[...]
```
 - K_CYCLES: тысячи тактов CPU;
 - K_INSTR: тысячи инструкций CPU;
 - IPC: инструкций на такт;
 - DTLB_WALKS: число обходов TLB данных;
 - ITLB_WALKS: число обходов TLB инструкций;
 - K_DTLBCYC: тысячи тактов, когда хотя бы один обработчик отсутствия страницы (Page-Miss Handler, PMH) был активен во время обхода TLB данных;
 - K_ITLBCYC: тысячи тактов, когда хотя бы один обработчик PMH был активен во время обхода TLB инструкций;
 - DTLB%: доля активных тактов TLB данных в общем числе тактов;
 - ITLB%: доля активных тактов TLB инструкций в общем числе тактов.

"Data TLB walk" refers to the hardware-assisted process of translating a virtual address to a physical address using the Translation Lookaside Buffer (TLB) , specifically when handling a data access (as opposed to instruction fetch).

## BPF tools
![image](https://github.com/user-attachments/assets/bbfc8c8d-0eaf-42e4-aaf8-617ebb3182ba)

## Очередь на выполнение
На 36 ядерной системе запущено 72 потока, при этом 0 idle, в очереди на выполнение 72 процесса (включая выполняющиеся)
```
# runqlat 10 1
Tracing run queue latency... Hit Ctrl-C to end.
usecs : count distribution
0 -> 1 : 1906 |*** |
2 -> 3 : 22087 |****************************************|
4 -> 7 : 21245 |************************************** |
8 -> 15 : 7333 |************* |
16 -> 31 : 4902 |******** |
32 -> 63 : 6002 |********** |
64 -> 127 : 7370 |************* |
128 -> 255 : 13001 |*********************** |
256 -> 511 : 4823 |******** |
512 -> 1023 : 1519 |** |
1024 -> 2047 : 3682 |****** |
2048 -> 4095 : 3170 |***** |
4096 -> 8191 : 5759 |********** |
8192 -> 16383 : 14549 |************************** |
16384 -> 32767 : 5589 |********** |
32768 -> 65535 : 372 | |
65536 -> 131071 : 10 |

# sar -uq 1
Linux 4.18.0-virtual (...) 01/21/2019 _x86_64_ (36 CPU)
11:06:25 PM CPU %user %nice %system %iowait %steal %idle
11:06:26 PM all 88.06 0.00  11.94   0.00    0.00   0.00
11:06:25 PM runq-sz plist-sz ldavg-1 ldavg-5 ldavg-15 blocked
11:06:26 PM 72      1030     65.90   41.52   34.75    0
[...]
```
## Измерение задержки очереди на выполнение
sched_wakeup_new - то же что и sched_wakeup, но вызывается при появлении нового потока, который будет выполняться первый раз <br>
sched_wakeup - вызывается для переключения состояния потока из состояний TASK_UNINTERRUPTABLE и TASK_INTERAPTABLE в состояние TASK_RUNNING - задача готова к выполнянию <br>
sched_switch - выполняется два раза, для прерывания предыдущей задачи и добавления ожидающей в состоянии TASK_RUNNING. <br>
Тут нужно понимать, если выполение потока прерывается из за исчерпания квоты, статус TASK_RUNNING остаётся, вызов sched_wakeup по идее и не нужен т.к. задача сразу попадает в очередь на выполнение (принудительное переключение контекста), поэтому в коде есть if конструкция.

Поскольку здесь используется макрос TASK_RUNNING, к программе подключается
файл заголовка linux/sched.h (#include), содержащий его определение.

```
#!/usr/local/bin/bpftrace
#include <linux/sched.h>

tracepoint:sched:sched_wakeup,
tracepoint:sched:sched_wakeup_new
{
@qtime[args->pid] = nsecs;
}
tracepoint:sched:sched_switch
{
if (args->prev_state == TASK_RUNNING) {
@qtime[args->prev_pid] = nsecs;
}
$ns = @qtime[args->next_pid];
if ($ns) {
@usecs = hist((nsecs - $ns) / 1000);
}
delete(@qtime[args->next_pid]);
}
END
{
clear(@qtime);
}
```
## Длина очереди на выполнение
runqlen выбирает данные по времени,с частотой 99 Гц, тогда как runqlat трассирует события планировщика.
```
# runqlen 10 1
Sampling run queue length... Hit Ctrl-C to end.
runqlen : count distribution
0 : 47284 |****************************************|
1 : 211 | |
2 : 28 | |
3 : 6 | |
4 : 4 | |
5 : 1 | |
6 : 1 | |
```
### Четыре потока один процессор
Очередь на выполнение на CPU 0 имеет длину, равную трем: один поток выполняется на процессоре и три потока ожидают своей очереди.

Вывод результатов для каждого процессора в отдельности помогает проверить правильную балансировку нагрузки на процессоры планировщиком.
```
# runqlen -C
Sampling run queue length... Hit Ctrl-C to end.
^C
cpu = 0
runqlen : count distribution
0 : 0 | |
1 : 0 | |
2 : 0 | |
3 : 551 |****************************************|
cpu = 1
runqlen : count distribution
0 : 41 |****************************************|
cpu = 2
runqlen : count distribution
0 : 126 |****************************************|
[...]
```
###  Реализация runqlen
```
#!/usr/local/bin/bpftrace
#include <linux/sched.h>

struct cfs_rq_partial {
struct load_weight load;
unsigned long runnable_weight;
unsigned int nr_running;
};

profile:hz:99
{
$task = (struct task_struct *)curtask;
$my_q = (struct cfs_rq_partial *)$task->se.cfs_rq;
$len = $my_q->nr_running;
$len = $len > 0 ? $len - 1 : 0; // учесть текущую выполняемую задачу
@runqlen = lhist($len, 0, 100, 1);
}
```
## runqslower (задержка больше чем..)
```
# runqslower
Tracing run queue latency higher than 10000 us
TIME COMM PID LAT(us)
17:42:49 python3 4590 16345
17:42:50 pool-25-thread- 4683 50001
17:42:53 ForkJoinPool.co 5898 11935
17:42:56 python3 4590 10191
17:42:56 ForkJoinPool.co 5912 13738
17:42:56 ForkJoinPool.co 5908 11434
17:42:57 ForkJoinPool.co 5890 11436
17:43:00 ForkJoinPool.co 5477 10502
17:43:01 grpc-default-wo 5794 11637
17:43:02 tomcat-exec-296 6373 12083
[...]
```
## cpudist (распределение времени выполнения потоков на CPU после возобновления.
Пример когда потоки завершаются быстро за микросекунды
```
# cpudist 10 1
Tracing on-CPU time... Hit Ctrl-C to end.
usecs : count distribution
0 -> 1 : 103865 |*************************** |
2 -> 3 : 91142 |************************ |
4 -> 7 : 134188 |*********************************** |
8 -> 15 : 149862 |****************************************|
16 -> 31 : 122285 |******************************** |
32 -> 63 : 71912 |******************* |
64 -> 127 : 27103 |******* |
128 -> 255 : 4835 |* |
256 -> 511 : 692 | |
512 -> 1023 : 320 | |
1024 -> 2047 : 328 | |
2048 -> 4095 : 412 | |
4096 -> 8191 : 356 | |
8192 -> 16383 : 69 | |
16384 -> 32767 : 42 | |
32768 -> 65535 : 30 | |
65536 -> 131071 : 22 | |
131072 -> 262143 : 20 | |
262144 -> 524287 : 4 | |
```
Распределение в миллисекундах, рабочая нагрузка с количеством потоков больше cpu, видна четкая мода от 8 до 15 (не меньше не больше), скорее всего потоки исчерпывают выделенные им кванты времени, после чего планировщик переключает контекст.
```
# cpudist -m
Tracing on-CPU time... Hit Ctrl-C to end.
^C
msecs : count distribution
0 -> 1 : 521 |****************************************|
2 -> 3 : 60 |**** |
4 -> 7 : 272 |******************** |
8 -> 15 : 308 |*********************** |
16 -> 31 : 66 |***** |
32 -> 63 : 14 |* |
```
## cpufreq
Выборка значений частоты процессора

Работает только при настройке регулятора частоты CPU на определенный режим, например
энергосбережения (powersave), и может использоваться для определения тактовой
частоты, с которой выполняются приложения. 
```
# cpufreq.bt
Sampling CPU freq system-wide & by process. Ctrl-C to end.
^C
[...]
@process_mhz[snmpd]:
[1200, 1400) 1 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
@process_mhz[python3]:
[1600, 1800) 1 |@ |
[1800, 2000) 0 | |
[2000, 2200) 0 | |
[2200, 2400) 0 | |
[2400, 2600) 0 | |
[2600, 2800) 2 |@@@ |
[2800, 3000) 0 | |
[3000, 3200) 29 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
@process_mhz[java]:
[1200, 1400) 216 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[1400, 1600) 23 |@@@@@ |
[1600, 1800) 18 |@@@@ |
[1800, 2000) 16 |@@@ |
[2000, 2200) 12 |@@ |
[2200, 2400) 0 | |
[2400, 2600) 4 | |
[2600, 2800) 2 | |
[2800, 3000) 1 | |
[3000, 3200) 18 |@@@@ |
@system_mhz:
[1200, 1400) 22041 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[1400, 1600) 903 |@@ |
[1600, 1800) 474 |@ |
[1800, 2000) 368 | |
[2000, 2200) 30 | |
[2200, 2400) 3 | |
[2400, 2600) 21 | |
[2600, 2800) 33 | |
[2800, 3000) 15 | |
[3000, 3200) 270 | |
[...]
```
Реализация
```
tracepoint:power:cpu_frequency
{
@curfreq[cpu] = args->state;
}
profile:hz:100
/@curfreq[cpu]/
{
@system_mhz = lhist(@curfreq[cpu] / 1000, 0, 5000, 200);
if (pid) {
@process_mhz[comm] = lhist(@curfreq[cpu] / 1000, 0, 5000, 200);
}
}
END
{
clear(@curfreq);
}
```
## profile
Выбирает трассировки стека с заданным интервалом и сообщает частоту каждой из них.

Для понимания особенностей потребления CPU, так как он обобщает практически все пути кода, характеризующиеся высоким потреблением
вычислительных ресурсов.
```
# profile
Sampling at 49 Hertz of all threads by user + kernel stack... Hit Ctrl-C to end.
^C
sk_stream_alloc_skb
sk_stream_alloc_skb
tcp_sendmsg_locked
tcp_sendmsg
sock_sendmsg
sock_write_iter
__vfs_write
vfs_write
ksys_write
do_syscall_64
entry_SYSCALL_64_after_hwframe
__GI___write
[unknown]
- iperf (29136)
1

[...]
__free_pages_ok
__free_pages_ok
skb_release_data
__kfree_skb
tcp_ack
tcp_rcv_established
tcp_v4_do_rcv
__release_sock
release_sock
tcp_sendmsg
sock_sendmsg
sock_write_iter
__vfs_write
vfs_write
ksys_write
do_syscall_64
entry_SYSCALL_64_after_hwframe
__GI___write
[unknown]
- iperf (29136)
1889

get_page_from_freelist
get_page_from_freelist
__alloc_pages_nodemask
skb_page_frag_refill
sk_page_frag_refill
tcp_sendmsg_locked
tcp_sendmsg
sock_sendmsg
sock_write_iter
__vfs_write
vfs_write
ksys_write
do_syscall_64
entry_SYSCALL_64_after_hwframe
__GI___write
[unknown]
- iperf (29136)
2673
```
Реализация
```
bpftrace -e 'profile:hz:49 /pid/ { @samples[ustack, kstack, comm] = count(); }'
```
## offcputime
Подсчитывает время, потраченное потоками в ожидании на блокировках и в очереди на выполнение,
и отображающий соответствующие трассировки стека. Этот инструмент помогает
понять, почему потоки не выполнялись на процессоре. offcputime является аналогом profile. Вместе они показывают все время, потраченное потоками в системе:

profile показывает время выполнения на процессоре, а offcputime — время
ожидания вне процессора.
```
# offcputime 5
Tracing off-CPU time (us) of all threads by user + kernel stack for 5 secs.
[...]
finish_task_switch
schedule
schedule_timeout
wait_woken
sk_stream_wait_memory
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
__write
[unknown]
- iperf (14657)
5625

[...]
finish_task_switch
schedule
schedule_timeout
wait_woken
sk_wait_data
tcp_recvmsg
inet_recvmsg
sock_recvmsg
SYSC_recvfrom
sys_recvfrom
do_syscall_64
entry_SYSCALL_64_after_hwframe
recv
- iperf (14659)
1021497

[...]
finish_task_switch
schedule
schedule_hrtimeout_range_clock
schedule_hrtimeout_range
poll_schedule_timeout
do_select
core_sys_select
sys_select
do_syscall_64
entry_SYSCALL_64_after_hwframe
__libc_select
[unknown]
- offcputime (14667)
5004039
```
Реализация
```
#!/usr/local/bin/bpftrace
#include <linux/sched.h>

kprobe:finish_task_switch
{
// записать время простоя предыдущего потока
$prev = (struct task_struct *)arg0;
if ($1 == 0 || $prev->tgid == $1) {
@start[$prev->pid] = nsecs;
}
// получить время запуска текущего потока
$last = @start[tid];
if ($last != 0) {
@[kstack, ustack, comm] = sum(nsecs - $last);
delete(@start[tid]);
}
}
END
{
clear(@start);
}
```
## syscount
Подсчитывает количество системных вызовов во всей системе в целом.
```
# syscount -i 1
Tracing syscalls, printing top 10... Ctrl+C to quit.
[00:04:18]
SYSCALL COUNT
futex 152923
read 29973
epoll_wait 27865
write 21707
epoll_ctl 4696
poll 2625
writev 2460
recvfrom 1594
close 1385
sendto 1343
[...]

# syscount -Pi 1
Tracing syscalls, printing top 10... Ctrl+C to quit.
[00:04:25]
PID COMM COUNT
3622 java 294783
990 snmpd 124
2392 redis-server 64
4790 snmp-pass 32
27035 python 31
26970 sshd 24
2380 svscan 11
2441 atlas-system-ag 5
2453 apache2 2
4786 snmp-pass 1
[...]
```
В своей работе этот инструмент использует точку трассировки raw_syscalls:sys_enter вместо привычных syscalls:sys_enter_*. Использование этой единой точки
трассировки, которая может видеть все системные вызовы, ускоряет начальную инструментацию. Но она имеет свой недостаток: ей доступны только идентификаторы системных вызовов, которые нужно дополнительно преобразовать в имена. <br>
Реализация
```
# bpftrace -e 't:syscalls:sys_enter_* { @[probe] = count(); }'
Attaching 316 probes...
^C
[...]
@[tracepoint:syscalls:sys_enter_ioctl]: 9465
@[tracepoint:syscalls:sys_enter_epoll_wait]: 9807
@[tracepoint:syscalls:sys_enter_gettid]: 10311
@[tracepoint:syscalls:sys_enter_futex]: 14062
@[tracepoint:syscalls:sys_enter_recvmsg]: 22342
```
 Сейчас во время
запуска программы возникает некоторая задержка из-за необходимости инстру-
ментировать все 316 точек трассировки. Предпочтительнее было бы использовать
одну точку трассировки raw_syscalls:sys_enter, как это делает BCC, но в этом случае
придется дополнительно преобразовывать идентификаторы системных вызовов
в их имена. 
## argdist и trace
```
tplist -v syscalls:sys_enter_read
..
syscalls:sys_enter_read
int __syscall_nr;
unsigned int fd;
char * buf;
size_t count;

# argdist -H 't:syscalls:sys_enter_read():int:args->count'
[09:08:31]
args->count : count distribution
0 -> 1 : 169 |***************** |
2 -> 3 : 243 |************************* |
4 -> 7 : 1 | |
8 -> 15 : 0 | |
16 -> 31 : 384 |****************************************|
32 -> 63 : 0 | |
64 -> 127 : 0 | |
128 -> 255 : 0 | |
256 -> 511 : 0 | |
512 -> 1023 : 0 | |
1024 -> 2047 : 267 |*************************** |
2048 -> 4095 : 2 | |
4096 -> 8191 : 23 |** |
[...]

# argdist -H 't:syscalls:sys_exit_read():int:args->ret'
[09:12:58]
args->ret : count distribution
0 -> 1 : 481 |****************************************|
2 -> 3 : 116 |********* |
4 -> 7 : 1 | |
8 -> 15 : 29 |** |
16 -> 31 : 6 | |
32 -> 63 : 31 |** |
64 -> 127 : 8 | |
128 -> 255 : 2 | |
256 -> 511 : 1 | |
512 -> 1023 : 2 | |
1024 -> 2047 : 13 |* |
2048 -> 4095 : 2 | |
[...]
```
Реализация
```
# bpftrace -e 't:syscalls:sys_enter_read { @ = hist(args->count); }'
Attaching 1 probe...
^C
@:
[1] 1102 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[2, 4) 902 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ |
[4, 8) 20 | |
[8, 16) 17 | |
[16, 32) 538 |@@@@@@@@@@@@@@@@@@@@@@@@@ |
[32, 64) 56 |@@ |
[64, 128) 0 | |
[128, 256) 0 | |
[256, 512) 0 | |
[512, 1K) 0 | |
[1K, 2K) 119 |@@@@@ |
[2K, 4K) 26 |@ |
[4K, 8K) 334 |@@@@@@@@@@@@@@@ |

# bpftrace -e 't:syscalls:sys_exit_read { @ = hist(args->ret); }'
Attaching 1 probe...
^C
@:
(..., 0) 105 |@@@@ |
[0] 18 | |
[1] 1161 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[2, 4) 196 |@@@@@@@@ |
[4, 8) 8 | |
[8, 16) 384 |@@@@@@@@@@@@@@@@@ |
[16, 32) 87 |@@@ |
[32, 64) 118 |@@@@@ |
[64, 128) 37 |@ |
[128, 256) 6 | |
[256, 512) 13 | |
[512, 1K) 3 | |
[1K, 2K) 3 | |
[2K, 4K) 15 | |
```
Распределение ошибок
```
# bpftrace -e 't:syscalls:sys_exit_read /args->ret < 0/ {
@ = lhist(- args->ret, 0, 100, 1); }'
Attaching 1 probe...
^C
@:
[11, 12) 123 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
```
## funccount
В своей работе funccount использует метод динамической трассировки функций:
зонды kprobes для функций ядра и uprobes для функций в пространстве пользо-
вателя
```
# funccount 'tcp_*'
Tracing 316 functions for "tcp_*"... Hit Ctrl-C to end.
^C
FUNC COUNT
[...]
tcp_stream_memory_free 368048
tcp_established_options 381234
tcp_v4_md5_lookup 402945
tcp_gro_receive 484571
tcp_md5_do_lookup 510322
Detaching...

# funccount -i 1 get_page_from_freelist
..
Tracing 1 functions for "get_page_from_freelist"... Hit Ctrl-C to end.

FUNC COUNT
get_page_from_freelist 586452

FUNC COUNT
get_page_from_freelist 586241
[...]
```
Реализация
```
# bpftrace -e 'k:tcp_* { @[probe] = count(); }'
Attaching 320 probes...
[...]
@[kprobe:tcp_release_cb]: 153001
@[kprobe:tcp_v4_md5_lookup]: 154896
@[kprobe:tcp_gro_receive]: 177187
```
## softirqs
Показывает время затраченное на обработку программных прерываний

В своей работе softirqs использует точки трассировки irq:softirq_enter и irq:softirq_
exit.
```
# softirqs 10 1
..
Tracing soft irq event time... Hit Ctrl-C to end.
SOFTIRQ TOTAL_usecs
net_tx 633
tasklet 30939
rcu 143859
sched 185873
timer 389144
net_rx 1358268
```
Согласно этим результатам, наибольшее время было потрачено на обработку прерывания net_rx, всего 1358 миллисекунд. Это довольно много — 3% процессорного
времени в 48-процессорной системе.

Реализация
```
# bpftrace -e 'tracepoint:irq:softirq_entry { @[args->vec] = count(); }'
Attaching 1 probe...
^C
@[3]: 11
@[6]: 45
@[0]: 395
@[9]: 405
@[1]: 524
@[7]: 561
```
## hardirqs
Показывает время затраченное на обработку аппаратных прерываний

В своей работе этот инструмент использует прием динамической трассировки
функции ядра handle_irq_event_percpu(), но будущие версии будут применять
точки трассировки irq:irq_handler_entry и irq:irq_handler_exit.
```
# hardirqs 10 1
Tracing hard irq event time... Hit Ctrl-C to end.
HARDIRQ                    TOTAL_usecs
ena-mgmnt@pci:0000:00:05.0 43
nvme0q0                    46
eth0-Tx-Rx-7               47424
eth0-Tx-Rx-6               48199
eth0-Tx-Rx-5               48524
eth0-Tx-Rx-2               49482
eth0-Tx-Rx-3               49750
eth0-Tx-Rx-0               51084
eth0-Tx-Rx-4               51106
eth0-Tx-Rx-1               52649
```
Параметр -d можно использовать для изучения распределения и выявления задержек, возникающих при обработке прерываний.
## smpcalls
Отслеживание и суммирование времени в функциях вызовов SMP (также известных как перекрестные вызовы). Поддержка таких вызовов позволяет одному процессору запускать функции на любых других процессорах и может приводить к сильному оверхеду в больших многопроцессорных
системах. Вот пример трассировки в системе с 36 процессорами:
```
# smpcalls.bt
Attaching 8 probes...
Tracing SMP calls. Hit Ctrl-C to stop.
^C
@time_ns[do_flush_tlb_all]:
[32K, 64K) 1 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[64K, 128K) 1 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
@time_ns[remote_function]:
[4K, 8K) 1 |@@@@@@@@@@@@@@@@@@@@@@@@@@ |
[8K, 16K) 1 |@@@@@@@@@@@@@@@@@@@@@@@@@@ |
[16K, 32K) 0 | |
[32K, 64K) 2 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
@time_ns[do_sync_core]:
[32K, 64K) 15 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[64K, 128K) 9 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ |
@time_ns[native_smp_send_reschedule]:
[2K, 4K) 7 |@@@@@@@@@@@@@@@@@@@ |
[4K, 8K) 3 |@@@@@@@@ |
[8K, 16K) 19 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[16K, 32K) 3 |@@@@@@@@ |
@time_ns[aperfmperf_snapshot_khz]:
[1K, 2K) 5 |@ |
[2K, 4K) 12 |@@@ |
[4K, 8K) 12 |@@@ |
[8K, 16K) 6 |@ |
[16K, 32K) 1 | |
[32K, 64K) 196 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[64K, 128K) 20 |@@@@@ |
```
Реализация
```
kprobe:smp_call_function_single,
kprobe:smp_call_function_many
{
@ts[tid] = nsecs;
@func[tid] = arg1;
}
kretprobe:smp_call_function_single,
kretprobe:smp_call_function_many
/@ts[tid]/
{
@time_ns[ksym(@func[tid])] = hist(nsecs - @ts[tid]);
delete(@ts[tid]);
delete(@func[tid]);
}
kprobe:native_smp_send_reschedule
{
@ts[tid] = nsecs;
@func[tid] = reg("ip");
}
kretprobe:native_smp_send_reschedule
/@ts[tid]/
{
@time_ns[ksym(@func[tid])] = hist(nsecs - @ts[tid]);
delete(@ts[tid]);
delete(@func[tid]);
}
END
{
clear(@ts);
clear(@func);
}
```
Многие из SMP-вызовов можно трассировать с помощью зондов kprobes для
функций ядра smp_call_function_single() и smp_call_function_many(). Во втором
аргументе этим функциям передается указатель на функцию для запуска на удаленном CPU, который в bpftrace доступен как arg1

Ключ гистограммы @time_ns можно изменить и включить в него трассировку стека
ядра и имя процесса:
@time_ns[comm, kstack, ksym(@func[tid])] = hist(nsecs - @ts[tid]);
```
@time_ns[snmp-pass,
smp_call_function_single+1
aperfmperf_snapshot_cpu+90
arch_freq_prepare_all+61
cpuinfo_open+14
proc_reg_open+111
do_dentry_open+484
path_openat+692
do_filp_open+153
do_sys_open+294
do_syscall_64+85
entry_SYSCALL_64_after_hwframe+68
, aperfmperf_snapshot_khz]:
[2K, 4K) 2 |@@ |
[4K, 8K) 0 | |
[8K, 16K) 1 |@ |
[16K, 32K) 1 |@ |
[32K, 64K) 51 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[64K, 128K) 17 |@@@@@@@@@@@@@@@@@
```
В этом выводе видно, что процесс snmp-pass, агент мониторинга, выполнил систем-
ный вызов open(), который заканчивается вызовом cpuinfo_open() и дорогостоящим
перекрестным вызовом
```
# opensnoop.py -Tn snmp-pass
TIME(s) PID COMM FD ERR PATH
0.000000000 2440 snmp-pass 4 0 /proc/cpuinfo
0.000841000 2440 snmp-pass 4 0 /proc/stat
1.022128000 2440 snmp-pass 4 0 /proc/cpuinfo
1.024696000 2440 snmp-pass 4 0 /proc/stat
2.046133000 2440 snmp-pass 4 0 /proc/cpuinfo
2.049020000 2440 snmp-pass 4 0 /proc/stat
3.070135000 2440 snmp-pass 4 0 /proc/cpuinfo
3.072869000 2440 snmp-pass 4 0 /proc/stat
[...]
```
Этот вывод показывает, что snmp-pass читает файл /proc/cpuinfo каждую секунду!
Большинство деталей в этом файле не меняется, кроме поля «CPU MHz».
Исследование исходного кода показало, что это ПО читает /proc/cpuinfo только
для того, чтобы узнать количество процессоров. Поле «CPU MHz» им вообще не
анализируется. Это пример выполнения ненужной работы, устранение которой
должно обеспечить небольшой, но легкий выигрыш.
На процессорах Intel эти SMP-вызовы реализованы как вызовы x2APIC IPI (Inter-
Processor Interrupt — межпроцессорные прерывания), включая x2apic_send_IPI().
## llcstat
Использует счетчики PMC для отображения частоты промахов и попаданий в кэш последнего уровня (Last-Level Cache, LLC) по процессам.
```
# llcstat
Running for 10 seconds or hit Ctrl-C to end.
PID NAME CPU REFERENCE MISS HIT%
0 swapper/15 15 1007300 1000 99.90%
4435 java 18 22000 200 99.09%
4116 java 7 11000 100 99.09%
4441 java 38 32200 300 99.07%
17387 java 17 10800 100 99.07%
4113 java 17 10500 100 99.05%
[...]
```
процесс может случайно переполнить счетчик промахов раньше, чем счетчик ссылок,
что не учитывается инструментом (потому что промахи — это подмножество ссылок).
## Однострочники
```
Трассирует запуск новых процессов и их аргументы:
bpftrace -e 'tracepoint:syscalls:sys_enter_execve { join(args->argv); }'

Сообщает, кто и что выполняет:
bpftrace -e 'tracepoint:syscalls:sys_enter_execve { printf("%s -> %s\n", comm,
str(args->filename)); }'

Выводит число системных вызовов, выполненных каждой программой:
bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'

Выводит число системных вызовов, выполненных каждым процессом:
bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[pid, comm] = count(); }'

Выводит число обращений к каждому системному вызову, используя его зонд:
bpftrace -e 'tracepoint:syscalls:sys_enter_* { @[probe] = count(); }'

Выводит число обращений к каждому системному вызову, используя имя функции:
bpftrace -e 'tracepoint:raw_syscalls:sys_enter {
@[sym(*(kaddr("sys_call_table") + args->id * 8))] = count(); }'

Выбирает имена работающих процессов с частотой 99 Гц:
bpftrace -e 'profile:hz:99 { @[comm] = count(); }'
Выбирает трассировки стека в пространстве пользователя с частотой 49 Гц для
PID 189:
bpftrace -e 'profile:hz:49 /pid == 189/ { @[ustack] = count(); }'

Выбирает все трассировки стека и имена процессов:
bpftrace -e 'profile:hz:49 { @[ustack, stack, comm] = count(); }'

Выбирает работающие процессоры с частотой 99 Гц и выводит собранную инфор-
мацию в виде линейной гистограммы:
bpftrace -e 'profile:hz:99 { @cpu = lhist(cpu, 0, 256, 1); }'

Подсчитывает число вызовов функций ядра с именами, начинающимися на «vfs_»:
bpftrace -e 'kprobe:vfs_* { @[func] = count(); }'

Подсчитывает SMP-вызовы по именам и трассировкам стека ядра:
bpftrace -e 'kprobe:smp_call* { @[probe, kstack(5)] = count(); }'

Подсчитывает вызовы Intel x2APIC по именам и трассировкам стека ядра:
bpftrace -e 'kprobe:x2apic_send_IPI* { @[probe, kstack(5)] = count(); }'

Трассирует запуск новых потоков вызовом pthread_create():
bpftrace -e 'u:/lib/x86_64-linux-gnu/libpthread-2.27.so:pthread_create {
printf("%s by %s (%d)\n", probe, comm, pid); }'
```
## EEVDF Scheduler
```
bpftrace -e 'kprobe:pick_eevdf { @samples[ustack, kstack, comm] = count(); }'
..
@samples[
,
    pick_eevdf+1
    pick_task_fair+78
    pick_next_task_fair+68
    __pick_next_task+62
    __schedule+263
    schedule_idle+31
    do_idle+166
    cpu_startup_entry+37
    start_secondary+280
    common_startup_64+318
, swapper/3]: 1032

@samples[
,
    pick_eevdf+1
    pick_task_fair+78
    pick_next_task_fair+68
    __pick_next_task+62
    __schedule+263
    schedule+38
    schedule_timeout+115
    kcompactd+563
    kthread+253
    ret_from_fork+48
    ret_from_fork_asm+26
, kcompactd0]: 8

@samples[
,
    pick_eevdf+1
    pick_task_fair+78
    pick_next_task_fair+68
    __pick_next_task+62
    __schedule+263
    schedule+38
    worker_thread+392
    kthread+253
    ret_from_fork+48
    ret_from_fork_asm+26
, kworker/2:0]: 7

@samples[
    runtime.futex.abi0+35
    runtime.notesleep+135
    runtime.stoplockedm+115
    runtime.schedule+58
    runtime.park_m+645
    runtime.mcall+78
    runtime.gopark+206
    runtime.chansend+933
    runtime.chansend1+23
    github.com/aquasecurity/libbpfgo.ringbufferCallback+156
    _cgoexp_3e8df8ae2b51_ringbufferCallback+37
    runtime.cgocallbackg1+651
    runtime.cgocallbackg+307
    runtime.cgocallbackg.abi0+41
    runtime.cgocallback.abi0+204
    crosscall2+65
    0x7f06f7fff0f0
    ringbufferCallback+117
    ringbuf_process_ring+95
    0x1
    0xd0758948d87d8948
,
    pick_eevdf+1
    pick_task_fair+78
    pick_next_task_fair+68
    __pick_next_task+62
    __schedule+263
    schedule+38
    futex_wait_queue+101
    __futex_wait+312
    futex_wait+100
    do_futex+312
    __x64_sys_futex+115
    do_syscall_64+96
    entry_SYSCALL_64_after_hwframe+118
, ebpf_exporter]: 6

@samples[
    runtime.usleep.abi0+55
    runtime.sysmon+165
    runtime.mstart1+147
    runtime.mstart0+117
    runtime.mstart.abi0+5
    start_thread+780
,
    pick_eevdf+1
    pick_task_fair+78
    pick_next_task_fair+68
    __pick_next_task+62
    __schedule+263
    schedule+38
    do_nanosleep+92
    hrtimer_nanosleep+119
    __x64_sys_nanosleep+172
    do_syscall_64+96
    entry_SYSCALL_64_after_hwframe+118
, ebpf_exporter]: 6
```
