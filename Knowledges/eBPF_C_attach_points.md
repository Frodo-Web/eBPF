## Attach points
| Section Type                  | Description                        | Example Usage                                  |
|-------------------------------|------------------------------------|------------------------------------------------|
| `kprobe/function_name`        | Kernel function entry              | `SEC("kprobe/sys_open")`                       |
| `kretprobe/function_name`     | Kernel function return             | `SEC("kretprobe/vfs_read")`                    |
| `uprobe/[path]:symbol`        | User-space function entry          | `SEC("uprobe//lib/x86_64-linux-gnu/libc.so.6:malloc")` |
| `uretprobe/[path]:symbol`     | User-space function return         | `SEC("uretprobe//usr/bin/myapp:my_function")`  |
| `tracepoint/category/event`   | Tracepoint event                   | `SEC("tracepoint/syscalls/sys_enter_execve")`  |
| `perf_event`                  | Perf event trigger                 | `SEC("perf_event")`                            |
| `xdp`                         | XDP hook on network interface      | `SEC("xdp")`                                   |
| `classifier`                  | TC classifier                      | `SEC("classifier")`                            |
| `lsm/file_mmap`               | LSM hooks                           | `SEC("lsm/file_mmap")`                          |
## Formats
By shared library name and its function
```
SEC("uprobe/libc.so.6:malloc")
```
By full path to bin and its function
```
SEC("uprobe/[PATH/TO/LIBRARY]:FUNCTION_NAME")
SEC("uprobe//lib/x86_64-linux-gnu/libc.so.6:malloc")
```
By full path and offset
```
SEC("uprobe/[PATH/TO/LIBRARY]+0xOFFSET")
SEC("uprobe//lib/x86_64-linux-gnu/libc.so.6+0x3f120") // malloc@plt or similar
```
