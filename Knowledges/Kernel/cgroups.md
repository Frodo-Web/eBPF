# Cgroups
Get cgroup tree
```
systemd-cgls
..
Control group /:
-.slice
├─user.slice (#1194)
│ → user.invocation_id: 83976197f66c45a3bc05d00b064145d0
│ → trusted.invocation_id: 83976197f66c45a3bc05d00b064145d0
│ └─user-1000.slice (#6519)
│   → user.invocation_id: 6ddaf4e1ba8241a78745ec247dad66db
│   → trusted.invocation_id: 6ddaf4e1ba8241a78745ec247dad66db
│   ├─session-9.scope (#7152)
│   │ ├─7130 sshd: frodo [priv]
│   │ ├─7134 sshd: frodo@pts/2
│   │ ├─7135 -bash
│   │ ├─7166 sudo su -
│   │ ├─7168 su -
│   │ ├─7169 -bash
│   │ ├─7375 systemd-cgls
│   │ └─7376 less
│   ├─user@1000.service … (#6597)
│   │ → user.invocation_id: d72655f624534f8bbb69911bd96183e7
│   │ → user.delegate: 1
│   │ → trusted.invocation_id: d72655f624534f8bbb69911bd96183e7
│   │ → trusted.delegate: 1
│   │ └─init.scope (#6636)
│   │   ├─6775 /usr/lib/systemd/systemd --user
│   │   └─6777 (sd-pam)
│   ├─session-6.scope (#6792)
│   │ ├─6770 sshd: frodo [priv]
│   │ ├─6784 sshd: frodo@pts/0
│   │ ├─6785 -bash
```
cgroup id is just inode # in cgroupfs so one workaround could look like this:
```
find /sys/fs/cgroup -inum 7152
..
/sys/fs/cgroup/user.slice/user-1000.slice/session-9.scope
```
