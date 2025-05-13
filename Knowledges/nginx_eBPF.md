# nginx eBPF
Nginx binary is builded statically, with_debug.
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
