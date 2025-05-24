# Traditional tools
## perf
perf is a powerful profiling tool built into the Linux kernel that allows you to analyze system and application performance using hardware and software counters.

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
