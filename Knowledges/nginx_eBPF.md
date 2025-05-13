# nginx eBPF
Nginx binary is builded statically, with_debug.

Lets check what it has
```
bpftrace -l 'uprobe:/opt/nginx/sbin/nginx:*' | wc -l
..
15809

bpftrace -l 'uretprobe:/opt/nginx/sbin/nginx:*' | wc -l
..
15809

bpftrace -l 'usdt:/opt/nginx/sbin/nginx:*' | wc -l
..
49
```

## Main functions
### ngx_worker_process_init
- This function is called once per worker process at startup.
- It initializes modules and sets up listening sockets.
- Ensures the worker can handle incoming connections.
```
bpftrace -l '*:/opt/nginx/sbin/nginx:*' | grep worker_process_init
..
uprobe:/opt/nginx/sbin/nginx:ngx_worker_process_init
```
