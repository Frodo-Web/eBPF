## Examples
```
SEC("uprobe//bin/bash:readline")
int handle_malloc(struct pt_regs *ctx)
{
    u64 pid_tgid = bpf_get_current_pid_tgid();
    u64 uid_gid = bpf_get_current_uid_gid();
    u64 cgroup_id = bpf_get_current_cgroup_id();
    char comm[16];

    bpf_get_current_comm(comm, sizeof(comm));

    bpf_printk("PID: %d, UID: %d, COMM: %s, CGROUP: %llx\n",
               pid_tgid, uid_gid, comm, cgroup_id);

    return 0;
}
```
