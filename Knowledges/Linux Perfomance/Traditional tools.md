# Traditional tools
# Tracing and profiling
## perf
perf is a powerful profiling tool built into the Linux kernel that allows you to analyze system and application performance using hardware and software counters.

perf is Linux interface to PMC/PMU (Perfomance monitoring counter/unit) registers on the core.

PMC counts events such as:
- Number of instructions executed
- CPU cycles used
- Cache hits/misses
- Branch predictions (correct/incorrect)
- Memory accesses
- TLB misses
- Floating-point operations
- Page faults

Perf features:
- Monitor CPU cycles, cache misses, branch predictions
- Profile functions in user or kernel space
- Sample call graphs (stack traces)
- Trace events and system behavior
```
perf -h
..
 usage: perf [--version] [--help] [OPTIONS] COMMAND [ARGS]

 The most commonly used perf commands are:
   annotate        Read perf.data (created by perf record) and display annotated code
   archive         Create archive with object files with build-ids found in perf.data file
   bench           General framework for benchmark suites
   buildid-cache   Manage build-id cache.
   buildid-list    List the buildids in a perf.data file
   c2c             Shared Data C2C/HITM Analyzer.
   config          Get and set variables in a configuration file.
   daemon          Run record sessions on background
   data            Data file related processing
   diff            Read perf.data files and display the differential profile
   evlist          List the event names in a perf.data file
   ftrace          simple wrapper for kernel's ftrace functionality
   inject          Filter to augment the events stream with additional information
   iostat          Show I/O performance metrics
   kallsyms        Searches running kernel for symbols
   kvm             Tool to trace/measure kvm guest os
   list            List all symbolic event types
   mem             Profile memory accesses
   record          Run a command and record its profile into perf.data
   report          Read perf.data (created by perf record) and display the profile
   script          Read perf.data (created by perf record) and display trace output
   stat            Run a command and gather performance counter statistics
   test            Runs sanity tests.
   top             System profiling tool.
   version         display the version of perf binary
   probe           Define new dynamic tracepoints
   trace           strace inspired tool
   kmem            Tool to trace/measure kernel memory properties
   kwork           Tool to trace/measure kernel work properties (latencies)
   lock            Analyze lock events
   sched           Tool to trace/measure scheduler properties (latencies)
   timechart       Tool to visualize total system behavior during a workload

perf sched -h
..
 Usage: perf sched [<options>] {record|latency|map|replay|script|timehist}

    -D, --dump-raw-trace  dump raw trace in ASCII
    -f, --force           don't complain, do it
    -i, --input <file>    input file name
    -v, --verbose         be more verbose (show symbol address, etc)
```
### Profile an application
```
perf record -g python3
ls perf.data
perf report
..
```
![image](https://github.com/user-attachments/assets/7b4938c1-87e2-4ee2-8c7c-32c1878f5bd4)
### Measure CPU cycles
```
perf stat -e cycles,instructions sleep 5
```
![image](https://github.com/user-attachments/assets/1c4d82ca-3953-4a62-ae28-7198b83db002)
### Trace all syscalls made by a process
```
perf trace -p <PID>
```
### Trace scheduler
```
perf sched record
perf report
```
![image](https://github.com/user-attachments/assets/d48affe5-392c-4919-9c66-e43d8de25a0f)
![image](https://github.com/user-attachments/assets/1133d500-78c9-45b6-91c7-2cf89890e7af)
## ftrace
ftrace is a tracing mechanism built directly into the Linux kernel. It helps trace kernel-level function calls, latencies, interrupts, scheduling, etc.
- Low overhead
- Good for deep kernel debugging
- Accessed through the debugfs filesystem (/debug/tracing)
```
mount -t debugfs none /debug
..
mount: /debug: mount point does not exist.

mkdir /debug
mount -t debugfs none /debug
ls /debug/
..
acpi              devices_deferred  fault_around_bytes  mei_wdt                regulator         ttm
bdi               dma_buf           gpio                multigrain_timestamps  sched             usb
block             dma_pools         hid                 opp                    slab              wakeup_sources
cec               dmaengine         i2c                 phy                    sleep_time        x86
check_wx_pages    dri               intel_lpss          pinctrl                split_huge_pages  xfs
clear_warn_once   dynamic_debug     intel_powerclamp    pkg_temp_thermal       stackdepot        zsmalloc
clk               eeepc-wmi         kprobes             pm_genpd               suspend_stats
cxl               energy_model      kvm                 pwm                    swiotlb
devfreq           error_injection   mce                 ras                    thunderbolt
device_component  extfrag           mei0                regmap                 tracing
```
### Enable function tracing
```
cat /debug/tracing/trace
..
# tracer: nop

echo function > /debug/tracing/current_tracer
tail -n 100000 /debug/tracing/trace | grep tail | head -n 15
..
            grep-4500    [003] .....  3110.578235: free_tail_page_prepare <-free_frozen_pages
            head-4501    [001] .....  3110.579528: free_tail_page_prepare <-free_frozen_pages
            tail-4499    [002] .....  3110.587621: get_symbol_offset <-kallsyms_lookup_buildid
            tail-4499    [002] ...1.  3111.167456: preempt_count_sub <-_raw_spin_unlock_irqrestore
            tail-4499    [002] d....  3111.271392: preempt_count_add <-_raw_spin_lock
            tail-4499    [002] .....  3111.293579: mutex_unlock <-seq_read_iter
            tail-4499    [002] d..1.  3111.299016: _raw_spin_unlock <-ring_buffer_empty_cpu.part.0.isra.0
            tail-4499    [002] d..1.  3111.299016: preempt_count_sub <-_raw_spin_unlock
            tail-4499    [002] .....  3111.299016: _raw_spin_lock_irqsave <-ring_buffer_iter_peek
            tail-4499    [002] d....  3111.299016: preempt_count_add <-__raw_spin_lock_irqsave
            tail-4499    [002] d..1.  3111.299016: _raw_spin_unlock_irqrestore <-ring_buffer_iter_peek
            tail-4499    [002] ...1.  3111.299017: preempt_count_sub <-_raw_spin_unlock_irqrestore
            tail-4499    [002] d....  3111.299017: _raw_spin_lock <-ring_buffer_empty_cpu.part.0.isra.0
            tail-4499    [002] d....  3111.299017: preempt_count_add <-_raw_spin_lock
            tail-4499    [002] d..1.  3111.299017: _raw_spin_unlock <-ring_buffer_empty_cpu.part.0.isra.0
```
### Select only specific functions
```
cat /debug/tracing/set_ftrace_filter
..
#### all functions enabled ####

cat /debug/tracing/trace | tail -n 20000 | less
..
 ebpf_exporter-715     [002] .....  3658.180704: schedule <-futex_wait_queue
   ebpf_exporter-722     [000] .....  3658.180717: schedule <-schedule_hrtimeout_range_clock
   ebpf_exporter-722     [000] .....  3658.180741: schedule <-do_nanosleep
   ebpf_exporter-715     [002] .....  3658.180750: schedule <-schedule_hrtimeout_range_clock
   ebpf_exporter-807     [001] .....  3658.180798: schedule <-futex_wait_queue
   ebpf_exporter-722     [000] .....  3658.180798: schedule <-futex_wait_queue
   ebpf_exporter-722     [000] .....  3658.180824: schedule <-schedule_hrtimeout_range_clock
   ebpf_exporter-807     [001] .....  3658.180858: schedule <-do_nanosleep
   ebpf_exporter-701     [000] .....  3658.180871: schedule <-do_nanosleep
   ebpf_exporter-715     [002] .....  3658.180876: schedule <-futex_wait_queue
   ebpf_exporter-722     [000] .....  3658.180878: schedule <-schedule_hrtimeout_range_clock
   ebpf_exporter-807     [002] .....  3658.180929: schedule <-futex_wait_queue
 systemd-journal-520     [001] .....  3658.181113: schedule <-schedule_hrtimeout_range_clock
   ebpf_exporter-701     [000] .....  3658.182206: schedule <-futex_wait_queue
     rcu_preempt-18      [003] .....  3658.184726: schedule <-schedule_timeout
     rcu_preempt-18      [003] .....  3658.188726: schedule <-schedule_timeout
     rcu_preempt-18      [003] .....  3658.192725: schedule <-schedule_timeout
     rcu_preempt-18      [003] .....  3658.196725: schedule <-rcu_gp_kthread
   ebpf_exporter-748     [001] .....  3658.221111: schedule <-schedule_hrtimeout_range_clock
   ebpf_exporter-701     [000] .....  3658.221132: schedule <-do_nanosleep
   ebpf_exporter-670     [002] .....  3658.221150: schedule <-schedule_hrtimeout_range_clock
   ebpf_exporter-701     [000] .....  3658.221207: schedule <-do_nanosleep
   ebpf_exporter-701     [000] .....  3658.221281: schedule <-futex_wait_queue
   ebpf_exporter-750     [003] .....  3658.222701: schedule <-schedule_hrtimeout_range_clock
   ebpf_exporter-701     [000] .....  3658.222722: schedule <-do_nanosleep
   ebpf_exporter-701     [000] .....  3658.222798: schedule <-futex_wait_queue
      kcompactd0-52      [003] .....  3658.225717: schedule <-schedule_timeout
   kworker/u16:2-44      [001] .....  3658.337723: schedule <-worker_thread
   kworker/u16:0-4517    [002] .....  3658.337738: schedule <-worker_thread
```
#### Question: Why do I see alot of these calls?
```
cat /debug/tracing/trace | tail -n 20000 | head -n 100
..
            tail-4541    [000] .....  3673.663321: schedule <-pipe_read
            tail-4541    [000] .....  3673.663407: schedule <-pipe_read
            tail-4541    [000] .....  3673.663493: schedule <-pipe_read
            tail-4541    [000] .....  3673.663579: schedule <-pipe_read
            tail-4541    [000] .....  3673.663664: schedule <-pipe_read
```
You're seeing a lot of schedule function calls in the context of pipe_read when tracing the scheduler with ftrace. This is normal and expected behavior, especially if the process is waiting on data from a pipe (e.g., stdin or inter-process communication) .
- The process tail-4541 was running.
- It called pipe_read() — which means it's trying to read from a pipe.
- There was no data available to read at that moment.
- So it called schedule() to voluntarily give up the CPU and wait for data to arrive.
- Later, when data becomes available, the kernel will wake up this task and it will run again.
### Trace scheduling latency
```
??? echo "" > /debug/tracing/set_ftrace_filter (Should I set to all before that?)
echo wakeup > /debug/tracing/current_tracer
..
cat /debug/tracing/trace
# tracer: wakeup
#
# wakeup latency trace v1.1.5 on 6.14.6-1.el9.elrepo.x86_64
# --------------------------------------------------------------------
# latency: 18 us, #6/6, CPU#0 | (M:desktop VP:0, KP:0, SP:0 HP:0 #P:4)
#    -----------------
#    | task: migration/0-21 (uid:0 nice:0 policy:1 rt_prio:99)
#    -----------------
#
#                    _------=> CPU#
#                   / _-----=> irqs-off/BH-disabled
#                  | / _----=> need-resched
#                  || / _---=> hardirq/softirq
#                  ||| / _--=> preempt-depth
#                  |||| / _-=> migrate-disable
#                  ||||| /     delay
#  cmd     pid     |||||| time  |   caller
#     \   /        ||||||  \    |    /
  <idle>-0         0dNh6.    0us+:        0:120:R   + [000]      21:  0:R migration/0
  <idle>-0         0dNh6.   13us : <stack trace>
 => __ftrace_trace_stack
 => probe_wakeup
 => ttwu_do_activate
 => try_to_wake_up
 => wake_up_q
 => cpu_stop_queue_work
 => watchdog_timer_fn
 => __hrtimer_run_queues
 => hrtimer_interrupt
 => __sysvec_apic_timer_interrupt
 => sysvec_apic_timer_interrupt
 => asm_sysvec_apic_timer_interrupt
 => cpuidle_enter_state
 => cpuidle_enter
 => cpuidle_idle_call
 => do_idle
 => cpu_startup_entry
 => rest_init
 => start_kernel
 => x86_64_start_reservations
 => x86_64_start_kernel
 => common_startup_64
  <idle>-0         0dNh6.   13us : 0
  <idle>-0         0d..3.   16us : __schedule
  <idle>-0         0d..3.   17us :        0:120:R ==> [000]      21:  0:R migration/0
  <idle>-0         0d..3.   19us : <stack trace>
 => __ftrace_trace_stack
 => probe_wakeup_sched_switch.part.0
 => __schedule
 => schedule_idle
 => do_idle
 => cpu_startup_entry
 => rest_init
 => start_kernel
 => x86_64_start_reservations
 => x86_64_start_kernel
 => common_startup_64
```
### See available tracers
```
cat /debug/tracing/available_tracers
..
timerlat osnoise hwlat blk function_graph wakeup_dl wakeup_rt wakeup function nop
```
```
echo "" > /debug/tracing/set_ftrace_filter
cat /debug/tracing/set_ftrace_filter
..
#### all functions enabled ####

cat /debug/tracing/trace
..
# tracer: hwlat
#
# entries-in-buffer/entries-written: 55/55   #P:4
#
#                                _-----=> irqs-off/BH-disabled
#                               / _----=> need-resched
#                              | / _---=> hardirq/softirq
#                              || / _--=> preempt-depth
#                              ||| / _-=> migrate-disable
#                              |||| /     delay
#           TASK-PID     CPU#  |||||  TIMESTAMP  FUNCTION
#              | |         |   |||||     |         |
           <...>-4603    [002] d....  5530.226260: #1     inner/outer(us):   13/13    ts:1748106483.610950304 count:2
           <...>-4603    [000] d....  5532.242255: #2     inner/outer(us):   17/10    ts:1748106486.059681953 count:1
           <...>-4603    [000] d....  5536.274311: #3     inner/outer(us):   11/10    ts:1748106490.065228713 count:1
           <...>-4603    [003] d....  5539.298336: #4     inner/outer(us):   13/26    ts:1748106492.809430691 count:10
           <...>-4603    [000] d....  5548.370464: #5     inner/outer(us):   17/9     ts:1748106502.059683554 count:1
           <...>-4603    [001] d....  5549.378468: #6     inner/outer(us):   36/15    ts:1748106503.214885660 count:33
           <...>-4603    [000] dn...  5552.402487: #7     inner/outer(us):   12/10    ts:1748106506.059724147 count:2
           <...>-4603    [002] d....  5554.418519: #8     inner/outer(us):   12/12    ts:1748106508.135728165 count:4
           <...>-4603    [003] d....  5555.426537: #9     inner/outer(us):   10/14    ts:1748106509.261875907 count:1
           <...>-4603    [000] d....  5556.434544: #10    inner/outer(us):   14/13    ts:1748106510.023729201 count:2 nmi-total:3 nmi-count:1
           <...>-4603    [001] d....  5557.442546: #11    inner/outer(us):    9/14    ts:1748106510.952476714 count:1 nmi-total:2 nmi-count:1
           <...>-4603    [002] d....  5558.450585: #12    inner/outer(us):   13/14    ts:1748106511.931331902 count:11
           <...>-4603    [003] d....  5559.458578: #13    inner/outer(us):   16/26    ts:1748106513.223770215 count:112
           <...>-4603    [000] d....  5560.466586: #14    inner/outer(us):   16/9     ts:1748106514.059683069 count:1
           <...>-4603    [001] d....  5561.474613: #15    inner/outer(us):   10/16    ts:1748106514.984476011 count:3
```
## ltrace
Great! ltrace is a dynamic tracing tool for Linux that intercepts and records dynamic library calls made by a program, along with the arguments passed and return values.

It's similar to strace, but instead of focusing on system calls , ltrace focuses on library function calls (like those from libc, libm, or any shared libraries used by the program).

Useful for:
- Reverse engineering
- Debugging crashes
- Understanding how a binary works
```
ltrace ls
..
strrchr("ls", '/')                                                        = nil
setlocale(LC_ALL, "")                                                     = "C.UTF-8"
bindtextdomain("coreutils", "/usr/share/locale")                          = "/usr/share/locale"
textdomain("coreutils")                                                   = "coreutils"
__cxa_atexit(0x556c51e25b10, 0, 0x556c51e3af80, 0)                        = 0
isatty(1)                                                                 = 1
getenv("QUOTING_STYLE")                                                   = nil
getenv("COLUMNS")                                                         = nil
ioctl(1, 21523, 0x7fff1c11d6d0)                                           = 0
getenv("TABSIZE")                                                         = nil
getopt_long(1, 0x7fff1c11d838, "abcdfghiklmnopqrstuvw:xABCDFGHI:"..., 0x556c51e3b360, -1) = -1
getenv("LS_BLOCK_SIZE")                                                   = nil
getenv("BLOCK_SIZE")                                                      = nil
getenv("BLOCKSIZE")                                                       = nil
getenv("POSIXLY_CORRECT")                                                 = nil
getenv("BLOCK_SIZE")                                                      = nil
__errno_location()                                                        = 0x7f7d072cfae0
malloc(56)                                                                = 0x556c5bac2bb0
__errno_location()                                                        = 0x7f7d072cfae0
malloc(56)                                                                = 0x556c5bac2bf0
getenv("TZ")                                                              = nil
malloc(128)                                                               = 0x556c5bac2c30
malloc(20000)                                                             = 0x556c5bac2cc0
malloc(32)                                                                = 0x556c5bac7af0
strlen(".")                                                               = 1
malloc(2)                                                                 = 0x556c5bac7b20
memcpy(0x556c5bac7b20, ".\0", 2)                                          = 0x556c5bac7b20
__errno_location()                                                        = 0x7f7d072cfae0
opendir(".")                                                              = { 3 }
readdir({ 3 })                                                            = { 9571630, "nginx" }
__errno_location()                                                        = 0x7f7d072cfae0
__ctype_get_mb_cur_max()                                                  = 6
strlen("nginx")                                                           = 5
strlen("nginx")                                                           = 5
malloc(6)                                                                 = 0x556c5bacfb80
memcpy(0x556c5bacfb80, "nginx\0", 6)                                      = 0x556c5bacfb80
readdir({ 3 })                                                            = { 9571672, "perf.data.old" }
__errno_location()                                                        = 0x7f7d072cfae0
__ctype_get_mb_cur_max()                                                  = 6
strlen("perf.data.old")                                                   = 13
strlen("perf.data.old")                                                   = 13
malloc(14)                                                                = 0x556c5bacfba0
memcpy(0x556c5bacfba0, "perf.data.old\0", 14)                             = 0x556c5bacfba0
readdir({ 3 })                                                            = { 9568262, "node_exporter-1.9.1.linux-amd64" }
```
You can trace specific function names, specific pids, apply specific filters etc...
### Follow forked process and print timestamps
```
ltrace -tt -f ping google.com
..
[pid 4829] 20:38:34.695151 strncpy(0x7ffe33333e10, "google.com", 1024)    = 0x7ffe33333e10
[pid 4829] 20:38:34.695290 socket(2, 2, 0)                                = 5
[pid 4829] 20:38:34.695429 connect(5, 0x7ffe33333dd0, 16, 0x7f3f5bd0f6cb) = 0
[pid 4829] 20:38:34.695571 getsockname(5, 0x7ffe3333662c, 0x7ffe33333db4, 0x7f3f5bd0f087) = 0
[pid 4829] 20:38:34.695712 close(5)                                       = 0
[pid 4829] 20:38:34.695835 setsockopt(3, 0, 11, 0x7ffe33333db4)           = 0
```
### Count how often functions are called (also sumarizes time spent)
```
ltrace -c ls
..
% time     seconds  usecs/call     calls      function
------ ----------- ----------- --------- --------------------
 17.69    0.002681          40        66 strlen
 16.33    0.002475          38        65 __ctype_get_mb_cur_max
 12.33    0.001869          38        49 __errno_location
  9.38    0.001422          41        34 __overflow
  8.25    0.001250          37        33 strcoll
  7.99    0.001211        1211         1 setlocale
  5.30    0.000804          38        21 malloc
  4.22    0.000640          40        16 readdir
  4.18    0.000633          37        17 memcpy
```
# Basic tools
Method USE - Utilization, Saturation, Errors
## uptime
```
$ uptime
..
03:16:59 up 17 days, 4:18, 1 user, load average: 2.74, 2.54, 2.58
```
## dmesg | tail
```
dmesg | tail
..
[1880957.563150] perl invoked oom-killer: gfp_mask=0x280da, order=0, oom_score_adj=0
[...]
[1880957.563400] Out of memory: Kill process 18694 (perl) score 246 or sacrifice child
[1880957.563408] Killed process 18694 (perl) total-vm:1972392kB, anon-rss:1953348kB,
file-rss:0kB
[2320864.954447] TCP: Possible SYN flooding on port 7001. Dropping request. Check
SNMP counters.
```
## vmstat 1
```
$ vmstat 1
..
procs ---------memory---------- ---swap-- -----io---- -system-- ------cpu-----
r b swpd free buff cache si so bi bo in cs us sy id wa st
34 0 0 200889792 73708 591828 0 0 0 5 6 10 96 1 3 0 0
32 0 0 200889920 73708 591860 0 0 0 592 13284 4282 98 1 1 0 0
32 0 0 200890112 73708 591860 0 0 0 0 9501 2154 99 1 0 0 0
[...]
```
## mpstat -P ALL 1
```
$ mpstat -P ALL 1
[...]
03:16:41 AM CPU %usr %nice %sys %iowait %irq %soft %steal %guest %gnice %idle
03:16:42 AM all 14.27 0.00 0.75 0.44 0.00 0.00 0.06 0.00 0.00 84.48
03:16:42 AM 0 100.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00
03:16:42 AM 1 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 100.00
03:16:42 AM 2 8.08 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 91.92
03:16:42 AM 3 10.00 0.00 1.00 0.00 0.00 0.00 1.00 0.00 0.00 88.00
03:16:42 AM 4 1.01 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 98.99
03:16:42 AM 5 5.10 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 94.90
03:16:42 AM 6 11.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 89.00
03:16:42 AM 7 10.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 90.00
[...]
```
## pidstat 1
```
$ pidstat 1
Linux 4.13.0-19-generic (...) 08/04/2018 _x86_64_ (16 CPU)
03:20:47 AM UID PID %usr %system %guest %CPU CPU Command
03:20:48 AM 0 1307 0.00 0.98 0.00 0.98 8 irqbalance
03:20:48 AM 33 12178 4.90 0.00 0.00 4.90 4 java
03:20:48 AM 33 12569 476.47 24.51 0.00 500.98 0 java
03:20:48 AM 0 130249 0.98 0.98 0.00 1.96 1 pidstat
03:20:48 AM UID PID %usr %system %guest %CPU CPU Command
03:20:49 AM 33 12178 4.00 0.00 0.00 4.00 4 java
03:20:49 AM 33 12569 331.00 21.00 0.00 352.00 0 java
03:20:49 AM 0 129906 1.00 0.00 0.00 1.00 8 sshd
03:20:49 AM 0 130249 1.00 1.00 0.00 2.00 1 pidstat
03:20:49 AM UID PID %usr %system %guest %CPU CPU Command
03:20:50 AM 33 12178 4.00 0.00 0.00 4.00 4 java
03:20:50 AM 113 12356 1.00 0.00 0.00 1.00 11 snmp-pass
03:20:50 AM 33 12569 210.00 13.00 0.00 223.00 0 java
03:20:50 AM 0 130249 1.00 0.00 0.00 1.00 1 pidstat
[...]
```
## iostat -xz 1
```
$ iostat -xz 1
Linux 4.13.0-19-generic (...) 08/04/2018 _x86_64_ (16 CPU)
[...]
avg-cpu: %user %nice %system %iowait %steal %idle
22.90 0.00 0.82 0.63 0.06 75.59
Device: rrqm/s wrqm/s r/s w/s rkB/s wkB/s avgrq-sz avgqu-sz
await r_await w_await svctm %util
nvme0n1 0.00 1167.00 0.00 1220.00 0.00 151293.00 248.02 2.10
1.72 0.00 1.72 0.21 26.00
nvme1n1 0.00 1164.00 0.00 1219.00 0.00 151384.00 248.37 0.90
0.74 0.00 0.74 0.19 23.60
md0 0.00 0.00 0.00 4770.00 0.00 303113.00 127.09 .00
0.00 0.00 0.00 0.00 0.00
[...]
```
## free -wm
```
$ free -m
total used free shared buff/cache available
Mem: 122872 39158 3107 1166 80607 81214
Swap: 0 0 0
```
## vfsstat
```
# vfsstat
..
TIME READ/s WRITE/s CREATE/s OPEN/s FSYNC/s
18:35:32: 231 12 4 98 0
18:35:33: 274 13 4 106 0
18:35:34: 586 86 4 251 0
18:35:35: 241 15 4 99 0
18:35:36: 232 10 4 98 0
[...]

bpftrace -e 'kprobe:vfs_read { @[comm] = count(); }'
..
Attaching 1 probe...
^C
@[rtkit-daemon]: 1
[...]
@[gnome-shell]: 207
@[Chrome_IOThread]: 222
@[chrome]: 225
@[InputThread]: 302
@[gdbus]: 819
@[Web Content]: 1725
```
## sar -n DEV 1
```
$ sar -n DEV 1
Linux 4.13.0-19-generic (...) 08/04/2018 _x86_64_ (16 CPU)
03:38:28 AM IFACE rxpck/s txpck/s rxkB/s txkB/s rxcmp/s txcmp/s
rxmcst/s %ifutil
03:38:29 AM eth0 7770.00 4444.00 10720.12 5574.74 0.00 0.00
0.00 0.00
03:38:29 AM lo 24.00 24.00 19.63 19.63 0.00 0.00
0.00 0.00
03:38:29 AM IFACE rxpck/s txpck/s rxkB/s txkB/s rxcmp/s txcmp/s
rxmcst/s %ifutil
03:38:30 AM eth0 5579.00 2175.00 7829.20 2626.93 0.00 0.00
0.00 0.00
03:38:30 AM lo 33.00 33.00 1.79 1.79 0.00 0.00
0.00 0.00
[...]
```
## sar -n TCP,ETCP 1
```
# sar -n TCP,ETCP 1
Linux 4.13.0-19-generic (...) 08/04/2019 _x86_64_ (16 CPU)
03:41:01 AM active/s passive/s iseg/s oseg/s
03:41:02 AM 1.00 1.00 348.00 1626.00
03:41:01 AM atmptf/s estres/s retrans/s isegerr/s orsts/s
03:41:02 AM 0.00 0.00 1.00 0.00 0.00
03:41:02 AM active/s passive/s iseg/s oseg/s
03:41:03 AM 0.00 0.00 521.00 2660.00
03:41:02 AM atmptf/s estres/s retrans/s isegerr/s orsts/s
03:41:03 AM 0.00 0.00 0.00 0.00 0.00
[...]
```
## top
```
top - 03:44:14 up 17 days, 4:46, 1 user, load average: 2.32, 2.20, 2.21
Tasks: 474 total, 1 running, 473 sleeping, 0 stopped, 0 zombie
%Cpu(s): 29.7 us, 0.4 sy, 0.0 ni, 69.7 id, 0.1 wa, 0.0 hi, 0.0 si, 0.0 st
KiB Mem : 12582137+total, 3159704 free, 40109716 used, 82551960 buff/cache
KiB Swap: 0 total, 0 free, 0 used. 83151728 avail Mem
PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND
12569 www 20 0 2.495t 0.051t 0.018t S 484.7 43.3 13276:02 java
12178 www 20 0 12.214g 3.107g 16540 S 4.9 2.6 553:41 java
125312 root 20 0 0 0 0 S 1.0 0.0 0:13.20 kworker/u256:0
128697 root 20 0 0 0 0 S 0.3 0.0 0:02.10 kworker/10:2
[...]
```
