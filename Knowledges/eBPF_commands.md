# eBPF commands
```
/sys/kernel/debug/tracing/trace_pipe

file hello.bpf.o
hello.bpf.o: ELF 64-bit LSB relocatable, eBPF, version 1 (SYSV), with debug_info,
not stripped

llvm-objdump -S hello.bpf.o

Disassembly of section xdp:
0000000000000000 <hello>:
; bpf_printk("Hello World %d", counter");
0: 18 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 r6 = 0 ll
2: 61 63 00 00 00 00 00 00 r3 = *(u32 *)(r6 + 0)
3: 18 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 r1 = 0 ll
5: b7 02 00 00 0f 00 00 00 r2 = 15
6: 85 00 00 00 06 00 00 00 call 6
; counter++;
7: 61 61 00 00 00 00 00 00 r1 = *(u32 *)(r6 + 0)
8: 07 01 00 00 01 00 00 00 r1 += 1
9: 63 16 00 00 00 00 00 00 *(u32 *)(r6 + 0) = r1
; return XDP_PASS;
10: b7 00 00 00 02 00 00 00 r0 = 2
11: 95 00 00 00 00 00 00 00 exit

bpftool prog load hello.bpf.o /sys/fs/bpf/hello

ls /sys/fs/bpf
..
hello

bpftool prog list
...
540: xdp name hello tag d35b94b4c0c10efb gpl
loaded_at 2022-08-02T17:39:47+0000 uid 0
xlated 96B jited 148B memlock 4096B map_ids 165,166
btf_id 254

bpftool prog show id 540 --pretty
{
"id": 540,
"type": "xdp",
"name": "hello",
"tag": "d35b94b4c0c10efb",
"gpl_compatible": true,
"loaded_at": 1659461987,
"uid": 0,
"bytes_xlated": 96,
"jited": true,
"bytes_jited": 148,
"bytes_memlock": 4096,
"map_ids": [165,166
],
"btf_id": 254
}

• bpftool prog show id 540
• bpftool prog show name hello
• bpftool prog show tag d35b94b4c0c10efb
• bpftool prog show pinned /sys/fs/bpf/hello

bpftool prog dump xlated name hello
..
int hello(struct xdp_md * ctx):
; bpf_printk("Hello World %d", counter);
0: (18) r6 = map[id:165][0]+0
2: (61) r3 = *(u32 *)(r6 +0)
3: (18) r1 = map[id:166][0]+0
5: (b7) r2 = 15
6: (85) call bpf_trace_printk#-78032
; counter++;
7: (61) r1 = *(u32 *)(r6 +0)
8: (07) r1 += 1
9: (63) *(u32 *)(r6 +0) = r1
; return XDP_PASS;
10: (b7) r0 = 2
11: (95) exit


bpftool prog dump jited name hello
..
int hello(struct xdp_md * ctx):
bpf_prog_d35b94b4c0c10efb_hello:
; bpf_printk("Hello World %d", counter);
0: hint #34
4: stp x29, x30, [sp, #-16]!
8: mov x29, sp
c: stp x19, x20, [sp, #-16]!
10: stp x21, x22, [sp, #-16]!
14: stp x25, x26, [sp, #-16]!
18: mov x25, sp
1c: mov x26, #0
20: hint #36
24: sub sp, sp, #0
28: mov x19, #-140733193388033
2c: movk x19, #2190, lsl #16
30: movk x19, #49152
34: mov x10, #0
38: ldr w2, [x19, x10]
3c: mov x0, #-205419695833089
40: movk x0, #709, lsl #16
44: movk x0, #5904
48: mov x1, #15
4c: mov x10, #-6992
50: movk x10, #29844, lsl #16
54: movk x10, #56832, lsl #32
58: blr x10
5c: add x7, x0, #0
; counter++;
60: mov x10, #0
64: ldr w0, [x19, x10]
68: add x0, x0, #1
6c: mov x10, #0
70: str w0, [x19, x10]
; return XDP_PASS;
74: mov x7, #2
78: mov sp, sp
7c: ldp x25, x26, [sp], #16
80: ldp x21, x22, [sp], #16
84: ldp x19, x20, [sp], #16
88: ldp x29, x30, [sp], #16
8c: add x0, x7, #0
90: ret

bpftool net attach xdp id 540 dev eth0

bpftool net list
..
xdp:
eth0(2) driver id 540
tc:
flow_dissector:

ip link
..
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT
group default qlen 1000
...
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 xdp qdisc fq_codel state UP
mode DEFAULT group default qlen 1000
...
prog/xdp id 540 tag 9d0e949f89f1a82c jited
...

bpftool map list
..
165: array name hello.bss flags 0x400
6 Here, bss stands for “block started by symbol.”
key 4B value 4B max_entries 1 memlock 4096B
btf_id 254

166: array name hello.rodata flags 0x80
key 4B value 15B max_entries 1 memlock 4096B
btf_id 254 frozen

bpftool map dump name hello.bss
..
[{
"value": {
".bss": [{
"counter": 11127
}
]
}
}

bpftool map dump name hello.rodata
..
[{
"value": {
".rodata": [{
"hello.____fmt": "Hello World %d"
}
]
}
}
]
]

bpftool net detach xdp dev eth0

bpftool net list
..
xdp:
tc:
flow_dissector:

bpftool prog show name hello
..
395: xdp name hello tag 9d0e949f89f1a82c gpl
loaded_at 2022-12-19T18:20:32+0000 uid 0
xlated 48B jited 108B memlock 4096B map_ids 4

rm /sys/fs/bpf/hello
bpftool prog show name hello

bpftool prog load hello-func.bpf.o /sys/fs/bpf/hello
bpftool prog list name hello
..
893: raw_tracepoint name hello tag 3d9eb0c23d4ab186 gpl
loaded_at 2023-01-05T18:57:31+0000 uid 0
xlated 80B jited 208B memlock 4096B map_ids 204
btf_id 30

bpftool prog dump xlated name hello
..
int hello(struct bpf_raw_tracepoint_args * ctx):
; int opcode = get_opcode(ctx);
0: (85) call pc+7#bpf_prog_cbacc90865b1b9a5_get_opcode
; bpf_printk("Syscall: %d", opcode);
1: (18) r1 = map[id:193][0]+0
3: (b7) r2 = 12
4: (bf) r3 = r0
5: (85) call bpf_trace_printk#-73584
; return 0;
6: (b7) r0 = 0
7: (95) exit
int get_opcode(struct bpf_raw_tracepoint_args * ctx):
; return ctx->args[1];
8: (79) r0 = *(u64 *)(r1 +8)
; return ctx->args[1];
9: (95) exit


bpftool prog list
...
120: raw_tracepoint name hello tag b6bfd0e76e7f9aac gpl
loaded_at 2023-01-05T14:35:32+0000 uid 0
xlated 160B jited 272B memlock 4096B map_ids 29
btf_id 124
pids hello-tail.py(3590)
121: raw_tracepoint name ignore_opcode tag a04f5eef06a7f555 gpl
loaded_at 2023-01-05T14:35:32+0000 uid 0
xlated 16B jited 72B memlock 4096B
btf_id 124
pids hello-tail.py(3590)
122: raw_tracepoint name hello_exec tag 931f578bd09da154 gpl
loaded_at 2023-01-05T14:35:32+0000 uid 0
xlated 112B jited 168B memlock 4096B
btf_id 124
pids hello-tail.py(3590)
123: raw_tracepoint name hello_timer tag 6c3378ebb7d3a617 gpl
loaded_at 2023-01-05T14:35:32+0000 uid 0
xlated 336B jited 356B memlock 4096B
btf_id 124
pids hello-tail.py(3590)

strace -e bpf ./hello-buffer-config.py
..
bpf(BPF_BTF_LOAD, ...) = 3
bpf(BPF_MAP_CREATE, {map_type=BPF_MAP_TYPE_PERF_EVENT_ARRAY…) = 4
bpf(BPF_MAP_CREATE, {map_type=BPF_MAP_TYPE_HASH...) = 5
bpf(BPF_PROG_LOAD, {prog_type=BPF_PROG_TYPE_KPROBE,...prog_name="hello",...) = 6
bpf(BPF_MAP_UPDATE_ELEM, ...}
...

bpftool btf list
..
1: name [vmlinux] size 5843164B
2: name [aes_ce_cipher] size 407B
3: name [cryptd] size 3372B
...
149: name <anon> size 4372B prog_ids 319 map_ids 103
pids hello-buffer-co(7660)
155: name <anon> size 37100B

bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h
bpftool gen skeleton hello-buffer-config.bpf.o > hello-buffer-config.skel.h
pids bpftool(7784)

BPF TRACE

# список всего что можно трассировать
sudo bpftrace -l | less

# список системных вызовов
sudo bpftrace -l 'tracepoint:syscalls:sys_enter_*'

Tracepoint - kernel static tracing. Kprobes - dynamic. Tracepoints have stable API

# Например, можно в реальном времени наблюдать, какие файлы открываются какими процессами:
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_open,
  tracepoint:syscalls:sys_enter_openat {
    printf("%s %s\n", comm, str(args->filename));
  }'

str() turns a pointer into the string it points to.

# Определить членов структуры args для трейспоинта (структура авт генерируется исходя из tracepoint информации для bpftrace)
bpftrace -vl tracepoint:syscalls:sys_enter_openat
..                                          
tracepoint:syscalls:sys_enter_openat                                                                                        
int __syscall_nr                                                                                                        
int dfd                                                                                                                 
const char * filename                                                                                                   
int flags                                                                                                               
umode_t mode 

bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'
Attaching 1 probe...
^C

@[bpftrace]: 6
@[systemd]: 24
@[snmp-pass]: 96
@[sshd]: 125

bpftrace -e 'tracepoint:syscalls:sys_exit_read /pid == 18644/ { @bytes = hist(args.ret); }'
Attaching 1 probe...
^C

@bytes:
[0, 1]                12 |@@@@@@@@@@@@@@@@@@@@                                |
[2, 4)                18 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                     |
[4, 8)                 0 |                                                    |
[8, 16)                0 |                                                    |
[16, 32)               0 |                                                    |
[32, 64)              30 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[64, 128)             19 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                    |
[128, 256)             1 |@

/.../: This is a filter (aka predicate), which acts as a filter for the action. The action is only executed if the filtered expression is true, in this case, only for the process ID 18644. Boolean operators are supported ("&&", "||").
ret: This is the return value of the function. For sys_read(), this is either -1 (error) or the number of bytes successfully read.'
Other map functions include lhist() (linear hist), count(), sum(), avg(), min(), and max().

bpftrace -e 'tracepoint:syscalls:sys_exit_read { @bytes = avg(args.ret); }'

# ret - количество прочитанный байтов которые вернул syscall при успешном выполнении
bpftrace -vl tracepoint:syscalls:sys_exit_read
..                                             
tracepoint:syscalls:sys_exit_read                                                                                           
int __syscall_nr                                                                                                        
long ret 

bpftrace -e 'kretprobe:vfs_read { @bytes = lhist(retval, 0, 2000, 200); }'
Attaching 1 probe...
^C

@bytes:
(...,0]                0 |                                                    |
[0, 200)              66 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[200, 400)             2 |@                                                   |
[400, 600)             3 |@@                                                  |
[600, 800)             0 |                                                    |
[800, 1000)            5 |@@@                                                 |
[1000, 1200)           0 |                                                    |
[1200, 1400)           0 |                                                    |
[1400, 1600)           0 |                                                    |
[1600, 1800)           0 |                                                    |
[1800, 2000)           0 |                                                    |
[2000,...)            39 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      |

Summarize read() bytes as a linear histogram, and traced using kernel dynamic tracing.

    It begins with the probe kretprobe:vfs_read: this is the kretprobe probe type (kernel dynamic tracing of function returns) instrumenting the vfs_read() kernel function. There is also the kprobe probe type (shown in the next lesson), to instrument when functions begin execution (are entered). These are powerful probe types, letting you trace tens of thousands of different kernel functions. However, these are "unstable" probe types: since they can trace any kernel function, there is no guarantee that your kprobe/kretprobe will work between kernel versions, as the function names, arguments, return values, and roles may change. Also, since it is tracing the raw kernel, you'll need to browse the kernel source to understand what these probes, arguments, and return values, mean.

    lhist(): this is a linear histogram, where the arguments are: value, min, max, step. The first argument (retval) of vfs_read() is the return value: the number of bytes read.

# bpftrace -e 'kprobe:vfs_read { @start[tid] = nsecs; } kretprobe:vfs_read /@start[tid]/ { @ns[comm] = hist(nsecs - @start[tid]); delete(@start, tid); }'
Attaching 2 probes...

[...]
@ns[snmp-pass]:
[0, 1]                 0 |                                                    |
[2, 4)                 0 |                                                    |
[4, 8)                 0 |                                                    |
[8, 16)                0 |                                                    |
[16, 32)               0 |                                                    |
[32, 64)               0 |                                                    |
[64, 128)              0 |                                                    |
[128, 256)             0 |                                                    |
[256, 512)            27 |@@@@@@@@@                                           |
[512, 1k)            125 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       |
[1k, 2k)              22 |@@@@@@@                                             |
[2k, 4k)               1 |                                                    |
[4k, 8k)              10 |@@@                                                 |
[8k, 16k)              1 |                                                    |
[16k, 32k)             3 |@                                                   |
[32k, 64k)           144 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[64k, 128k)            7 |@@                                                  |
[128k, 256k)          28 |@@@@@@@@@@                                          |
[256k, 512k)           2 |                                                    |
[512k, 1M)             3 |@                                                   |
[1M, 2M)               1 |                                                    |

Summarize the time spent in read(), in nanoseconds, as a histogram, by process name.

    @start[tid]: This uses the thread ID as a key. There may be many reads in-flight, and we want to store a start timestamp to each. How? We could construct a unique identifier for each read, and use that as the key. But because kernel threads can only be executing one syscall at a time, we can use the thread ID as the unique identifier, as each thread cannot be executing more than one.

    nsecs: Nanoseconds since boot. This is a high resolution timestamp counter than can be used to time events.

    /@start[tid]/: This filter checks that the start time was seen and recorded. Without this filter, this program may be launched during a read and only catch the end, resulting in a time calculation of now - zero, instead of now - start.

    delete(@start, tid): this frees the variable.

bpftrace -e 'tracepoint:sched:sched* { @[probe] = count(); } interval:s:5 { exit(); }'
Attaching 25 probes...
@[tracepoint:sched:sched_wakeup_new]: 1
@[tracepoint:sched:sched_process_fork]: 1
@[tracepoint:sched:sched_process_exec]: 1
@[tracepoint:sched:sched_process_exit]: 1
@[tracepoint:sched:sched_process_free]: 2
@[tracepoint:sched:sched_process_wait]: 7
@[tracepoint:sched:sched_wake_idle_without_ipi]: 53
@[tracepoint:sched:sched_stat_runtime]: 212
@[tracepoint:sched:sched_wakeup]: 253
@[tracepoint:sched:sched_waking]: 253
@[tracepoint:sched:sched_switch]: 510

Count process-level events for five seconds, printing a summary.

    sched: The sched probe category has high-level scheduler and process events, such as fork, exec, and context switch.
    probe: The full name of the probe.
    interval:s:5: This is a probe that fires once every 5 seconds, on one CPU only. It is used for creating script-level intervals or timeouts.
    exit(): This exits bpftrace.

bpftrace -e 'profile:hz:99 { @[kstack] = count(); }'
..
Attaching 1 probe...
^C

[...]
@[
filemap_map_pages+181
__handle_mm_fault+2905
handle_mm_fault+250
__do_page_fault+599
async_page_fault+69
]: 12
[...]
@[
cpuidle_enter_state+164
do_idle+390
cpu_startup_entry+111
start_secondary+423
secondary_startup_64+165
]: 22122

    profile:hz:99: This fires on all CPUs at 99 Hertz. Why 99 and not 100 or 1000? We want frequent enough to catch both the big and small picture of execution, but not too frequent as to perturb performance. 100 Hertz is enough. But we don't want 100 exactly, as sampling may occur in lockstep with other timed activities, hence 99.
    kstack: Returns the kernel stack trace. This is used as a key for the map, so that it can be frequency counted. The output of this is ideal to be visualized as a flame graph. There is also ustack for the user-level stack trace.

bpftrace -e 'profile:hz:99 { @[ustack] = count(); }'

bpftrace -e 'tracepoint:sched:sched_switch { @[kstack] = count(); }'
^C
[...]

@[
__schedule+697
__schedule+697
schedule+50
schedule_timeout+365
xfsaild+274
kthread+248
ret_from_fork+53
]: 73
@[
__schedule+697
__schedule+697
schedule_idle+40
do_idle+356
cpu_startup_entry+111
start_secondary+423
secondary_startup_64+165
]: 305

This counts stack traces that led to context switching (off-CPU) events. The above output has been truncated to show the last two only.

    sched: The sched category has tracepoints for different kernel CPU scheduler events: sched_switch, sched_wakeup, sched_migrate_task, etc.
    sched_switch: This probe fires when a thread leaves CPU. This will be a blocking event: eg, waiting on I/O, a timer, paging/swapping, or a lock.
    kstack: A kernel stack trace.
    sched_switch fires in thread context, so that the stack refers to the thread who is leaving. As you use other probe types, pay attention to context, as comm, pid, kstack, etc, may not refer to the target of the probe.

bpftrace -e 'tracepoint:block:block_rq_issue { @ = hist(args.bytes); }'
Attaching 1 probe...
^C

@:
[0, 1]                 1 |@@                                                  |
[2, 4)                 0 |                                                    |
[4, 8)                 0 |                                                    |
[8, 16)                0 |                                                    |
[16, 32)               0 |                                                    |
[32, 64)               0 |                                                    |
[64, 128)              0 |                                                    |
[128, 256)             0 |                                                    |
[256, 512)             0 |                                                    |
[512, 1K)              0 |                                                    |
[1K, 2K)               0 |                                                    |
[2K, 4K)               0 |                                                    |
[4K, 8K)              24 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[8K, 16K)              2 |@@@@                                                |
[16K, 32K)             6 |@@@@@@@@@@@@@                                       |
[32K, 64K)             5 |@@@@@@@@@@                                          |
[64K, 128K)            0 |                                                    |
[128K, 256K)           1 |@@                                                  |

Block I/O requests by size in bytes, as a histogram.

    tracepoint:block: The block category of tracepoints traces various block I/O (storage) events.
    block_rq_issue: This fires when an I/O is issued to the device.
    args.bytes: This is a member from the tracepoint block_rq_issue arguments which shows the size in bytes.

The context of this probe is important: this fires when the I/O is issued to the device. This often happens in process context, where builtins like comm will show you the process name, but it can also happen from kernel context (eg, readahead) when the pid and comm will not show the application you expect.


# cat path.bt
#ifndef BPFTRACE_HAVE_BTF
#include <linux/path.h>
#include <linux/dcache.h>
#endif

kprobe:vfs_open
{
	printf("open path: %s\n", str(((struct path *)arg0)->dentry->d_name.name));
}

# bpftrace path.bt
Attaching 1 probe...
open path: dev
open path: if_inet6
open path: retrans_time_ms
[...]

UPROBE EXAMPLES

bpftrace -p 62684 -l | grep 'uprobe:' | wc -l                                                                                                                                                          bpftrace -l 'uprobe:/usr/bin/postgres:*'
bpftrace -l 'uretprobe:/usr/bin/postgres:*' | wc -l 
bpftrace -l 'usdt:/proc/<PID>/exe:*

bpftrace -e 'uretprobe:/usr/bin/postgres:  pg_walfile_name { printf("%d %s %d\n", pid, comm, retval); }'                                                                                                           Attaching 1 probe...                                                                                                   
62956 postmaster 2090227688 

postgres=# SELECT pg_walfile_name(pg_current_wal_lsn());                                                                     
pg_walfile_name                                                                                                    
--------------------------                                                                                               
000000010000000000000001

usdt:/proc/1234/exe:hotspot:gc__start
{
    printf("GC started at %d\n", nsecs);
}

usdt:/proc/1234/exe:hotspot:gc__end
{
    printf("GC ended at %d\n", nsecs);
}

bpftrace gc.bt

Attempts to find USDT directly in binaries

objdump -T /usr/lib/jvm/java-21-openjdk-21.0.7.0.6-1.el9.x86_64/bin/java 
..                                                                                                                                          
/usr/lib/jvm/java-21-openjdk-21.0.7.0.6-1.el9.x86_64/bin/java:     file format elf64-x86-64                                                                                                                                                     DYNAMIC SYMBOL TABLE:                                                                                                   
0000000000000000      DF *UND*  0000000000000000  GLIBC_2.2.5 getenv                                                   
0000000000000000      DF *UND*  0000000000000000  GLIBC_2.34  __libc_start_main                                        
0000000000000000  w   D  *UND*  0000000000000000              _ITM_deregisterTMCloneTable                             
0000000000000000      DF *UND*  0000000000000000              JLI_Launch                                              
0000000000000000      DF *UND*  0000000000000000              JLI_StringDup                                          
0000000000000000      DF *UND*  0000000000000000              JLI_List_add                                          
0000000000000000  w   D  *UND*  0000000000000000              __gmon_start__                                        
0000000000000000      DF *UND*  0000000000000000              JLI_PreprocessArg                                     
0000000000000000      DF *UND*  0000000000000000              JLI_InitArgProcessing                                 
0000000000000000      DF *UND*  0000000000000000              JLI_List_new                                          
0000000000000000      DF *UND*  0000000000000000              JLI_MemFree                                          
0000000000000000      DF *UND*  0000000000000000              JLI_ReportMessage                                  
0000000000000000      DF *UND*  0000000000000000              JLI_AddArgsFromEnvVar                             
0000000000000000  w   D  *UND*  0000000000000000              _ITM_registerTMCloneTable                        
0000000000000000  w   DF *UND*  0000000000000000  GLIBC_2.2.5 __cxa_finalize


Attempts to find Uprobes directly in binaries

nm -D /usr/lib/jvm/java-21-openjdk-21.0.7.0.6-1.el9.x86_64/bin/java
..                                         
w __cxa_finalize@GLIBC_2.2.5                                                                                            
U getenv@GLIBC_2.2.5                                                                                                    
w __gmon_start__                                                                                                        
w _ITM_deregisterTMCloneTable                                                                                           
w _ITM_registerTMCloneTable                                                                                             
U JLI_AddArgsFromEnvVar                                                                                                 
U JLI_InitArgProcessing                                                                                                 
U JLI_Launch                                                                                                            
U JLI_List_add                                                                                                          
U JLI_List_new                                                                                                          
U JLI_MemFree                                                                                                           
U JLI_PreprocessArg                                                                                                     
U JLI_ReportMessage                                                                                                     
U JLI_StringDup                                                                                                         
U __libc_start_main@GLIBC_2.34 

The nm utility is a command-line tool  in Unix-like systems used to list symbols from object files , executables, shared libraries, or the kernel. It stands for "name list ".
Given a compiled binary (like an executable, .so, or .o file), nm reads the symbol table  and prints out each symbol along with: 

    Its address 
    Its type  (function, variable, etc.)
    Its name 

-g Show only global (external) symbols
-u Show only undefined symbols
-D Display dynamic symbols (useful for .so shared libraries)
--demangle  Demangle C++ function names
-C Same as --demangle
-n or --numeric-sort Sort symbols numerically by address
-S Show symbol size
-l Attempt to show line numbers (requires debug info)

T Text (Code) Global function defined in the code section
t Local Text  Static function
D Data (Initialized) Global initialized variable
d Local Data (Initialized) Static initialized variable
B BSS (Uninitialized Data) Global uninitialized variable
b Local BSS Static uninitialized variable
U Undefined External reference (e.g., function from a shared library)
W Weak Symbol May be overridden by other definitions
I Indirect Symbol Used in shared libraries
     
To generate more symbols use -g
gcc -g -o myapp myapp.c
nm myapp


nm -D /bin/ls 
..
U statx@GLIBC_2.28                                                                                                      
U stderr@GLIBC_2.2.5                                                                                                    
U stdout@GLIBC_2.2.5                                                                                                    
U stpncpy@GLIBC_2.2.5                                                                                                   
U strchr@GLIBC_2.2.5                                                                                                    
U strcmp@GLIBC_2.2.5                                                                                                    
U strcoll@GLIBC_2.2.5                                                                                                   
U strcpy@GLIBC_2.2.5                                                                                                    
U strftime@GLIBC_2.2.5                                                                                                  
U strlen@GLIBC_2.2.5                                                                                                    
U strncmp@GLIBC_2.2.5                                                                                                   
U strrchr@GLIBC_2.2.5                                                                                                   
U strtoumax@GLIBC_2.2.5 
...


nm /lib/x86_64-linux-gnu/libc.so.6 | grep ' malloc$'
uprobe:/lib/x86_64-linux-gnu/libc.so.6:malloc

uprobe:/usr/lib/jvm/java-17-openjdk-amd64/bin/java:JVM_DefineClass
{
    printf("Defining class");
}

# Tutorial One liners
https://github.com/bpftrace/bpftrace/blob/master/docs/tutorial_one_liners.md
# EBPF TOOLS
https://github.com/bpftrace/bpftrace/blob/master/tools/README.md

COMPILE JAVA for eBPF tracing

1. Install dependencies packages (Don't forget systemtap-sdt-dev and related for dtrace support)
2. Get java and follow the guide https://github.com/openjdk/jdk21u/blob/master/doc/building.md
git clone https://github.com/openjdk/jdk21u
cd jdk21u
3. Configure it
bash configure --enable-debug --with-jvm-variants=server --enable-dtrace
4. Build the java
make images
5. JDK will be placed here
build/linux-x86_64-server-release/images/jdk

Copy with symbol links dereferenced
cp -R --dereference jdk/* /opt/java24/jdk24u-debug

update-alternatives --install /usr/bin/java java /opt/java24/jdk24u-debug/bin/java 1
sudo update-alternatives --config java

6. Verify USDT probes exist
readelf -n build/linux-x86_64-server-release/images/jdk/bin/java
..
Displaying notes found in: .note.stapsdt
Owner                 Data size	Description
StapSDT               0x00000055	NT_STAPSDT (SystemTap probe descriptors)

7. List the USDT probes
PID=$(pgrep -f java)
sudo bpftrace -l "usdt:/proc/$PID/exe:*"

8. List the uprobes
nm -g build/linux-x86_64-server-release/images/jdk/bin/java | grep JVM_DefineClass

9. Package JDK
cd build/linux-x86_64-server-release/
tar -czvf custom-openjdk21.tar.gz jdk

10. Distribute and install
sudo mkdir -p /opt/custom-jdk21
sudo tar -xzf custom-openjdk21.tar.gz -C /opt/custom-jdk21

export JAVA_HOME=/opt/custom-jdk21/jdk
export PATH=$JAVA_HOME/bin:$PATH
```
