## SLAB allocator
SLAB allocator:
- Purpose: Optimizes memory allocation for small, frequently used kernel objects (e.g., process descriptors, network sockets, filesystem metadata).
- Replaces traditional malloc() in kernel space to reduce fragmentation and improve performance.

Three main allocators in Linux history:
- SLAB (original, now mostly deprecated)
- SLUB (default in modern kernels, simpler and more scalable)
- SLOB (for embedded systems with very low memory)
### /proc/slabinfo, slabtop
```
cat /proc/slabinfo
slabinfo - version: 2.1
# name            <active_objs> <num_objs> <objsize> <objperslab> <pagesperslab> : tunables <limit> <batchcount> <sharedfactor> : slabdata <active_slabs> <num_slabs> <sharedavail>
pid_2                 84     84    192   21    1 : tunables    0    0    0 : slabdata      4      4      0
nf_conntrack_expect      0      0    208   19    1 : tunables    0    0    0 : slabdata      0      0      0
nf_conntrack          80     80    256   16    1 : tunables    0    0    0 : slabdata      5      5      0
nf-frags               0      0    184   22    1 : tunables    0    0    0 : slabdata      0      0      0
kvm_async_pf           0      0    136   30    1 : tunables    0    0    0 : slabdata      0      0      0
kvm_vcpu               0      0   9216    3    8 : tunables    0    0    0 : slabdata      0      0      0
kvm_mmu_page_header      0      0    184   22    1 : tunables    0    0    0 : slabdata      0      0      0
pte_list_desc          0      0    128   32    1 : tunables    0    0    0 : slabdata      0      0      0
x86_emulator           0      0   2672   12    8 : tunables    0    0    0 : slabdata      0      0      0
fat_inode_cache       21     21    768   21    4 : tunables    0    0    0 : slabdata      1      1      0
fat_cache              0      0     40  102    1 : tunables    0    0    0 : slabdata      0      0      0
i915_vma_resource     50     50    320   25    2 : tunables    0    0    0 : slabdata      2      2      0
i915_vma              50     50    640   25    4 : tunables    0    0    0 : slabdata      2      2      0
i915_priolist          0      0     48   85    1 : tunables    0    0    0 : slabdata      0      0      0
i915_dependency        0      0    128   32    1 : tunables    0    0    0 : slabdata      0      0      0
execute_cb             0      0     64   64    1 : tunables    0    0    0 : slabdata      0      0      0
i915_request          46     46    704   23    4 : tunables    0    0    0 : slabdata      2      2      0
drm_i915_gem_object    588    588   1152   28    8 : tunables    0    0    0 : slabdata     21     21      0
i915_lut_handle        0      0     32  128    1 : tunables    0    0    0 : slabdata      0      0      0
intel_context         42     42    768   21    4 : tunables    0    0    0 : slabdata      2      2      0
active_node           32     32    128   32    1 : tunables    0    0    0 : slabdata      1      1      0
xfs_dqtrx              0      0   1320   24    8 : tunables    0    0    0 : slabdata      0      0      0
xfs_dquot              0      0    528   31    4 : tunables    0    0    0 : slabdata      0      0      0
xfs_parent_args        0      0    168   24    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_xmi_item           0      0    248   16    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_xmd_item           0      0    176   23    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_iul_item           0      0    176   23    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_attri_item         0      0    208   19    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_attrd_item         0      0    176   23    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_bui_item           0      0    208   19    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_bud_item           0      0    176   23    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_cui_item           0      0    432   18    2 : tunables    0    0    0 : slabdata      0      0      0
xfs_cud_item           0      0    176   23    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_rui_item           0      0    688   23    4 : tunables    0    0    0 : slabdata      0      0      0
xfs_rud_item           0      0    176   23    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_icr                0      0    184   22    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_ili               60     60    200   20    1 : tunables    0    0    0 : slabdata      3      3      0
xfs_inode             48     48   1024   16    4 : tunables    0    0    0 : slabdata      3      3      0
xfs_efi_item          18     18    432   18    2 : tunables    0    0    0 : slabdata      1      1      0
xfs_efd_item          18     18    440   18    2 : tunables    0    0    0 : slabdata      1      1      0
xfs_buf_item         120    120    272   30    2 : tunables    0    0    0 : slabdata      4      4      0
xfs_trans             68     68    232   17    1 : tunables    0    0    0 : slabdata      4      4      0
xfs_ifork              0      0     48   85    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_da_state           0      0    480   17    2 : tunables    0    0    0 : slabdata      0      0      0
xfs_exchmaps_intent      0      0     80   51    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_attr_intent       46     46     88   46    1 : tunables    0    0    0 : slabdata      1      1      0
xfs_extfree_intent     73     73     56   73    1 : tunables    0    0    0 : slabdata      1      1      0
xfs_bmap_intent        0      0     72   56    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_refc_intent        0      0     48   85    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_rmap_intent        0      0     80   51    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_defer_pending     64     64     64   64    1 : tunables    0    0    0 : slabdata      1      1      0
xfs_rtrefcountbt_cur      0      0    216   18    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_rtrmapbt_cur       0      0    456   17    2 : tunables    0    0    0 : slabdata      0      0      0
xfs_refcbt_cur         0      0    216   18    1 : tunables    0    0    0 : slabdata      0      0      0
xfs_rmapbt_cur         0      0    280   29    2 : tunables    0    0    0 : slabdata      0      0      0
xfs_bmbt_cur           0      0    344   23    2 : tunables    0    0    0 : slabdata      0      0      0
xfs_inobt_cur         36     36    216   18    1 : tunables    0    0    0 : slabdata      2      2      0
xfs_bnobt_cur         17     17    232   17    1 : tunables    0    0    0 : slabdata      1      1      0
xfs_log_ticket       340    340     48   85    1 : tunables    0    0    0 : slabdata      4      4      0
xfs_buf               63     63    384   21    2 : tunables    0    0    0 : slabdata      3      3      0
drm_buddy_block        0      0     72   56    1 : tunables    0    0    0 : slabdata      0      0      0
bio-160               21     21    192   21    1 : tunables    0    0    0 : slabdata      1      1      0
kcopyd_job             0      0   3240   10    8 : tunables    0    0    0 : slabdata      0      0      0
io                     0      0     64   64    1 : tunables    0    0    0 : slabdata      0      0      0
dm_uevent              0      0   2888   11    8 : tunables    0    0    0 : slabdata      0      0      0
ext4_groupinfo_4k   2178   2178    184   22    1 : tunables    0    0    0 : slabdata     99     99      0
ext4_fc_dentry_update      0      0    104   39    1 : tunables    0    0    0 : slabdata      0      0      0
ext4_inode_cache   11282  11284   1152   28    8 : tunables    0    0    0 : slabdata    403    403      0
ext4_free_data       292    292     56   73    1 : tunables    0    0    0 : slabdata      4      4      0
ext4_allocation_context    104    104    152   26    1 : tunables    0    0    0 : slabdata      4      4      0
ext4_prealloc_space    144    144    112   36    1 : tunables    0    0    0 : slabdata      4      4      0
ext4_system_zone     204    204     40  102    1 : tunables    0    0    0 : slabdata      2      2      0
ext4_io_end_vec      896    896     32  128    1 : tunables    0    0    0 : slabdata      7      7      0
ext4_io_end          448    704     64   64    1 : tunables    0    0    0 : slabdata     11     11      0
bio_post_read_ctx    170    170     48   85    1 : tunables    0    0    0 : slabdata      2      2      0
pending_reservation      0      0     32  128    1 : tunables    0    0    0 : slabdata      0      0      0
extent_status       8466   8466     40  102    1 : tunables    0    0    0 : slabdata     83     83      0
mb_cache_entry       292    292     56   73    1 : tunables    0    0    0 : slabdata      4      4      0
jbd2_transaction_s    112    112    256   16    1 : tunables    0    0    0 : slabdata      7      7      0
jbd2_inode          1728   1728     64   64    1 : tunables    0    0    0 : slabdata     27     27      0
jbd2_journal_handle    511    803     56   73    1 : tunables    0    0    0 : slabdata     11     11      0
jbd2_journal_head    408    408    120   34    1 : tunables    0    0    0 : slabdata     12     12      0
jbd2_revoke_table_s    256    256     16  256    1 : tunables    0    0    0 : slabdata      1      1      0
jbd2_revoke_record_s    512    512     32  128    1 : tunables    0    0    0 : slabdata      4      4      0
bio-120              128    128    128   32    1 : tunables    0    0    0 : slabdata      4      4      0
scsi_sense_cache     352    352    128   32    1 : tunables    0    0    0 : slabdata     11     11      0
fuse_request           0      0    168   24    1 : tunables    0    0    0 : slabdata      0      0      0
fuse_inode             0      0    896   18    4 : tunables    0    0    0 : slabdata      0      0      0
net_bridge_fdb_entry    128    128    128   32    1 : tunables    0    0    0 : slabdata      4      4      0
ovl_inode              0      0    696   23    4 : tunables    0    0    0 : slabdata      0      0      0
MPTCPv6                0      0   2176   15    8 : tunables    0    0    0 : slabdata      0      0      0
ip6-frags              0      0    184   22    1 : tunables    0    0    0 : slabdata      0      0      0
fib6_node            256    256     64   64    1 : tunables    0    0    0 : slabdata      4      4      0
ip6_dst_cache         64     64    256   16    1 : tunables    0    0    0 : slabdata      4      4      0
mfc6_cache             0      0    192   21    1 : tunables    0    0    0 : slabdata      0      0      0
PINGv6                 0      0   1216   26    8 : tunables    0    0    0 : slabdata      0      0      0
RAWv6                 78     78   1216   26    8 : tunables    0    0    0 : slabdata      3      3      0
UDPLITEv6              0      0   1344   24    8 : tunables    0    0    0 : slabdata      0      0      0
UDPv6                 96     96   1344   24    8 : tunables    0    0    0 : slabdata      4      4      0
tw_sock_TCPv6         32     32    256   16    1 : tunables    0    0    0 : slabdata      2      2      0
request_sock_TCPv6     52     52    312   26    2 : tunables    0    0    0 : slabdata      2      2      0
TCPv6                 48     48   2624   12    8 : tunables    0    0    0 : slabdata      4      4      0
uhci_urb_priv          0      0     56   73    1 : tunables    0    0    0 : slabdata      0      0      0
btree_node             0      0    128   32    1 : tunables    0    0    0 : slabdata      0      0      0
io_buffer              0      0     32  128    1 : tunables    0    0    0 : slabdata      0      0      0
io_kiocb               0      0    256   16    1 : tunables    0    0    0 : slabdata      0      0      0
bfq_io_cq              0      0   1360   24    8 : tunables    0    0    0 : slabdata      0      0      0
bfq_queue              0      0    576   28    4 : tunables    0    0    0 : slabdata      0      0      0
bio-248               64     64    256   16    1 : tunables    0    0    0 : slabdata      4      4      0
mqueue_inode_cache     34     34    960   17    4 : tunables    0    0    0 : slabdata      2      2      0
kioctx               112    112    576   28    4 : tunables    0    0    0 : slabdata      4      4      0
aio_kiocb             84     84    192   21    1 : tunables    0    0    0 : slabdata      4      4      0
userfaultfd_ctx_cache      0      0    192   21    1 : tunables    0    0    0 : slabdata      0      0      0
fanotify_perm_event      0      0    112   36    1 : tunables    0    0    0 : slabdata      0      0      0
fanotify_path_event      0      0     64   64    1 : tunables    0    0    0 : slabdata      0      0      0
fanotify_fid_event      0      0     72   56    1 : tunables    0    0    0 : slabdata      0      0      0
fanotify_mark          0      0     80   51    1 : tunables    0    0    0 : slabdata      0      0      0
dnotify_mark           0      0     80   51    1 : tunables    0    0    0 : slabdata      0      0      0
dnotify_struct         0      0     32  128    1 : tunables    0    0    0 : slabdata      0      0      0
dio                    0      0    640   25    4 : tunables    0    0    0 : slabdata      0      0      0
fasync_cache           0      0     48   85    1 : tunables    0    0    0 : slabdata      0      0      0
audit_tree_mark        0      0     80   51    1 : tunables    0    0    0 : slabdata      0      0      0
pid_namespace         28     28    288   28    2 : tunables    0    0    0 : slabdata      1      1      0
posix_timers_cache      0      0    360   22    2 : tunables    0    0    0 : slabdata      0      0      0
UNIX-STREAM          160    160   1024   16    4 : tunables    0    0    0 : slabdata     10     10      0
UNIX                  96     96   1024   16    4 : tunables    0    0    0 : slabdata      6      6      0
ip4-frags              0      0    200   20    1 : tunables    0    0    0 : slabdata      0      0      0
mfc_cache              0      0    192   21    1 : tunables    0    0    0 : slabdata      0      0      0
UDP-Lite               0      0   1152   28    8 : tunables    0    0    0 : slabdata      0      0      0
MPTCP                 48     48   1984   16    8 : tunables    0    0    0 : slabdata      3      3      0
request_sock_subflow_v6      0      0    384   21    2 : tunables    0    0    0 : slabdata      0      0      0
request_sock_subflow_v4     21     21    384   21    2 : tunables    0    0    0 : slabdata      1      1      0
tcp_bind2_bucket     128    128    128   32    1 : tunables    0    0    0 : slabdata      4      4      0
tcp_bind_bucket      128    128    128   32    1 : tunables    0    0    0 : slabdata      4      4      0
inet_peer             21     21    192   21    1 : tunables    0    0    0 : slabdata      1      1      0
xfrm_dst               0      0    320   25    2 : tunables    0    0    0 : slabdata      0      0      0
xfrm_state             0      0    832   19    4 : tunables    0    0    0 : slabdata      0      0      0
ip_fib_trie          255    255     48   85    1 : tunables    0    0    0 : slabdata      3      3      0
ip_fib_alias         219    219     56   73    1 : tunables    0    0    0 : slabdata      3      3      0
rtable                84     84    192   21    1 : tunables    0    0    0 : slabdata      4      4      0
PING                   0      0   1024   16    4 : tunables    0    0    0 : slabdata      0      0      0
RAW                   16     16   1024   16    4 : tunables    0    0    0 : slabdata      1      1      0
UDP                  112    112   1152   28    8 : tunables    0    0    0 : slabdata      4      4      0
tw_sock_TCP           64     64    256   16    1 : tunables    0    0    0 : slabdata      4      4      0
request_sock_TCP     104    104    312   26    2 : tunables    0    0    0 : slabdata      4      4      0
TCP                   52     52   2432   13    8 : tunables    0    0    0 : slabdata      4      4      0
hugetlbfs_inode_cache     52     52    624   26    4 : tunables    0    0    0 : slabdata      2      2      0
dquot                  0      0    256   16    1 : tunables    0    0    0 : slabdata      0      0      0
bio-240              240    240    256   16    1 : tunables    0    0    0 : slabdata     15     15      0
backing_aio            0      0    128   32    1 : tunables    0    0    0 : slabdata      0      0      0
ep_head             1024   1024     16  256    1 : tunables    0    0    0 : slabdata      4      4      0
eventpoll_pwq        448    448     64   64    1 : tunables    0    0    0 : slabdata      7      7      0
eventpoll_epi        537    864    128   32    1 : tunables    0    0    0 : slabdata     27     27      0
inotify_inode_mark    561    561     80   51    1 : tunables    0    0    0 : slabdata     11     11      0
dax_cache             42     42    768   21    4 : tunables    0    0    0 : slabdata      2      2      0
sgpool-128            48     48   4096    8    8 : tunables    0    0    0 : slabdata      6      6      0
sgpool-64             64     64   2048   16    8 : tunables    0    0    0 : slabdata      4      4      0
sgpool-32             64     64   1024   16    4 : tunables    0    0    0 : slabdata      4      4      0
sgpool-16             64     64    512   16    2 : tunables    0    0    0 : slabdata      4      4      0
sgpool-8              64     64    256   16    1 : tunables    0    0    0 : slabdata      4      4      0
request_queue         34     34    936   17    4 : tunables    0    0    0 : slabdata      2      2      0
blkdev_ioc           184    184     88   46    1 : tunables    0    0    0 : slabdata      4      4      0
bio-184              273    273    192   21    1 : tunables    0    0    0 : slabdata     13     13      0
biovec-max           116    128   4096    8    8 : tunables    0    0    0 : slabdata     16     16      0
biovec-128            32     32   2048   16    8 : tunables    0    0    0 : slabdata      2      2      0
biovec-64             64     64   1024   16    4 : tunables    0    0    0 : slabdata      4      4      0
biovec-16             64     64    256   16    1 : tunables    0    0    0 : slabdata      4      4      0
bio_integrity_payload     21     21    192   21    1 : tunables    0    0    0 : slabdata      1      1      0
msg_msg-8k             0      0   8192    4    8 : tunables    0    0    0 : slabdata      0      0      0
msg_msg-4k             0      0   4096    8    8 : tunables    0    0    0 : slabdata      0      0      0
msg_msg-2k             0      0   2048   16    8 : tunables    0    0    0 : slabdata      0      0      0
msg_msg-1k             0      0   1024   16    4 : tunables    0    0    0 : slabdata      0      0      0
msg_msg-512            0      0    512   16    2 : tunables    0    0    0 : slabdata      0      0      0
msg_msg-256            0      0    256   16    1 : tunables    0    0    0 : slabdata      0      0      0
msg_msg-128            0      0    128   32    1 : tunables    0    0    0 : slabdata      0      0      0
msg_msg-64             0      0     64   64    1 : tunables    0    0    0 : slabdata      0      0      0
msg_msg-32             0      0     32  128    1 : tunables    0    0    0 : slabdata      0      0      0
msg_msg-16             0      0     16  256    1 : tunables    0    0    0 : slabdata      0      0      0
msg_msg-8              0      0      8  512    1 : tunables    0    0    0 : slabdata      0      0      0
msg_msg-192            0      0    192   21    1 : tunables    0    0    0 : slabdata      0      0      0
msg_msg-96             0      0     96   42    1 : tunables    0    0    0 : slabdata      0      0      0
khugepaged_mm_slot    408    408     40  102    1 : tunables    0    0    0 : slabdata      4      4      0
ksm_mm_slot            0      0     48   85    1 : tunables    0    0    0 : slabdata      0      0      0
ksm_stable_node        0      0     64   64    1 : tunables    0    0    0 : slabdata      0      0      0
ksm_rmap_item          0      0     64   64    1 : tunables    0    0    0 : slabdata      0      0      0
memdup_user-8k         0      0   8192    4    8 : tunables    0    0    0 : slabdata      0      0      0
memdup_user-4k        24     24   4096    8    8 : tunables    0    0    0 : slabdata      3      3      0
memdup_user-2k         0      0   2048   16    8 : tunables    0    0    0 : slabdata      0      0      0
memdup_user-1k         0      0   1024   16    4 : tunables    0    0    0 : slabdata      0      0      0
memdup_user-512       16     16    512   16    2 : tunables    0    0    0 : slabdata      1      1      0
memdup_user-256        0      0    256   16    1 : tunables    0    0    0 : slabdata      0      0      0
memdup_user-128       64     64    128   32    1 : tunables    0    0    0 : slabdata      2      2      0
memdup_user-64       256    256     64   64    1 : tunables    0    0    0 : slabdata      4      4      0
memdup_user-32       512    512     32  128    1 : tunables    0    0    0 : slabdata      4      4      0
memdup_user-16      1024   1024     16  256    1 : tunables    0    0    0 : slabdata      4      4      0
memdup_user-8       2048   2048      8  512    1 : tunables    0    0    0 : slabdata      4      4      0
memdup_user-192        0      0    192   21    1 : tunables    0    0    0 : slabdata      0      0      0
memdup_user-96       168    168     96   42    1 : tunables    0    0    0 : slabdata      4      4      0
user_namespace        26     26    616   26    4 : tunables    0    0    0 : slabdata      1      1      0
uid_cache             84     84    192   21    1 : tunables    0    0    0 : slabdata      4      4      0
iommu_iova_magazine      0      0   1024   16    4 : tunables    0    0    0 : slabdata      0      0      0
iommu_iova             0      0     64   64    1 : tunables    0    0    0 : slabdata      0      0      0
dmaengine-unmap-256     15     15   2112   15    8 : tunables    0    0    0 : slabdata      1      1      0
dmaengine-unmap-128     30     30   1088   30    8 : tunables    0    0    0 : slabdata      1      1      0
dmaengine-unmap-16     21     21    192   21    1 : tunables    0    0    0 : slabdata      1      1      0
dmaengine-unmap-2     64     64     64   64    1 : tunables    0    0    0 : slabdata      1      1      0
audit_buffer         680    680     24  170    1 : tunables    0    0    0 : slabdata      4      4      0
sock_inode_cache     418    418    832   19    4 : tunables    0    0    0 : slabdata     22     22      0
skbuff_ext_cache      84     84    192   21    1 : tunables    0    0    0 : slabdata      4      4      0
skbuff_small_head    322    414    704   23    4 : tunables    0    0    0 : slabdata     18     18      0
skbuff_fclone_cache     64     64    512   16    2 : tunables    0    0    0 : slabdata      4      4      0
skbuff_head_cache    336    336    256   16    1 : tunables    0    0    0 : slabdata     21     21      0
tracefs_inode_cache    175    175    648   25    4 : tunables    0    0    0 : slabdata      7      7      0
debugfs_inode_cache    725    725    632   25    4 : tunables    0    0    0 : slabdata     29     29      0
configfs_dir_cache      0      0     88   46    1 : tunables    0    0    0 : slabdata      0      0      0
file_lease_cache       0      0    160   25    1 : tunables    0    0    0 : slabdata      0      0      0
file_lock_cache       84     84    192   21    1 : tunables    0    0    0 : slabdata      4      4      0
file_lock_ctx        438    438     56   73    1 : tunables    0    0    0 : slabdata      6      6      0
fsnotify_mark_connector    680    680     24  170    1 : tunables    0    0    0 : slabdata      4      4      0
buffer_head       211926 211926    104   39    1 : tunables    0    0    0 : slabdata   5434   5434      0
x86_lbr                0      0    800   20    4 : tunables    0    0    0 : slabdata      0      0      0
task_delay_info        0      0    256   16    1 : tunables    0    0    0 : slabdata      0      0      0
taskstats            116    116    560   29    4 : tunables    0    0    0 : slabdata      4      4      0
proc_dir_entry       693    693    192   21    1 : tunables    0    0    0 : slabdata     33     33      0
pde_opener           408    408     40  102    1 : tunables    0    0    0 : slabdata      4      4      0
proc_inode_cache    2084   2139    688   23    4 : tunables    0    0    0 : slabdata     93     93      0
seq_file             136    136    120   34    1 : tunables    0    0    0 : slabdata      4      4      0
sigqueue             204    204     80   51    1 : tunables    0    0    0 : slabdata      4      4      0
bdev_cache            60     60   1600   20    8 : tunables    0    0    0 : slabdata      3      3      0
shmem_inode_cache   3131   3256    744   22    4 : tunables    0    0    0 : slabdata    148    148      0
kernfs_iattrs_cache   1410   1785     80   51    1 : tunables    0    0    0 : slabdata     35     35      0
kernfs_node_cache  43965  44220    136   30    1 : tunables    0    0    0 : slabdata   1474   1474      0
mnt_cache            777    777    384   21    2 : tunables    0    0    0 : slabdata     37     37      0
bfilp                  0      0    256   16    1 : tunables    0    0    0 : slabdata      0      0      0
filp                1593   1701    192   21    1 : tunables    0    0    0 : slabdata     81     81      0
inode_cache        11884  12038    616   26    4 : tunables    0    0    0 : slabdata    463    463      0
dentry             33217  33516    192   21    1 : tunables    0    0    0 : slabdata   1596   1596      0
names_cache           56     88   4096    8    8 : tunables    0    0    0 : slabdata     11     11      0
net_namespace         14     14   4672    7    8 : tunables    0    0    0 : slabdata      2      2      0
ima_iint_cache         0      0    104   39    1 : tunables    0    0    0 : slabdata      0      0      0
hashtab_node       17680  17680     24  170    1 : tunables    0    0    0 : slabdata    104    104      0
ebitmap_node       45120  45120     64   64    1 : tunables    0    0    0 : slabdata    705    705      0
avtab_extended_perms      0      0     40  102    1 : tunables    0    0    0 : slabdata      0      0      0
avtab_node         93160  93160     24  170    1 : tunables    0    0    0 : slabdata    548    548      0
extended_perms_data      0      0     32  128    1 : tunables    0    0    0 : slabdata      0      0      0
avc_xperms_decision_node      0      0     48   85    1 : tunables    0    0    0 : slabdata      0      0      0
avc_xperms_node        0      0     56   73    1 : tunables    0    0    0 : slabdata      0      0      0
avc_node             962   1064     72   56    1 : tunables    0    0    0 : slabdata     19     19      0
lsm_inode_cache    29264  29580    120   34    1 : tunables    0    0    0 : slabdata    870    870      0
lsm_file_cache      1709   2048     32  128    1 : tunables    0    0    0 : slabdata     16     16      0
key_jar              384    384    256   16    1 : tunables    0    0    0 : slabdata     24     24      0
uts_namespace         72     72    432   18    2 : tunables    0    0    0 : slabdata      4      4      0
nsproxy              224    224     72   56    1 : tunables    0    0    0 : slabdata      4      4      0
vma_lock            5999   6732     40  102    1 : tunables    0    0    0 : slabdata     66     66      0
vm_area_struct      5675   6072    176   23    1 : tunables    0    0    0 : slabdata    264    264      0
fs_cache             256    256     64   64    1 : tunables    0    0    0 : slabdata      4      4      0
files_cache          138    138    704   23    4 : tunables    0    0    0 : slabdata      6      6      0
signal_cache         276    308   1152   28    8 : tunables    0    0    0 : slabdata     11     11      0
sighand_cache        255    255   2112   15    8 : tunables    0    0    0 : slabdata     17     17      0
task_struct          195    212   6656    4    8 : tunables    0    0    0 : slabdata     53     53      0
cred                 609    609    192   21    1 : tunables    0    0    0 : slabdata     29     29      0
anon_vma_chain      2929   3200     64   64    1 : tunables    0    0    0 : slabdata     50     50      0
anon_vma            1893   2145    104   39    1 : tunables    0    0    0 : slabdata     55     55      0
pid                  336    336    192   21    1 : tunables    0    0    0 : slabdata     16     16      0
Acpi-Operand        4536   4536     72   56    1 : tunables    0    0    0 : slabdata     81     81      0
Acpi-ParseExt        204    204     80   51    1 : tunables    0    0    0 : slabdata      4      4      0
Acpi-Parse           365    365     56   73    1 : tunables    0    0    0 : slabdata      5      5      0
Acpi-State           204    204     80   51    1 : tunables    0    0    0 : slabdata      4      4      0
Acpi-Namespace      2805   2805     48   85    1 : tunables    0    0    0 : slabdata     33     33      0
shared_policy_node      0      0     48   85    1 : tunables    0    0    0 : slabdata      0      0      0
numa_policy           30     30    272   30    2 : tunables    0    0    0 : slabdata      1      1      0
perf_event            96     96   1312   24    8 : tunables    0    0    0 : slabdata      4      4      0
trace_event_file    2982   2982     96   42    1 : tunables    0    0    0 : slabdata     71     71      0
ftrace_event_field   7738   7738     56   73    1 : tunables    0    0    0 : slabdata    106    106      0
pool_workqueue       352    352    512   16    2 : tunables    0    0    0 : slabdata     22     22      0
maple_node          1239   1744    256   16    1 : tunables    0    0    0 : slabdata    109    109      0
radix_tree_node     8532   8624    584   28    4 : tunables    0    0    0 : slabdata    308    308      0
task_group           125    125    640   25    4 : tunables    0    0    0 : slabdata      5      5      0
mm_struct             92     92   1408   23    8 : tunables    0    0    0 : slabdata      4      4      0
vmap_area           3864   3864     72   56    1 : tunables    0    0    0 : slabdata     69     69      0
kmalloc_buckets       36     36    112   36    1 : tunables    0    0    0 : slabdata      1      1      0
kmalloc-cg-8k          4      4   8192    4    8 : tunables    0    0    0 : slabdata      1      1      0
kmalloc-cg-4k         88     88   4096    8    8 : tunables    0    0    0 : slabdata     11     11      0
kmalloc-cg-2k        428    544   2048   16    8 : tunables    0    0    0 : slabdata     34     34      0
kmalloc-cg-1k        261    288   1024   16    4 : tunables    0    0    0 : slabdata     18     18      0
kmalloc-cg-512       240    240    512   16    2 : tunables    0    0    0 : slabdata     15     15      0
kmalloc-cg-256        80     80    256   16    1 : tunables    0    0    0 : slabdata      5      5      0
kmalloc-cg-128       224    224    128   32    1 : tunables    0    0    0 : slabdata      7      7      0
kmalloc-cg-64        448    448     64   64    1 : tunables    0    0    0 : slabdata      7      7      0
kmalloc-cg-32       5131   5632     32  128    1 : tunables    0    0    0 : slabdata     44     44      0
kmalloc-cg-16       1024   1024     16  256    1 : tunables    0    0    0 : slabdata      4      4      0
kmalloc-cg-8        2048   2048      8  512    1 : tunables    0    0    0 : slabdata      4      4      0
kmalloc-cg-192       189    189    192   21    1 : tunables    0    0    0 : slabdata      9      9      0
kmalloc-cg-96       4443   5082     96   42    1 : tunables    0    0    0 : slabdata    121    121      0
dma-kmalloc-8k         0      0   8192    4    8 : tunables    0    0    0 : slabdata      0      0      0
dma-kmalloc-4k         0      0   4096    8    8 : tunables    0    0    0 : slabdata      0      0      0
dma-kmalloc-2k         0      0   2048   16    8 : tunables    0    0    0 : slabdata      0      0      0
dma-kmalloc-1k         0      0   1024   16    4 : tunables    0    0    0 : slabdata      0      0      0
dma-kmalloc-512        0      0    512   16    2 : tunables    0    0    0 : slabdata      0      0      0
dma-kmalloc-256        0      0    256   16    1 : tunables    0    0    0 : slabdata      0      0      0
dma-kmalloc-128        0      0    128   32    1 : tunables    0    0    0 : slabdata      0      0      0
dma-kmalloc-64         0      0     64   64    1 : tunables    0    0    0 : slabdata      0      0      0
dma-kmalloc-32         0      0     32  128    1 : tunables    0    0    0 : slabdata      0      0      0
dma-kmalloc-16       256    256     16  256    1 : tunables    0    0    0 : slabdata      1      1      0
dma-kmalloc-8          0      0      8  512    1 : tunables    0    0    0 : slabdata      0      0      0
dma-kmalloc-192        0      0    192   21    1 : tunables    0    0    0 : slabdata      0      0      0
dma-kmalloc-96         0      0     96   42    1 : tunables    0    0    0 : slabdata      0      0      0
kmalloc-rcl-8k         0      0   8192    4    8 : tunables    0    0    0 : slabdata      0      0      0
kmalloc-rcl-4k         0      0   4096    8    8 : tunables    0    0    0 : slabdata      0      0      0
kmalloc-rcl-2k         0      0   2048   16    8 : tunables    0    0    0 : slabdata      0      0      0
kmalloc-rcl-1k         0      0   1024   16    4 : tunables    0    0    0 : slabdata      0      0      0
kmalloc-rcl-512        0      0    512   16    2 : tunables    0    0    0 : slabdata      0      0      0
kmalloc-rcl-256        0      0    256   16    1 : tunables    0    0    0 : slabdata      0      0      0
kmalloc-rcl-128      128    128    128   32    1 : tunables    0    0    0 : slabdata      4      4      0
kmalloc-rcl-64         0      0     64   64    1 : tunables    0    0    0 : slabdata      0      0      0
kmalloc-rcl-32         0      0     32  128    1 : tunables    0    0    0 : slabdata      0      0      0
kmalloc-rcl-16         0      0     16  256    1 : tunables    0    0    0 : slabdata      0      0      0
kmalloc-rcl-8          0      0      8  512    1 : tunables    0    0    0 : slabdata      0      0      0
kmalloc-rcl-192        0      0    192   21    1 : tunables    0    0    0 : slabdata      0      0      0
kmalloc-rcl-96       420    420     96   42    1 : tunables    0    0    0 : slabdata     10     10      0
kmalloc-8k           100    112   8192    4    8 : tunables    0    0    0 : slabdata     28     28      0
kmalloc-4k           472    480   4096    8    8 : tunables    0    0    0 : slabdata     60     60      0
kmalloc-2k           712    784   2048   16    8 : tunables    0    0    0 : slabdata     49     49      0
kmalloc-1k          1790   1824   1024   16    4 : tunables    0    0    0 : slabdata    114    114      0
kmalloc-512         7277   7328    512   16    2 : tunables    0    0    0 : slabdata    458    458      0
kmalloc-256         4313   4352    256   16    1 : tunables    0    0    0 : slabdata    272    272      0
kmalloc-128          995   1024    128   32    1 : tunables    0    0    0 : slabdata     32     32      0
kmalloc-64         14986  15488     64   64    1 : tunables    0    0    0 : slabdata    242    242      0
kmalloc-32         20652  20992     32  128    1 : tunables    0    0    0 : slabdata    164    164      0
kmalloc-16         30781  31232     16  256    1 : tunables    0    0    0 : slabdata    122    122      0
kmalloc-8          15321  15360      8  512    1 : tunables    0    0    0 : slabdata     30     30      0
kmalloc-192         3505   3612    192   21    1 : tunables    0    0    0 : slabdata    172    172      0
kmalloc-96          5271   5922     96   42    1 : tunables    0    0    0 : slabdata    141    141      0
kmem_cache_node      448    448     64   64    1 : tunables    0    0    0 : slabdata      7      7      0
kmem_cache           368    368    256   16    1 : tunables    0    0    0 : slabdata     23     23      0
```

## Contiguous Memory Allocator (CMA)
The Contiguous Memory Allocator (CMA) is a memory management mechanism in the Linux kernel designed to allocate contiguous blocks of physical memory for devices that require large, physically contiguous memory regions.

Key Features of CMA:

Purpose:

- Some hardware devices (e.g., GPUs, DMA controllers, video codecs) require physically contiguous memory for efficient operation.

- Traditional memory allocation (e.g., kmalloc) may fail for large contiguous blocks due to memory fragmentation.

How CMA Works:

- Reserved at Boot Time: CMA reserves a portion of memory during kernel initialization.

Dynamic Allocation & Release:

- When not in use by devices, the CMA memory is available for general use (e.g., movable pages for the buddy allocator).

- When a device driver requests contiguous memory, CMA reclaims the memory (possibly migrating movable pages).

Advantages:

- Reduces memory waste by allowing CMA regions to be used for non-contiguous allocations when not needed.

- Avoids the need for dedicated pre-allocated memory pools.

Configuration:

- CMA size and placement are set via kernel command-line parameters (e.g., cma=64M@0x38000000).

- Can also be configured via Device Tree (for ARM-based systems).

Usage in Drivers:

- Drivers use the dma_alloc_contiguous() or CMA-specific APIs to request contiguous memory.

Example Use Cases:

- Video processing (e.g., cameras, display buffers).

- DMA operations for high-speed peripherals.

- GPU framebuffer allocations.

Comparison with Other Methods:

- vs. kmalloc: kmalloc is limited in size (typically a few MBs) and may fail under fragmentation.

- vs. vmalloc: vmalloc provides virtually contiguous (not physically contiguous) memory, unsuitable for DMA.

- vs. Reserved Memory Pools: CMA is more flexible since it allows shared usage when not needed by devices.

CMA improves memory utilization while meeting the needs of hardware requiring contiguous memory.

## Memory Commit, Overcommit, and Limits Explained

### Key Concepts
#### Commit Limit

This is the total amount of memory that the system can potentially allocate to processes, based on the current overcommit settings. Your value of ~8.18 GB represents the maximum memory (including physical RAM and swap space) that the Linux kernel will allow to be committed to processes.

#### Committed Memory (Committed_AS)

This is an estimate of how much memory has currently been promised (committed) to processes. Your value of ~567.6 MB shows the amount that applications have requested, regardless of whether they're actively using all of it.

#### How Memory Commitment Works
Memory Overcommit: Linux by default uses an "overcommit" model where it allows the sum of committed memory to exceed physical RAM + swap. This works because:

- Not all committed memory is used immediately
- Many allocations are never fully utilized
- Shared memory between processes reduces actual usage

Overcommit Modes (controlled by vm.overcommit_memory sysctl):

- 0 (default): Heuristic overcommit - kernel estimates if request can be satisfied
- 1: Always overcommit - no memory exhaustion checks
- 2: No overcommit - strict limit based on CommitLimit

```
sysctl vm.overcommit_memory
..
vm.overcommit_memory = 0
```

Commit Limit Calculation:
```
CommitLimit = (Physical RAM * overcommit_ratio) + Swap Space
(where overcommit_ratio is typically 50% by default)
```
Why This Matters

- Your system shows healthy metrics: Committed memory (567MB) is well below the commit limit (8.18GB)
- If committed memory approaches the limit, the OOM killer may terminate processes

Monitoring these values helps prevent out-of-memory situations

Key Metrics to Watch

- CommitLimit: Your ceiling for memory commitments
- Committed_AS: Current memory promises
- Swap usage: When physical RAM is exhausted
- OOM killer events: Indicates memory pressure

## Node-exporter
```
# HELP node_memory_Active_anon_bytes Memory information field Active_anon_bytes.
# TYPE node_memory_Active_anon_bytes gauge
node_memory_Active_anon_bytes 3.166208e+06
# HELP node_memory_Active_bytes Memory information field Active_bytes.
# TYPE node_memory_Active_bytes gauge
node_memory_Active_bytes 4.43011072e+08
# HELP node_memory_Active_file_bytes Memory information field Active_file_bytes.
# TYPE node_memory_Active_file_bytes gauge
node_memory_Active_file_bytes 4.39844864e+08
# HELP node_memory_AnonHugePages_bytes Memory information field AnonHugePages_bytes.
# TYPE node_memory_AnonHugePages_bytes gauge
node_memory_AnonHugePages_bytes 6.5011712e+07
# HELP node_memory_AnonPages_bytes Memory information field AnonPages_bytes.
# TYPE node_memory_AnonPages_bytes gauge
node_memory_AnonPages_bytes 1.40210176e+08
# HELP node_memory_Bounce_bytes Memory information field Bounce_bytes.
# TYPE node_memory_Bounce_bytes gauge
node_memory_Bounce_bytes 0
# HELP node_memory_Buffers_bytes Memory information field Buffers_bytes.
# TYPE node_memory_Buffers_bytes gauge
node_memory_Buffers_bytes 3.8846464e+07
# HELP node_memory_Cached_bytes Memory information field Cached_bytes.
# TYPE node_memory_Cached_bytes gauge
node_memory_Cached_bytes 1.143857152e+09
# HELP node_memory_CmaFree_bytes Memory information field CmaFree_bytes.
# TYPE node_memory_CmaFree_bytes gauge
node_memory_CmaFree_bytes 0
# HELP node_memory_CmaTotal_bytes Memory information field CmaTotal_bytes.
# TYPE node_memory_CmaTotal_bytes gauge
node_memory_CmaTotal_bytes 0
# HELP node_memory_CommitLimit_bytes Memory information field CommitLimit_bytes.
# TYPE node_memory_CommitLimit_bytes gauge
node_memory_CommitLimit_bytes 8.183586816e+09
# HELP node_memory_Committed_AS_bytes Memory information field Committed_AS_bytes.
# TYPE node_memory_Committed_AS_bytes gauge
node_memory_Committed_AS_bytes 5.67619584e+08
# HELP node_memory_DirectMap1G_bytes Memory information field DirectMap1G_bytes.
# TYPE node_memory_DirectMap1G_bytes gauge
node_memory_DirectMap1G_bytes 1.1811160064e+10
# HELP node_memory_DirectMap2M_bytes Memory information field DirectMap2M_bytes.
# TYPE node_memory_DirectMap2M_bytes gauge
node_memory_DirectMap2M_bytes 6.163529728e+09
# HELP node_memory_DirectMap4k_bytes Memory information field DirectMap4k_bytes.
# TYPE node_memory_DirectMap4k_bytes gauge
node_memory_DirectMap4k_bytes 1.44883712e+08
# HELP node_memory_Dirty_bytes Memory information field Dirty_bytes.
# TYPE node_memory_Dirty_bytes gauge
node_memory_Dirty_bytes 0
# HELP node_memory_HardwareCorrupted_bytes Memory information field HardwareCorrupted_bytes.
# TYPE node_memory_HardwareCorrupted_bytes gauge
node_memory_HardwareCorrupted_bytes 0
# HELP node_memory_HugePages_Free Memory information field HugePages_Free.
# TYPE node_memory_HugePages_Free gauge
node_memory_HugePages_Free 0
# HELP node_memory_HugePages_Rsvd Memory information field HugePages_Rsvd.
# TYPE node_memory_HugePages_Rsvd gauge
node_memory_HugePages_Rsvd 0
# HELP node_memory_HugePages_Surp Memory information field HugePages_Surp.
# TYPE node_memory_HugePages_Surp gauge
node_memory_HugePages_Surp 0
# HELP node_memory_HugePages_Total Memory information field HugePages_Total.
# TYPE node_memory_HugePages_Total gauge
node_memory_HugePages_Total 0
# HELP node_memory_Hugepagesize_bytes Memory information field Hugepagesize_bytes.
# TYPE node_memory_Hugepagesize_bytes gauge
node_memory_Hugepagesize_bytes 2.097152e+06
# HELP node_memory_Inactive_anon_bytes Memory information field Inactive_anon_bytes.
# TYPE node_memory_Inactive_anon_bytes gauge
node_memory_Inactive_anon_bytes 1.4729216e+08
# HELP node_memory_Inactive_bytes Memory information field Inactive_bytes.
# TYPE node_memory_Inactive_bytes gauge
node_memory_Inactive_bytes 8.79763456e+08
# HELP node_memory_Inactive_file_bytes Memory information field Inactive_file_bytes.
# TYPE node_memory_Inactive_file_bytes gauge
node_memory_Inactive_file_bytes 7.32471296e+08
# HELP node_memory_KernelStack_bytes Memory information field KernelStack_bytes.
# TYPE node_memory_KernelStack_bytes gauge
node_memory_KernelStack_bytes 2.932736e+06
# HELP node_memory_Mapped_bytes Memory information field Mapped_bytes.
# TYPE node_memory_Mapped_bytes gauge
node_memory_Mapped_bytes 2.20553216e+08
# HELP node_memory_MemAvailable_bytes Memory information field MemAvailable_bytes.
# TYPE node_memory_MemAvailable_bytes gauge
node_memory_MemAvailable_bytes 1.5770914816e+10
# HELP node_memory_MemFree_bytes Memory information field MemFree_bytes.
# TYPE node_memory_MemFree_bytes gauge
node_memory_MemFree_bytes 1.4826561536e+10
# HELP node_memory_MemTotal_bytes Memory information field MemTotal_bytes.
# TYPE node_memory_MemTotal_bytes gauge
node_memory_MemTotal_bytes 1.6367177728e+10
# HELP node_memory_Mlocked_bytes Memory information field Mlocked_bytes.
# TYPE node_memory_Mlocked_bytes gauge
node_memory_Mlocked_bytes 0
# HELP node_memory_NFS_Unstable_bytes Memory information field NFS_Unstable_bytes.
# TYPE node_memory_NFS_Unstable_bytes gauge
node_memory_NFS_Unstable_bytes 0
# HELP node_memory_PageTables_bytes Memory information field PageTables_bytes.
# TYPE node_memory_PageTables_bytes gauge
node_memory_PageTables_bytes 4.087808e+06
# HELP node_memory_Percpu_bytes Memory information field Percpu_bytes.
# TYPE node_memory_Percpu_bytes gauge
node_memory_Percpu_bytes 2.162688e+06
# HELP node_memory_SReclaimable_bytes Memory information field SReclaimable_bytes.
# TYPE node_memory_SReclaimable_bytes gauge
node_memory_SReclaimable_bytes 5.834752e+07
# HELP node_memory_SUnreclaim_bytes Memory information field SUnreclaim_bytes.
# TYPE node_memory_SUnreclaim_bytes gauge
node_memory_SUnreclaim_bytes 6.4274432e+07
# HELP node_memory_ShmemHugePages_bytes Memory information field ShmemHugePages_bytes.
# TYPE node_memory_ShmemHugePages_bytes gauge
node_memory_ShmemHugePages_bytes 0
# HELP node_memory_ShmemPmdMapped_bytes Memory information field ShmemPmdMapped_bytes.
# TYPE node_memory_ShmemPmdMapped_bytes gauge
node_memory_ShmemPmdMapped_bytes 0
# HELP node_memory_Shmem_bytes Memory information field Shmem_bytes.
# TYPE node_memory_Shmem_bytes gauge
node_memory_Shmem_bytes 1.0391552e+07
# HELP node_memory_Slab_bytes Memory information field Slab_bytes.
# TYPE node_memory_Slab_bytes gauge
node_memory_Slab_bytes 1.22621952e+08
# HELP node_memory_SwapCached_bytes Memory information field SwapCached_bytes.
# TYPE node_memory_SwapCached_bytes gauge
node_memory_SwapCached_bytes 0
# HELP node_memory_SwapFree_bytes Memory information field SwapFree_bytes.
# TYPE node_memory_SwapFree_bytes gauge
node_memory_SwapFree_bytes 0
# HELP node_memory_SwapTotal_bytes Memory information field SwapTotal_bytes.
# TYPE node_memory_SwapTotal_bytes gauge
node_memory_SwapTotal_bytes 0
# HELP node_memory_Unevictable_bytes Memory information field Unevictable_bytes.
# TYPE node_memory_Unevictable_bytes gauge
node_memory_Unevictable_bytes 139264
# HELP node_memory_VmallocChunk_bytes Memory information field VmallocChunk_bytes.
# TYPE node_memory_VmallocChunk_bytes gauge
node_memory_VmallocChunk_bytes 0
# HELP node_memory_VmallocTotal_bytes Memory information field VmallocTotal_bytes.
# TYPE node_memory_VmallocTotal_bytes gauge
node_memory_VmallocTotal_bytes 3.5184372087808e+13
# HELP node_memory_VmallocUsed_bytes Memory information field VmallocUsed_bytes.
# TYPE node_memory_VmallocUsed_bytes gauge
node_memory_VmallocUsed_bytes 2.7283456e+07
# HELP node_memory_WritebackTmp_bytes Memory information field WritebackTmp_bytes.
# TYPE node_memory_WritebackTmp_bytes gauge
node_memory_WritebackTmp_bytes 0
# HELP node_memory_Writeback_bytes Memory information field Writeback_bytes.
# TYPE node_memory_Writeback_bytes gauge
node_memory_Writeback_bytes 0
```
## cat /proc/meminfo 
```
MemTotal:       15983572 kB
MemFree:        14337532 kB
MemAvailable:   15262848 kB
Buffers:           39552 kB
Cached:          1118480 kB
SwapCached:            0 kB
Active:           457564 kB
Inactive:         836996 kB
Active(anon):       3096 kB
Inactive(anon):   143576 kB
Active(file):     454468 kB
Inactive(file):   693420 kB
Unevictable:         136 kB
Mlocked:               0 kB
SwapTotal:             0 kB
SwapFree:              0 kB
Zswap:                 0 kB
Zswapped:              0 kB
Dirty:                 0 kB
Writeback:             0 kB
AnonPages:        136664 kB
Mapped:           215468 kB
Shmem:             10148 kB
KReclaimable:      57076 kB
Slab:             119836 kB
SReclaimable:      57076 kB
SUnreclaim:        62760 kB
KernelStack:        2896 kB
PageTables:         4044 kB
SecPageTables:      2056 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:     7926248 kB
Committed_AS:     553848 kB
VmallocTotal:   34359738367 kB
VmallocUsed:       26660 kB
VmallocChunk:          0 kB
Percpu:             2112 kB
HardwareCorrupted:     0 kB
AnonHugePages:     63488 kB
ShmemHugePages:        0 kB
ShmemPmdMapped:        0 kB
FileHugePages:         0 kB
FilePmdMapped:         0 kB
CmaTotal:              0 kB
CmaFree:               0 kB
Unaccepted:            0 kB
HugePages_Total:      64
HugePages_Free:       64
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
Hugetlb:          131072 kB
DirectMap4k:      141488 kB
DirectMap2M:     6019072 kB
DirectMap1G:    11534336 kB
```
## Active Memory Metrics:
### node_memory_Active_anon_bytes:

Amount of anonymous memory (not file-backed) in active use.

3.166208e+06 bytes (~3.17 MB) in this case.

```
AnonPages %lu (since Linux 2.6.18)
       Non-file backed pages mapped into user-space page tables.

The way a process maps memory in Linux is usually using the mmap(2) system call which "maps files or devices into memory". The memory can be backed by an actual file in the disk, so you could handle a file as if it was a regular memory block.

However, you could also allocate empty memory section not backed by any file. Those memory pages are called "Anonymous". From the man page of mmap:

MAP_ANONYMOUS
       The mapping is not backed by any file; its contents are initialized to zero.

If you've ever programmed in C, you're probably familiar with malloc(3) and used it to allocate dynamic memory. In Linux, in most cases, under the hood malloc would actually call mmap to allocate Anonymous memory pages.

AnonPages shows the usage of the most common type of memory - dynamic memory areas that are used by process.

Note that allocating Anonymous pages using mmap or malloc will not necessarily be reflected immediately by the AnonPages; When you allocate dynamic memory, you just get a virtual address space that you can use, but the memory pages do not actually "instantiate" and mapped into the user-space memory of the process until it starts using them (write or read to/from a memory). Only then those memory pages are loaded to the RAM and accounted by AnonPages.
```

### node_memory_Active_bytes:

Total active memory (both file-backed and anonymous) currently in use.

4.43011072e+08 bytes (~443 MB) here.

### node_memory_Active_file_bytes:

Amount of file-backed (cache, mmapped files) memory in active use.

4.39844864e+08 bytes (~439.8 MB) here.

## Anonymous & Huge Pages:

### 1. Standard Pages (Regular Pages)
Size: Typically 4 KB (on most x86_64 systems).

Purpose: Used for general memory management by the Linux kernel.

Translation Lookaside Buffer (TLB) Usage:

Since pages are small, managing large memory ranges requires many page table entries (PTEs).

This leads to higher TLB misses, increasing overhead due to frequent page table walks.

Fragmentation: More likely to cause memory fragmentation when dealing with large allocations.

Use Case: Suitable for most applications where memory demands are dynamic and unpredictable.

### 2. HugePages
Size: Much larger than standard pages (commonly 2 MB or 1 GB on x86_64).

Purpose: Optimized for large memory workloads (e.g., databases, virtualization, high-performance computing).

TLB Efficiency:

Fewer PTEs are needed for the same memory range, reducing TLB misses.

Improves performance for memory-intensive applications.

Memory Allocation:

Pre-allocated at boot or runtime (avoids runtime fragmentation).

Cannot be swapped out (pinned in memory).

Administration:

Requires manual configuration (/proc/sys/vm/nr_hugepages).

Applications must explicitly request HugePages (e.g., via mmap() with MAP_HUGETLB).

Use Case: Ideal for applications needing large, contiguous memory blocks (e.g., Oracle DB, Kubernetes nodes, big data processing).

```
[root@zeus alloy1.8.2]# cat /proc/sys/vm/nr_hugepages
0
[root@zeus alloy1.8.2]# cat /proc/meminfo | grep Huge
AnonHugePages:     63488 kB
ShmemHugePages:        0 kB
FileHugePages:         0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
Hugetlb:               0 kB
[root@zeus alloy1.8.2]# echo 64 > /proc/sys/vm/nr_hugepages
[root@zeus alloy1.8.2]# cat /proc/meminfo | grep Huge
AnonHugePages:     63488 kB
ShmemHugePages:        0 kB
FileHugePages:         0 kB
HugePages_Total:      64
HugePages_Free:       64
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
Hugetlb:          131072 kB
```

| Feature          | Standard Pages (4 KB)      | HugePages (2 MB / 1 GB)    |
|------------------|---------------------------|----------------------------|
| **Size**         | Small (4 KB)              | Large (2 MB / 1 GB)        |
| **TLB Efficiency** | High overhead (more misses) | Lower overhead (fewer misses) |
| **Fragmentation** | Possible                  | Minimized (pre-allocated)  |
| **Swappable**    | Yes                       | No (pinned in RAM)         |
| **Configuration** | Dynamic (default)         | Manual setup required      |
| **Use Case**     | General-purpose           | Large memory workloads     |

## node_memory_AnonHugePages_bytes:

Anonymous transparent hugepages allocated.

6.5011712e+07 bytes (~65 MB) here.

## node_memory_AnonPages_bytes:

Total anonymous memory (not file-backed, including non-hugepages).

1.40210176e+08 bytes (~140.2 MB) here.

## Buffers & Cache:
### node_memory_Buffers_bytes:

Memory used by kernel buffers (e.g., for filesystem metadata, I/O operations).

3.8846464e+07 bytes (~38.8 MB) here.

### node_memory_Cached_bytes:

Memory used for caching files (disk reads/writes).

1.143857152e+09 bytes (~1.14 GB) here.

## CMA (Contiguous Memory Allocator):
### node_memory_CmaFree_bytes:

Free memory in the CMA region (used for DMA-capable devices).

0 bytes (no free CMA memory here).

### node_memory_CmaTotal_bytes:

Total CMA memory available.

0 bytes (CMA not configured/used here).

## Memory Commit & Limits:
### node_memory_CommitLimit_bytes:

Total memory allocatable (based on overcommit settings).

8.183586816e+09 bytes (~8.18 GB) here.

### node_memory_Committed_AS_bytes:

Estimated memory allocated by processes (may exceed physical memory).

5.67619584e+08 bytes (~567.6 MB) here.

## Direct Memory Mapping (TLB efficiency - Translation Lookaside Buffer):

```
TLB Efficiency:

The Translation Lookaside Buffer (TLB) caches virtual-to-physical address translations.

Larger pages mean fewer TLB entries are needed for the same memory range, reducing misses and improving speed.

More hugepages (1G/2M) → Better TLB efficiency → Faster memory access.

Too many small (4K) pages → More TLB misses → Slower performance.
```
### node_memory_DirectMap1G_bytes:

Memory mapped with 1GB hugepages (for performance).

1.1811160064e+10 bytes (~11.81 GB) here.

### node_memory_DirectMap2M_bytes:

Memory mapped with 2MB hugepages.

6.163529728e+09 bytes (~6.16 GB) here.

### node_memory_DirectMap4k_bytes:

Memory mapped with standard 4KB pages.

1.44883712e+08 bytes (~144.9 MB) here.

## Memory used for "bounce buffers" (temporary I/O buffers for DMA to high memory).
```
Bounce buffers are temporary memory buffers used when a device or system cannot directly access a particular region of memory due to hardware or software constraints. They act as intermediaries, "bouncing" data between the source and destination to facilitate proper data transfer.
```

### Performance Impact
- Overhead: Extra copying reduces performance.
- Avoidance: Modern 64-bit systems and IOMMUs (Input-Output Memory Management Units) help eliminate bounce buffers by remapping addresses dynamically.

Their use is diminishing with 64-bit systems and IOMMUs, but they remain relevant in legacy and embedded systems.
### node_memory_Bounce_bytes:

0 bytes (no bounce buffers in use here).

## node_memory_Dirty_bytes

```
Data Consistency & Durability
File System Integrity: If the system crashes before dirty pages are written, file data could be lost or corrupted.

Applications Expect Durability: When a program writes to a file (e.g., a database transaction), it assumes the data will persist. Delayed writes must eventually sync to disk.

Memory Reclamation (Not Just for Swap)
Freeing Up RAM: Dirty pages occupy memory. If the system runs low on free RAM, the kernel must:

Write dirty file-backed pages to disk (freeing up memory).

Swap out anonymous pages (if enabled) to the swap file/partition.

Not Just for Swap: Even if swap is disabled, file-backed dirty pages (e.g., from write() syscalls) must be flushed to their underlying storage.
```

Definition: Memory pages modified in RAM but not yet written to disk ("dirty" pages).

Value: 0 (no dirty pages in this case).

How it Works:

When files are modified in memory, the kernel marks them as "dirty."

The pdflush (or kswapd) kernel thread periodically writes dirty pages to disk.

High values can indicate I/O bottlenecks (e.g., slow disks or heavy write activity).

Tuning:

Controlled by /proc/sys/vm/dirty_ratio (max % of memory allowed to be dirty).

dirty_background_ratio triggers background writes before hitting the limit.


dirty_background_ratio (e.g., 10%): Start background writes early.

dirty_ratio (e.g., 20%): Max dirty pages before blocking writes.

dirty_expire_centisecs: How long dirty pages can stay in RAM (default: 3000 = 30 sec).

Example (reduce risk of stalls):

```
echo 10 > /proc/sys/vm/dirty_background_ratio
echo 20 > /proc/sys/vm/dirty_ratio
```

## node_memory_HardwareCorrupted_bytes
Definition: Memory corrupted due to hardware failures (ECC errors, bad RAM).

Value: 0 (no corruption detected).

How it Works:

The kernel marks faulty memory regions as "corrupted" and avoids using them.

Non-zero values indicate failing RAM (check kernel logs: dmesg | grep -i error).

Action Required: Replace faulty RAM if this value increases.

## HugePages Metrics (HugePages_Free, HugePages_Rsvd, HugePages_Surp, HugePages_Total)
Purpose: Track usage of HugePages (large memory pages to reduce TLB misses).

Values: All 0 (HugePages not configured/enabled).

How it Works:

HugePages_Total: Total allocated HugePages (configured via /proc/sys/vm/nr_hugepages).

HugePages_Free: Unused HugePages.

HugePages_Rsvd: Reserved but not yet allocated (e.g., by libhugetlbfs).

HugePages_Surp: Surplus HugePages beyond the initial allocation.

Tuning:

Critical for databases (Oracle, PostgreSQL) to reduce page table overhead.

Configure via sysctl or /proc/sys/vm/.

## node_memory_Hugepagesize_bytes
Definition: Size of a single HugePage (default: 2MB or 1GB depending on CPU).

Value: 2.097152e+06 (2 MB).

Note: Larger sizes (1GB) require CPU support (e.g., Intel x86_64 with pdpe1gb flag).

## Inactive Memory Metrics (Inactive_anon_bytes, Inactive_bytes, Inactive_file_bytes)
Purpose: Track memory not recently used (candidates for eviction by the kernel).

How it Works:

The kernel divides memory into active (frequently used) and inactive (rarely used).

### Inactive_anon_bytes: Anonymous (non-file-backed) pages (e.g., heap, stack).

Value: 1.4729216e+08 (~147 MB).

High values suggest unused application memory (may be swapped out).

### Inactive_file_bytes: File-backed pages (e.g., cached files).

Value: 7.32471296e+08 (~732 MB).

Can be safely reclaimed if needed (reloaded from disk later).

### Inactive_bytes: Total inactive memory (Inactive_anon + Inactive_file).

Value: 8.79763456e+08 (~879 MB).

Tuning:

vfs_cache_pressure (in /proc/sys/vm/) adjusts reclaim priority for file-backed pages.

High inactive memory is normal (Linux aggressively caches files).

## node_memory_KernelStack_bytes
Definition: Memory used by kernel stacks for each thread/process.

Value: 2.932736e+06 (~2.93 MB).

How it Works:

Every thread in the system gets a small kernel stack (usually 8–16 KB).

Used for system calls, interrupts, and kernel-mode execution.

Why it Matters:

High values indicate many threads (e.g., containers, Java apps).

Kernel stacks are non-swappable, so they consume physical RAM.

## node_memory_Mapped_bytes
Definition: Memory mapped into user-space processes (e.g., mmap'd files, shared libraries).

Value: 2.20553216e+08 (~220.5 MB).

How it Works:

Includes files mapped into memory (/proc/<pid>/maps).

Shared between processes (e.g., libc.so).

Why it Matters:

High values suggest heavy file I/O or shared memory usage (e.g., databases).

## node_memory_MemAvailable_bytes
Definition: Estimate of memory available for new workloads (without swapping).

Value: 1.5770914816e+10 (~15.77 GB).

How it Works:

Calculated as:

MemFree + (Cached + Buffers) + (SReclaimable) - (Unreclaimable slabs)  
More accurate than MemFree (includes reclaimable caches).

Why it Matters:

Key metric for real memory pressure.

If low, the system may start swapping or killing processes (OOM).

## node_memory_MemFree_bytes
Definition: Raw free memory (unused RAM).

Value: 1.4826561536e+10 (~14.83 GB).

How it Works:

Does not account for caches/buffers that can be reclaimed.

Why it Matters:

Less useful than MemAvailable (Linux aggressively uses free RAM for caching).

## node_memory_Mlocked_bytes
Definition: Memory locked by processes (cannot be swapped/paged out).

Value: 0 (no locked memory).

How it Works:

Used by mlock()/mlockall() syscalls (e.g., databases, real-time apps).

Why it Matters:

Excessive locking can starve the system of free memory.

## node_memory_NFS_Unstable_bytes
Definition: Memory holding NFS writes not yet committed to disk.

Value: 0 (no NFS instability).

How it Works:

NFS client caches writes temporarily (similar to Dirty_bytes but for NFS).

Why it Matters:

Non-zero values indicate pending NFS writes (risk of data loss on crash).

## node_memory_PageTables_bytes
Definition: Memory used for page tables (virtual-to-physical address mappings).

Value: 4.087808e+06 (~4.1 MB).

How it Works:

Each process has its own page tables (managed by the kernel).

Grows with the number of memory mappings.

Why it Matters:

High values occur with many processes or large address spaces (e.g., VMs).

## node_memory_Percpu_bytes
Definition: Memory used for per-CPU kernel data structures.

Value: 2.162688e+06 (~2.16 MB).

How it Works:

Kernel allocates per-CPU copies of data to avoid locking (e.g., network stats).

Why it Matters:

Scales with CPU cores (usually negligible unless extreme).

## node_memory_SReclaimable_bytes
Definition: Reclaimable slab memory (kernel object caches that can be freed).

Value: 5.834752e+07 (~58.3 MB).

How it Works:

Slabs cache kernel objects (e.g., inode_cache, dentry).

SReclaimable can be freed under memory pressure.

Why it Matters:

Part of MemAvailable—high values mean more reclaimable memory.

## node_memory_SUnreclaim_bytes
Definition: Unreclaimable slab memory (kernel objects pinned in RAM).

Value: 6.4274432e+07 (~64.3 MB).

How it Works:

Includes critical kernel structures (e.g., vm_area_struct).

Why it Matters:

High values may indicate kernel memory leaks (check slabtop).

## node_memory_ShmemHugePages_bytes
Definition: Shared memory allocated in HugePages.

Value: 0 (no shared HugePages).

How it Works:

Used for shared memory (e.g., tmpfs, IPC) with HugePages enabled.

Why it Matters:

HugePages improve performance for shared memory workloads.

## node_memory_ShmemPmdMapped_bytes
Definition: Shared memory mapped with PMD (Page Middle Directory) huge pages.

Value: 0 (no PMD-mapped shared memory).

How it Works:

PMD entries map 2MB huge pages (faster TLB lookups).

Why it Matters:

Non-zero values indicate optimized shared memory access.

## node_memory_Shmem_bytes
Definition: Total shared memory (e.g., tmpfs, shared IPC segments).

Value: 1.0391552e+07 (~10.4 MB).

How it Works:

Includes /dev/shm, tmpfs mounts, and shmget() allocations.

Why it Matters:

High usage can exhaust memory (shared memory is not swappable).
