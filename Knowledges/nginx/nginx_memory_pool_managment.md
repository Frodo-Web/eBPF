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
