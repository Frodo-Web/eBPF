# Virtualization and I/O
Flow: 

1. Guest OS Layer (Filesystem, Device mapper, block layer)

- Filesystems (ext4, xfs, ...)
- Device mapper (md, lvm)
- Block layer (blk_insert, blk_issue, blk_complete)
- Cgroups / cgroup limits (CPU, IOPS, etc.)

2. Hyper Visor/Virtualization Layer.

The hypervisor (e.g., KVM/QEMU, VMware ESXi, Hyper-V) emulates the block device:

- Virtio-blk or SCSI (KVM/QEMU)
- PV (Paravirtualized) drivers (Xen)
- VMware Tools (vSphere/ESXi)

Hypervisor schedules I/Os to the host-level storage stack.

3. Host OS Layer (if using Type-2 hypervisor or nested VMs)
  
If your VM runs on a host OS (like Linux with KVM), then the host handles I/O scheduling.

May include:

- Host filesystem (e.g., ext4)
- Host block layer
- Cgroups / cgroup limits (CPU, IOPS, etc.)

4. Storage Backend (Physical/NFS/iSCSI/vSAN)
- Local disk (NVMe/SATA/SAS)
- SAN (Fibre Channel, iSCSI)
- NAS (NFS)
- Distributed storage (Ceph, vSAN, GlusterFS)

Latency can be caused by:

- Disk saturation
- Network congestion (for remote storage)
- Storage controller bottlenecks
- Thin provisioning overcommit
