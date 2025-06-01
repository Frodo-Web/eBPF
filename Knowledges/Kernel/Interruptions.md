# IRQ, SOFTIRQ

## IRQ:
Hardware-triggered interrupts sent by devices (e.g., network card, disk, keyboard) to notify the CPU of an event.

High priority – The CPU stops what it's doing to handle them immediately.

Handled by the kernel’s interrupt handler.

### Examples:
A network card receives a packet.

A disk finishes a read/write operation.

A key is pressed on the keyboard.

### High irq time may indicate:

Heavy network traffic (NIC generating many interrupts).

Faulty hardware (spurious interrupts).

Misconfigured IRQ affinity (CPU core overloaded with interrupts).


### /proc/interrupts

| IRQ#/Type    | CPU0    | CPU1   | CPU2   | CPU3     | Description                          |
|--------------|---------|--------|--------|----------|--------------------------------------|
| 0            | 31      | 0      | 0      | 0        | IR-IO-APIC 2-edge timer              |
| 8            | 0       | 0      | 0      | 1        | IR-IO-APIC 8-edge rtc0               |
| 9            | 0       | 1126   | 0      | 0        | IR-IO-APIC 9-fasteoi acpi            |
| 18           | 16      | 0      | 0      | 0        | IR-IO-APIC 18-fasteoi i801_smbus     |
| 20           | 0       | 29     | 0      | 0        | IR-IO-APIC 20-fasteoi ehci_hcd:usb4  |
| 23           | 29      | 0      | 0      | 0        | IR-IO-APIC 23-fasteoi ehci_hcd:usb2  |
| 24           | 0       | 0      | 0      | 0        | IR-PCI-MSI-0000:00:01.0 PCIe bwctrl  |
| 25           | 0       | 0      | 0      | 0        | IR-PCI-MSI-0000:00:1c.0 PCIe bwctrl  |
| 26           | 1       | 0      | 0      | 0        | IR-PCI-MSI-0000:00:1c.2 PCIe bwctrl  |
| 27           | 0       | 1      | 0      | 0        | IR-PCI-MSI-0000:00:1c.3 PCIe bwctrl  |
| 28           | 0       | 0      | 0      | 0        | IR-PCI-MSI-0000:00:14.0 xhci_hcd     |
| 33           | 0       | 0      | 0      | 148521   | IR-PCI-MSIX-0000:03:00.0 enp3s0 (NIC)|
| 34           | 0       | 0      | 16215  | 0        | IR-PCI-MSI-0000:00:1f.2 ahci (SATA)  |
| 35           | 0       | 0      | 0      | 31       | IR-PCI-MSI-0000:00:16.0 mei_me       |
| 36           | 0       | 4511   | 0      | 0        | IR-PCI-MSI-0000:00:02.0 i915 (GPU)   |
| 37           | 0       | 0      | 422    | 0        | IR-PCI-MSI-0000:00:1b.0 snd_hda_intel|
| **NMI**      | 2       | 1      | 1      | 3        | Non-maskable interrupts              |
| **LOC**      | 240354  | 244152 | 214633 | 493950   | Local timer interrupts               |
| **SPU**      | 0       | 0      | 0      | 0        | Spurious interrupts                  |
| **PMI**      | 2       | 1      | 1      | 3        | Performance monitoring interrupts    |
| **IWI**      | 18      | 16     | 0      | 0        | IRQ work interrupts                  |
| **RTR**      | 0       | 0      | 0      | 0        | APIC ICR read retries                |
| **RES**      | 1221    | 1150   | 966    | 1400     | Rescheduling interrupts              |
| **CAL**      | 22959   | 18812  | 24699  | 13982    | Function call interrupts             |
| **TLB**      | 886     | 975    | 1084   | 934      | TLB shootdowns                       |
| **TRM**      | 0       | 0      | 0      | 0        | Thermal event interrupts             |
| **THR**      | 0       | 0      | 0      | 0        | Threshold APIC interrupts            |
| **DFR**      | 0       | 0      | 0      | 0        | Deferred Error APIC interrupts       |
| **MCE**      | 0       | 0      | 0      | 0        | Machine check exceptions             |
| **MCP**      | 35      | 36     | 36     | 36       | Machine check polls                  |
| **ERR**      | 0       | -      | -      | -        | Errors                               |
| **MIS**      | 0       | -      | -      | -        | Miscellaneous                        |
| **PIN**      | 0       | 0      | 0      | 0        | Posted-interrupt notification        |
| **NPI**      | 0       | 0      | 0      | 0        | Nested posted-interrupt event        |
| **PIW**      | 0       | 0      | 0      | 0        | Posted-interrupt wakeup event        |

1. NMI (Non-Maskable Interrupts)
What it is: Highest-priority interrupts that cannot be ignored by the CPU (even if interrupts are disabled).

Causes:

Hardware failures (e.g., memory corruption, power issues).

Kernel panics or watchdog timeouts.

Your data: Low counts (2|1|1|3) are normal (likely watchdog timers).

2. LOC (Local Timer Interrupts)
What it is: Interrupts from the CPU’s local APIC timer, used for task scheduling and timekeeping.

Why high?: Scales with uptime and CPU usage. Your values (240K–493K) are normal for a running system.

3. SPU (Spurious Interrupts)
What it is: "Ghost" interrupts triggered by electrical noise or hardware glitches.

Your data: 0 is ideal (no hardware issues).

4. PMI (Performance Monitoring Interrupts)
What it is: Triggered by CPU performance counters (e.g., cache misses, branch mispredictions).

Your data: Low counts (2|1|1|3) suggest minor profiling (e.g., perf or kernel optimizations).

5. IWI (IRQ Work Interrupts)
What it is: Deferred work from hardware IRQs (e.g., re-enabling devices after interrupts).

Your data: 18|16|0|0 suggests CPU0/1 handled recent IRQ cleanup tasks.

6. RTR (APIC ICR Read Retries)
What it is: Retries when the CPU reads the APIC Interrupt Command Register (ICR).

Your data: 0 means no APIC communication issues.

7. RES (Rescheduling Interrupts)
What it is: Requests to switch tasks (triggered by scheduler or sched_yield()).

Your data: 1221|1150|966|1400 indicates moderate context switching (normal for multitasking).

8. CAL (Function Call Interrupts)
What it is: Interrupts for kernel function calls (e.g., system calls).

Your data: High counts (18K–24K) are normal for active processes.

9. TLB (TLB Shootdowns)
What it is: Synchronizes Translation Lookaside Buffers (TLBs) across CPUs when memory mappings change.

Your data: 886|975|1084|934 suggests moderate memory pressure (e.g., process startups/exits).

10. TRM (Thermal Event Interrupts)
What it is: Triggered when CPU temperature exceeds thresholds.

Your data: 0 means no thermal throttling.

11. THR (Threshold APIC Interrupts)
What it is: APIC-specific interrupts for power/thermal thresholds.

Your data: 0 (typical unless using advanced power features).

12. DFR (Deferred Error APIC Interrupts)
What it is: Handles correctable CPU errors (e.g., ECC memory fixes).

Your data: 0 (no corrected errors detected).

13. MCE (Machine Check Exceptions)
What it is: Fatal hardware errors (e.g., CPU cache corruption).

Your data: 0 is good (no critical failures).

14. MCP (Machine Check Polls)
What it is: Kernel checks for pending MCEs.

Your data: 35|36|36|36 (normal background checks).

15. ERR/MIS (Errors/Miscellaneous)
What it is: Catch-all for unclassified interrupts/errors.

Your data: 0 (no anomalies).

16. PIN/NPI/PIW (Posted Interrupts)
What it is: Virtualization-related interrupts for CPU wakeups/notifications.

Your data: 0 (no active VM workloads).

## SOFTIRQ:

Deferred interrupt processing – Used to handle less urgent tasks after hardware interrupts.

Lower priority than irq – Runs after hardware interrupts or during kernel scheduling.

Can be interrupted by irq but not by normal processes.

### Examples:
Network packet processing (NET_RX, NET_TX).

Timer interrupts (TIMER).

Block device operations (disk I/O scheduling).

### High softirq time may indicate:

High network traffic (packet processing).

Kernel bottlenecks (too many timers or deferred tasks).

CPU contention (if softirq is starving normal processes).

### /proc/softirqs

| SoftIRQ Type | CPU0   | CPU1   | CPU2   | CPU3     |
|--------------|--------|--------|--------|----------|
| HI           | 0      | 94     | 2      | 0        |
| TIMER        | 36469  | 31409  | 31211  | 38943    |
| NET_TX       | 0      | 4      | 1      | 162      |
| NET_RX       | 449    | 431    | 384    | 356474   |
| BLOCK        | 49     | 2      | 16214  | 22       |
| IRQ_POLL     | 0      | 0      | 0      | 0        |
| TASKLET      | 46     | 1169   | 24     | 1220     |
| SCHED        | 54649  | 51761  | 46302  | 61280    |
| HRTIMER      | 0      | 0      | 0      | 789      |
| RCU          | 14711  | 13032  | 14441  | 13414    |

1. HI (High-Priority Tasklets)
Purpose: Executes high-priority deferred tasks (rarely used in modern kernels).

Typical triggers: Urgent bottom-half processing from hardware interrupts.

Your data:

CPU1=94, others near 0 → Likely a few high-priority kernel tasks ran on CPU1.

2. TIMER (Timer Interrupts)
Purpose: Handles kernel timers (e.g., scheduling timeouts, periodic tasks).

Impact: High frequency but usually low overhead.

Your data:

CPU0=36K, CPU3=38K → Normal for systems with many timers (e.g., TCP keepalives, cron jobs).

3. NET_TX (Network Transmission)
Purpose: Processes outbound network packets (packet scheduling, DMA completion).

Impact: Increases with network traffic.

Your data:

CPU3=162 → Indicates moderate outbound traffic (e.g., web server responses).

4. NET_RX (Network Reception)
Purpose: Handles inbound network packets (packet filtering, protocol stacks).

Impact: Often the most CPU-intensive SoftIRQ under network load.

Your data:

CPU3=356,474 → Bottleneck detected! CPU3 is drowning in packets (likely NIC IRQ affinity issue).

Fix: Balance interrupts with irqbalance or bind NIC IRQs to multiple cores.

5. BLOCK (Block Device I/O)
Purpose: Completes disk I/O operations (e.g., page cache updates, filesystem tasks).

Impact: High during disk-heavy workloads (database, backups).

Your data:

CPU2=16,214 → Heavy disk I/O (matches ahci IRQs in your /proc/interrupts).

6. IRQ_POLL (IRQ Polling)
Purpose: Kernel’s polling mode for low-latency devices (rarely used).

Your data: 0 → Default (interrupt-driven I/O is active).

7. TASKLET (Regular Tasklets)
Purpose: General-purpose deferred work (legacy alternative to workqueues).

Impact: Can cause latency if overloaded.

Your data:

CPU1=1,169, CPU3=1,220 → May indicate kernel drivers using tasklets (e.g., older NIC drivers).

8. SCHED (Scheduler)
Purpose: Handles thread scheduling (load balancing, CPU migration).

Impact: Scales with process count/context switches.

Your data:

CPU0=54K, CPU3=61K → Expected for multi-core systems running many threads.

9. HRTIMER (High-Resolution Timers)
Purpose: Precision timers for nanosecond-level tasks (e.g., media playback).

Your data:

CPU3=789 → Likely used by a userspace or kernel service (e.g., audio/video).

10. RCU (Read-Copy-Update)
Purpose: Synchronization mechanism for lock-free kernel data structures.

Impact: Overhead scales with CPU cores/kernel threads.

Your data:

CPU0=14K, CPU3=13K → Normal for Linux kernels ≥4.x.
