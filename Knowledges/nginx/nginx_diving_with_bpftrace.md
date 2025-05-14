# Nginx: Diving with bpftrace
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
### Main functions
### ngx_worker_process_init
- This function is called once per worker process at startup.
- It initializes modules and sets up listening sockets.
- Ensures the worker can handle incoming connections.
### ngx_event_accept()
- Triggered when a new TCP connection comes in on port 80 or 443.
- Accepts the connection and adds it to the event loop.
### ngx_http_init_request()
- Called when the first HTTP data is read from the connection.
- Initializes the HTTP request structure (ngx_http_request_t).
- Parses headers and prepares for request processing.
### ngx_http_core_run_phases()
This is the main function that runs the HTTP request processing phases .

It goes through various phases like:
- NGX_HTTP_POST_READ_PHASE
- NGX_HTTP_SERVER_REWRITE_PHASE
- NGX_HTTP_FIND_CONFIG_PHASE (matches location block)
- NGX_HTTP_REWRITE_PHASE
- NGX_HTTP_POST_REWRITE_PHASE
- NGX_HTTP_ACCESS_PHASE (checks access rules like allow/deny)
- NGX_HTTP_CONTENT_PHASE → This is where content gets generated!
### ngx_http_static_handler()
If the request matches a static file (like /index.html) and no rewrite/proxy rules apply, this handler is used.

This function:
- Checks if the file exists using ngx_open_file() or equivalent system calls.
- Sets proper MIME type based on extension (e.g., text/html).
- Sends HTTP headers via ngx_http_send_header().
- Sends the file body using ngx_http_send_special() and ngx_http_output_filter().

### ngx_http_send_header()
Sends the HTTP response headers to the client.

Includes things like:
- Content-Type: text/html
- Content-Length
- Last-Modified
- ETag (if enabled)

### ngx_http_send_response() / ngx_http_output_filter()
- Handles sending the actual file content.
- Uses efficient mechanisms like sendfile() (on Linux) or aio (for asynchronous I/O) depending on config.
- Buffers output if needed.

### ngx_http_finalize_request()
- Cleans up the request after completion.
- Closes file handles and logs access (via ngx_http_log_request()).

### Relevant files:
- src/http/ngx_http_core_module.c – Core request handling
- src/http/modules/ngx_http_static_module.c – Static file handler
- src/http/ngx_http_request.c – Main request lifecycle functions
```
location / {
    root /usr/share/nginx/html;
}
```
This maps the URI /index.html to the filesystem path /usr/share/nginx/html/index.html.

Internally, Nginx uses ngx_http_map_uri_to_path() to resolve this.
### Using nm, readelf, objdump and bpftrace to find symbols
#### nm
```
nm /opt/nginx/sbin/nginx | grep ngx_worker_process_init
..
000000000044faec t ngx_worker_process_init
```
#### readelf
```
readelf -sW /opt/nginx/sbin/nginx | grep ngx_worker_process_init
..
   765: 000000000044faec  2385 FUNC    LOCAL  DEFAULT    7 ngx_worker_process_init
```
#### objdump
```
objdump -t /opt/nginx/sbin/nginx | grep ngx_worker_process_init
..
000000000044faec l     F .text  0000000000000951 ngx_worker_process_init
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
### Find out typedef references
For example we don't have access to the source code, and want to figure out to what structure ngx_queue_t references, implying:
```
typedef struct ngx_queue_s  ngx_queue_t;

struct ngx_queue_s {
    ngx_queue_t  *prev;
    ngx_queue_t  *next;
};
```
readelf tool can help with that
```
readelf -wi /opt/nginx/sbin/nginx
```
Look for something like
```
<some_offset> DW_TAG_typedef
              DW_AT_name        "ngx_queue_t"
              DW_AT_type        <offset to struct ngx_queue_s>
              ...
```
And also
```
<other_offset> DW_TAG_structure_type
                 DW_AT_name        "ngx_queue_s"
```
This tells you that ngx_queue_t is just an alias (typedef) for struct ngx_queue_s.
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
### Check this out
Attach to uprobe, note '-f json' so the output won't be bufferized (printed only when you press Ctrl + C)
```
sudo bpftrace -f json -e 'uprobe:/opt/nginx/sbin/nginx:ngx_worker_process_init { printf("Worker ID: %d", arg1); }'
..
{"type": "attached_probes", "data": {"probes": 1}}
```
OR just add '\n', bpftrace automatically flushes on newline
```
sudo bpftrace -e '
uprobe:/opt/nginx/sbin/nginx:ngx_worker_process_init {
    printf("Worker ID: %d\n", arg1);
    usleep(100000);  // optional: give time for flush
}'
```
Here arg1 is ngx_int_t worker

Send sighup to master process of nginx
```
kill -s SIGHUP 35102
```
The line will appear
```
{"type": "printf", "data": "Worker ID: 0"}
```
To access fields inside cycle:
```
 bpftrace -f json -e 'uprobe:/opt/nginx/sbin/nginx:ngx_worker_process_init {
    printf("worker: %d", arg1);
    printf("free_connection_n: %d", ((struct ngx_cycle_s *)arg0)->free_connection_n);
}'
..
{"type": "attached_probes", "data": {"probes": 1}}
{"type": "printf", "data": "worker: 0"}
{"type": "printf", "data": "free_connection_n: 0"}
```
This works if your kernel supports CO-RE (BTF + BPF skeletons), or you're using usdt probes.

Otherwise, needs to manually type offsets..

To access nested data, like ngx_cycle_s -> ngx_pool_s -> size_t (max), ngx_pool_t (current), ngx_pool_large_t (large), ngx_pool_cleanup_t (cleanup)
```
struct ngx_cycle_s {
    ...
    ngx_pool_t *pool;  // offset 8
    ...
};

struct ngx_pool_s {
        size_t                     max;                  /* offset 32
        ngx_pool_t *               current;              /*    40     8 */
        ngx_pool_large_t *         large;                /*    56     8 */
        ngx_pool_cleanup_t *       cleanup;              /*    64     8 */
};
```
We can build a query like this
```
sudo bpftrace -f json -e '
uprobe:/opt/nginx/sbin/nginx:ngx_worker_process_init {
    $cycle = (struct ngx_cycle_s *)arg0;
    $pool = (struct ngx_pool_s *)$cycle->pool;

    printf("worker: %d", arg1);
    printf("free_connection_n: %llu", $cycle->free_connection_n);
    printf("pool_max: %llu", $pool->max);
    printf("pool_current: %p", $pool->current);
    printf("pool_large: %p", $pool->large);
    printf("pool_cleanup: %p", $pool->cleanup);
}'
..
{"type": "attached_probes", "data": {"probes": 1}}
{"type": "printf", "data": "worker: 0"}
{"type": "printf", "data": "free_connection_n: 0"}
{"type": "printf", "data": "pool_max: 4095"}
{"type": "printf", "data": "pool_current: 0x28da0b0"}
{"type": "printf", "data": "pool_large: 0x2905a28"}
{"type": "printf", "data": "pool_cleanup: 0x2900b30"}
```
### Other functions
```
objdump -t /opt/nginx/sbin/nginx | grep event_accept
..
0000000000000000 l    df *ABS*  0000000000000000 ngx_event_accept.c
0000000000441889 g     F .text  0000000000000bd0 ngx_event_accept

bpftrace -lv '*:/opt/nginx/sbin/nginx:ngx_event_accept'
..
uprobe:/opt/nginx/sbin/nginx:ngx_event_accept
    ngx_event_t * ev
```
```
pahole /opt/nginx/sbin/nginx | less
..
struct ngx_event_s {
        void *                     data;                 /*     0     8 */
        unsigned int               write:1;              /*     8: 0  4 */
        unsigned int               accept:1;             /*     8: 1  4 */
        unsigned int               instance:1;           /*     8: 2  4 */
        unsigned int               active:1;             /*     8: 3  4 */
        unsigned int               disabled:1;           /*     8: 4  4 */
        unsigned int               ready:1;              /*     8: 5  4 */
        unsigned int               oneshot:1;            /*     8: 6  4 */
        unsigned int               complete:1;           /*     8: 7  4 */
        unsigned int               eof:1;                /*     8: 8  4 */
        unsigned int               error:1;              /*     8: 9  4 */
        unsigned int               timedout:1;           /*     8:10  4 */
        unsigned int               timer_set:1;          /*     8:11  4 */
        unsigned int               delayed:1;            /*     8:12  4 */
        unsigned int               deferred_accept:1;    /*     8:13  4 */
        unsigned int               pending_eof:1;        /*     8:14  4 */
        unsigned int               posted:1;             /*     8:15  4 */
        unsigned int               closed:1;             /*     8:16  4 */
        unsigned int               channel:1;            /*     8:17  4 */
        unsigned int               resolver:1;           /*     8:18  4 */
        unsigned int               cancelable:1;         /*     8:19  4 */

        /* XXX 12 bits hole, try to pack */

        int                        available;            /*    12     4 */
        ngx_event_handler_pt       handler;              /*    16     8 */
        ngx_uint_t                 index;                /*    24     8 */
        ngx_log_t *                log;                  /*    32     8 */
        ngx_rbtree_node_t          timer;                /*    40    40 */
        /* --- cacheline 1 boundary (64 bytes) was 16 bytes ago --- */
        ngx_queue_t                queue;                /*    80    16 */

        /* size: 96, cachelines: 2, members: 27 */
        /* sum members: 92 */
        /* sum bitfield members: 20 bits, bit holes: 1, sum bit holes: 12 bits */
        /* last cacheline: 32 bytes */
};
```
