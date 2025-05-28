# Kernel requirements for eBPF programs
```
# Old kernels
/sys/kernel/btf/vmlinux
bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h

? BPF_CORE_READ=y
CONFIG_BPF=y
CONFIG_BPF_SYSCALL=y
CONFIG_BPF_EVENTS=y,
CONFIG_BPF_JIT=y
CONFIG_HAVE_EBPF_JIT=y

# For LSM support
? CONFIG_BPF_LSM=y
cat /sys/kernel/security/lsm
capability,lockdown,landlock,yama,apparmor,bpf

CONFIG_DEBUG_INFO=y
CONFIG_DEBUG_INFO_BTF=y
CONFIG_SECURITY=y
CONFIG_SECURITYFS=y
CONFIG_SECURITY_NETWORK=y
CONFIG_FUNCTION_TRACER=y
CONFIG_FTRACE_SYSCALLS=y

GRUB_CMDLINE_LINUX="lsm=[YOUR CURRENTLY ENABLED LSMs],bpf"
grub-mkconfig -o /boot/grub/grub.cfg
```
