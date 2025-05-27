# SNMP
Simple Network Management Protocol (SNMP) is an Internet Standard protocol for collecting and organizing information about managed devices on IP networks and for modifying that information to change device behavior.
## What Are SNMP Counters?
```
[2320864.954447] TCP: Possible SYN flooding on port 7001. Dropping request. Check
SNMP counters.
```
https://docs.kernel.org/networking/snmp_counter.html

SNMP counters are numeric values maintained by the Simple Network Management Protocol (SNMP) that track various network and system events, such as:
- Number of packets received or transmitted
- Errors in packet transmission
- Connection attempts
- Retransmissions
- TCP/UDP statistics
These counters are stored in a hierarchical structure called the Management Information Base (MIB) and can be queried using tools like snmpwalk, snmpget, or via monitoring systems like Zabbix , Cacti , or Prometheus + snmp_exporter .
### 🧪 How to Check SNMP Counters
On Linux, SNMP counters are exposed in /proc/net/snmp and /proc/net/netstat.
```
cat /proc/net/snmp | grep Tcp
..
Tcp: InSegs OutSegs InErrs OutRsts
Tcp: 123456   98765   12      34
```
### 🛠️ Using SNMP Tools to Monitor Remotely
```
snmpwalk -v 2c -c public your.server.ip TCP-MIB::tcpConnTable
```
