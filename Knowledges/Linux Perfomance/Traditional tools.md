# Traditional tools
## perf
perf is a powerful profiling tool built into the Linux kernel that allows you to analyze system and application performance using hardware and software counters.

- Monitor CPU cycles, cache misses, branch predictions
- Profile functions in user or kernel space
- Sample call graphs (stack traces)
- Trace events and system behavior
```
perf record -g ./my_program
ls perf.data
perf report
..
```
![image](https://github.com/user-attachments/assets/7b4938c1-87e2-4ee2-8c7c-32c1878f5bd4)
