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
