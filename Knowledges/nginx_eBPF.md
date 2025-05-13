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
### Using nm and bpftrace to find symbols
#### nm
```
nm /opt/nginx/sbin/nginx | grep ngx_worker_process_init
..
000000000044faec t ngx_worker_process_init
```
#### bpftrace
```
bpftrace -l '*:/opt/nginx/sbin/nginx:*' | grep worker_process_init
..
uprobe:/opt/nginx/sbin/nginx:ngx_worker_process_init

bpftrace -lv 'uprobe:/opt/nginx/sbin/nginx:ngx_worker_process_init'
..
uprobe:/opt/nginx/sbin/nginx:ngx_worker_process_init
    ngx_cycle_t * cycle
    ngx_int_t worker
```
### Using pahole and gdb to read structures
#### GDB
```
gdb /opt/nginx/sbin/nginx
(gdb) ptype ngx_cycle_t
type = struct ngx_cycle_s {
    void ****conf_ctx;
    ngx_pool_t *pool;
    ngx_log_t *log;
    ngx_log_t new_log;
    ngx_uint_t log_use_stderr;
    ngx_connection_t **files;
    ngx_connection_t *free_connections;
    ngx_uint_t free_connection_n;
    ngx_module_t **modules;
    ngx_uint_t modules_n;
    ngx_uint_t modules_used;
    ngx_queue_t reusable_connections_queue;
    ngx_uint_t reusable_connections_n;
    time_t connections_reuse_time;
    ngx_array_t listening;
    ngx_array_t paths;
    ngx_array_t config_dump;
    ngx_rbtree_t config_dump_rbtree;
    ngx_rbtree_node_t config_dump_sentinel;
    ngx_list_t open_files;
    ngx_list_t shared_memory;
    ngx_uint_t connection_n;
    ngx_uint_t files_n;
    ngx_connection_t *connections;
    ngx_event_t *read_events;
    ngx_event_t *write_events;
    ngx_cycle_t *old_cycle;
    ngx_str_t conf_file;
    ngx_str_t conf_param;
    ngx_str_t conf_prefix;
    ngx_str_t prefix;
    ngx_str_t error_log;
    ngx_str_t lock_file;
    ngx_str_t hostname;
}
```
#### Pahole
```
pahole /opt/nginx/sbin/nginx | less
..
struct ngx_cycle_s {
        void * * * *               conf_ctx;             /*     0     8 */
        ngx_pool_t *               pool;                 /*     8     8 */
        ngx_log_t *                log;                  /*    16     8 */
        ngx_log_t                  new_log;              /*    24    80 */
        /* --- cacheline 1 boundary (64 bytes) was 40 bytes ago --- */
        ngx_uint_t                 log_use_stderr;       /*   104     8 */
        ngx_connection_t * *       files;                /*   112     8 */
        ngx_connection_t *         free_connections;     /*   120     8 */
        /* --- cacheline 2 boundary (128 bytes) --- */
        ngx_uint_t                 free_connection_n;    /*   128     8 */
        ngx_module_t * *           modules;              /*   136     8 */
        ngx_uint_t                 modules_n;            /*   144     8 */
        ngx_uint_t                 modules_used;         /*   152     8 */
        ngx_queue_t                reusable_connections_queue; /*   160    16 */
        ngx_uint_t                 reusable_connections_n; /*   176     8 */
        time_t                     connections_reuse_time; /*   184     8 */
        /* --- cacheline 3 boundary (192 bytes) --- */
        ngx_array_t                listening;            /*   192    40 */
        ngx_array_t                paths;                /*   232    40 */
        /* --- cacheline 4 boundary (256 bytes) was 16 bytes ago --- */
        ngx_array_t                config_dump;          /*   272    40 */
        ngx_rbtree_t               config_dump_rbtree;   /*   312    24 */
        /* --- cacheline 5 boundary (320 bytes) was 16 bytes ago --- */
        ngx_rbtree_node_t          config_dump_sentinel; /*   336    40 */
        ngx_list_t                 open_files;           /*   376    56 */
        /* --- cacheline 6 boundary (384 bytes) was 48 bytes ago --- */
        ngx_list_t                 shared_memory;        /*   432    56 */
        /* --- cacheline 7 boundary (448 bytes) was 40 bytes ago --- */
        ngx_uint_t                 connection_n;         /*   488     8 */
        ngx_uint_t                 files_n;              /*   496     8 */
        ngx_connection_t *         connections;          /*   504     8 */
        /* --- cacheline 8 boundary (512 bytes) --- */
        ngx_event_t *              read_events;          /*   512     8 */
        ngx_event_t *              write_events;         /*   520     8 */
        ngx_cycle_t *              old_cycle;            /*   528     8 */
        ngx_str_t                  conf_file;            /*   536    16 */
        ngx_str_t                  conf_param;           /*   552    16 */
        ngx_str_t                  conf_prefix;          /*   568    16 */
        /* --- cacheline 9 boundary (576 bytes) was 8 bytes ago --- */
        ngx_str_t                  prefix;               /*   584    16 */
        ngx_str_t                  error_log;            /*   600    16 */
        ngx_str_t                  lock_file;            /*   616    16 */
        ngx_str_t                  hostname;             /*   632    16 */

        /* size: 648, cachelines: 11, members: 34 */
        /* last cacheline: 8 bytes */
};
```
