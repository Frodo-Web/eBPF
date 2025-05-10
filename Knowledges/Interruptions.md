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
