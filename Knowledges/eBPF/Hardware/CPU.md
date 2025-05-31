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
