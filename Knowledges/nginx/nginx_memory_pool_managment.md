## 🧱 How Do Memory Pools Work in Nginx?
Nginx uses a chain of memory pools to manage memory efficiently. Each request gets its own pool so that:
- Allocations are fast (simple pointer bump)
- Cleanup is easy (just reset the whole pool)
- No need to track individual frees
### ngx_pool_s
```
struct ngx_pool_s {
        ngx_pool_data_t            d;                    /*     0    32 */
        size_t                     max;                  /*    32     8 */
        ngx_pool_t *               current;              /*    40     8 */
        ngx_chain_t *              chain;                /*    48     8 */
        ngx_pool_large_t *         large;                /*    56     8 */
        /* --- cacheline 1 boundary (64 bytes) --- */
        ngx_pool_cleanup_t *       cleanup;              /*    64     8 */
        ngx_log_t *                log;                  /*    72     8 */

        /* size: 80, cachelines: 2, members: 7 */
        /* last cacheline: 16 bytes */
};
```
You're looking at the structure struct ngx_pool_s, which is typically typedef'ed as ngx_pool_t in Nginx. This means:
```
typedef struct ngx_pool_s     ngx_pool_t;
```
So when you see this
```
struct ngx_pool_s {
    ...
    ngx_pool_t *current;   // same as struct ngx_pool_s *
    ...
};
```
It's just a self-referential pointer — a very common pattern in C data structures like linked lists, trees, or pools.

This is a pointer to another ngx_pool_t , and it has a specific purpose in Nginx memory management.

The current pointer allows Nginx to navigate between pools in a hierarchy or list.
```
Pool A
├── d (data area)
├── current → Pool B
└── ...

Pool B
├── d
├── current → Pool C
└── ...

Pool C
├── current → NULL
```

When Nginx wants to allocate memory:
- It starts at the current pool (current)
- If there's not enough space, it may create a new pool and update the links
- This helps avoid fragmentation and makes bulk freeing efficient.

Use Cases for current

In practice, current is used in situations like:
- Streaming uploads/downloads: You might have one main pool and sub-pools for each stage.
- Handling HTTP headers/body: Separate allocations can be grouped into different pools.
- Chaining internal buffers (ngx_chain_t) across multiple pools.

Here's how you'd loop through pools using current in C code:
```
ngx_pool_t *p = cycle->pool;

while (p) {
    ngx_log_debug1(NGX_LOG_DEBUG, log, 0, "Pool at %p", p);
    p = p->current;  // move to the next pool in the chain
}
```
And in bpftrace (with CO-RE), you could do something similar:
```
bpftrace -e '
uprobe:/opt/nginx/sbin/nginx:ngx_worker_process_init {
    $cycle = (struct ngx_cycle_s *)arg0;
    $pool = $cycle->pool;

    printf("Main pool: %p\n", $pool);
    printf("Next pool (current): %p\n", ((struct ngx_pool_s *)$pool)->current);
}'
..
Attaching 1 probe...
Main pool: 0x28da0b0
Next pool (current): 0x28da0b0
```
Examine  ngx_pood_data_t in ngx_pool_s:
```
typedef struct {
    u_char               *last; // next free byte
    u_char               *end; // end of block
    ngx_pool_t           *next; // next pool in list
    ngx_uint_t            failed;  // allocation failure count
} ngx_pool_data_t;
```
We can imagine ngx_pool_s like this:
```
ngx_pool_t
│
├── d.last          → start of available memory
├── d.end           → end of current chunk
├── d.next          → next pool in global list
├── d.failed        → allocation stats
├── max             → threshold for small vs large allocations
├── current         → currently active pool for allocations
├── large           → list of large allocations
├── cleanup         → list of cleanup callbacks
└── log             → logging context
```
On github there even a module created in the past which helps debug memory pools - https://github.com/chobits/ngx_debug_pool
```
$ curl http://localhost:80/debug_pool
..
pid:1671
size:      502312 num:           6 cnum:           1 lnum:          31 ngx_init_cycle
size:           0 num:           1 cnum:           0 lnum:           0 ngx_http_spdy_keepalive_handler
size:        1536 num:         195 cnum:           1 lnum:        1635 ngx_event_accept
size:           0 num:          11 cnum:           0 lnum:           0 ngx_http_upstream_connect
size:           0 num:           1 cnum:           0 lnum:           0 ngx_http_lua_create_fake_request
size:           0 num:           1 cnum:           0 lnum:           0 main
size:           0 num:           1 cnum:           0 lnum:           0 ngx_http_lua_create_fake_connection
size:           0 num:           1 cnum:           0 lnum:           0 ngx_http_spdy_init
size:           0 num:           3 cnum:           0 lnum:          18 ngx_http_server_names
size:        8192 num:         810 cnum:           1 lnum:          11 ngx_http_create_request
size:           0 num:           1 cnum:           0 lnum:           0 ngx_http_lua_init_worker
size:       500KB num:        1031 cnum:           3 lnum:        1695 [SUMMARY]
```
Data
====

Every line except the last one of output content has the same format, as follows:

"__size__: %12u __num__: %12u __cnum__: %12u __lnum__: %12u __\<function name\>__"

* __size__: size of current used memory of this pool
* __num__:  number of created pool (including current used pool and destroyed pool)
* __cnum__: number of current used pool
* __lnum__: number of calling ngx_palloc_large()
  * If allocated memory is larger than predefined size of memory pool, nginx will allocate memory via malloc(ngx_alloc) in ngx_palloc_large().
* __funcion name__: which nginx C function creates this pool
  * With function name of pool creator, we can know memory usage of every module, for example:
  * pool created by `ngx_http_create_request` is used for one HTTP request.
    * Because most modules allocates memory from this pool directly, it's hard to distinguish between them.
  * pool created by `ngx_event_accept` is used for TCP connection from client.
  * pool created by `ngx_http_upstream_connect` is used for HTTP connection to upstream peer.
  * pool created by `ngx_http_spdy_init` is used for SPDY session.
    * This pool will be freed and recreated by `ngx_http_spdy_keepalive_handler` when spdy connection goes idle.
  * pool created by `ngx_init_cycle` is used for parsing nginx configuration and keeping other global data structures.
  * pool created by `ngx_http_lua_init_worker` is used for conf.temp_pool of directive [init_worker_by_lua](https://github.com/openresty/lua-nginx-module#init_worker_by_lua).
  * ...

Last line of output content summarizes the information of all memory pools.
