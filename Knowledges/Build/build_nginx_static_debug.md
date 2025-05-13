# Build nginx statically
Build the bin using Dockerfile
```
# Use a builder image with all the necessary tools
FROM ubuntu:24.04 AS builder

RUN apt update && \
    apt install -y build-essential wget libpcre3-dev libssl-dev git

# Set NGINX version
ENV NGINX_VERSION=1.28.0

# Download NGINX source
RUN wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz && \
    tar zxvf nginx-${NGINX_VERSION}.tar.gz

# Download zlib source
RUN cd /usr/src && rm -rf zlib && \
    wget https://zlib.net/zlib-1.3.1.tar.gz  && \
    tar zxvf zlib-1.3.1.tar.gz && \
    mv zlib-1.3.1 zlib

WORKDIR /nginx-${NGINX_VERSION}

# Configure NGINX with debug info and force static linking
RUN CC="gcc -static" \
    CFLAGS="-static -g" \
    LDFLAGS="-static" \
    ./configure \
    --prefix=/usr/local/nginx \
    --with-http_ssl_module \
    --with-debug \
    --with-cc-opt="-g -static" \
    --with-ld-opt="-static" \
    --with-http_stub_status_module \
    --with-http_realip_module \
    --with-http_gzip_static_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_v2_module \
    --with-http_addition_module \
    --with-http_gunzip_module \
    --with-http_random_index_module \
    --with-http_secure_link_module \
    --with-http_degradation_module \
    --with-http_slice_module \
    --with-mail \
    --with-mail_ssl_module \
    --with-stream \
    --with-stream_ssl_module \
    --with-stream_realip_module \
    --with-stream_ssl_preread_module \
    --with-compat \
    --with-pcre \
    --with-zlib=/usr/src/zlib

# Build NGINX
RUN make -j$(nproc)

# Final stage — copy only the binary
FROM scratch AS final

# Re-define NGINX_VERSION so we can reference it
ENV NGINX_VERSION=1.28.0

# Copy the built binary from the builder
COPY --from=builder /nginx-${NGINX_VERSION}/objs/nginx /nginx
```
Just run the container to get overlayfs with the bin mounted
```
docker run --name nginx_copy nginx-static-debug /bin/bash
..
error (no bash, since we use from scratch. Anyway overlay fs wil be mounted)
```
Copy the binary
```
docker cp nginx_copy:/nginx ./nginx-static-debug
..
Successfully copied 13.5MB to /opt/nginx/nginx-static-debug
```
We should see, it is statically linked and with debug_info
```
file ./nginx-static-debug
./nginx-static-debug: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, BuildID[sha1]=dd8445ca33652146291ea6851f1a2db5aad210f2, for GNU/Linux 3.2.0, with debug_info, not stripped

```
Also, ldd will prove that
```
ldd ./nginx-static-debug
..
not a dynamic executable
```
We should see .debug_info, .debug_abbrev
```
readelf -S ./nginx-static-debug | grep .debug
..
  [25] .debug_aranges    PROGBITS         0000000000000000  00814c74
  [26] .debug_info       PROGBITS         0000000000000000  00816f14
  [27] .debug_abbrev     PROGBITS         0000000000000000  00b1c986
  [28] .debug_line       PROGBITS         0000000000000000  00b42b37
  [29] .debug_str        PROGBITS         0000000000000000  00bc1dba
  [30] .debug_line_str   PROGBITS         0000000000000000  00be3260
  [31] .debug_rnglists   PROGBITS         0000000000000000  00be541e
```
# Prepare nginx
Create custom environment
```
sudo mkdir -p /opt/nginx/{etc,log,logs,sbin}
sudo cp ./nginx-static-debug /opt/nginx/sbin/nginx
sudo vim /opt/nginx/etc/nginx.conf
sudo mkdir -p /opt/nginx/html
echo "Hello from NGINX static build!" | sudo tee /opt/nginx/html/index.html
sudo curl -L -o /opt/nginx/etc/mime.types https://raw.githubusercontent.com/nginx/nginx/master/conf/mime.types
sudo chown nginx:nginx -R /opt/nginx
```
Run nginx (WARNING: Not as root!)
```
/opt/nginx/sbin/nginx -p /opt/nginx -c /opt/nginx/etc/nginx.conf
```
### Problems I encountered
After I builded and runned user as root I got an error
```
sudo /opt/nginx/sbin/nginx -p /opt/nginx -c /opt/nginx/etc/nginx.conf
..
Floating point exception
```
Open it with gdb
```
sudo gdb /opt/nginx/sbin/nginx
```
Start nginx and pass the arguments
```
(gdb) run -p /opt/nginx -c /opt/nginx/etc/nginx.conf
```
Lets see...
```
Starting program: /opt/nginx/sbin/nginx -p /opt/nginx -c /opt/nginx/etc/nginx.conf
warning: File "/usr/lib64/libthread_db.so.1" auto-loading has been declined by your `auto-load safe-path' set to "$debugdir:$datadir/auto-load:/usr/lib/golang/src/pkg/runtime/runtime-gdb.py".
To enable execution of this file add
        add-auto-load-safe-path /usr/lib64/libthread_db.so.1
line to your configuration file "/root/.config/gdb/gdbinit".
To completely disable this security protection add
        set auto-load safe-path /
line to your configuration file "/root/.config/gdb/gdbinit".
For more information about this security protection see the
"Auto-loading safe path" section in the GDB manual.  E.g., run from the shell:
        info "(gdb)Auto-loading safe path"
warning: Unable to find libthread_db matching inferior's thread library, thread debugging will not be available.

Program received signal SIGFPE, Arithmetic exception.
0x00007ffff7d56789 in __libc_early_init () from /lib64/libc.so.6
Missing separate debuginfos, use: dnf debuginfo-install glibc-2.34-125.el9_5.8.x86_64 sssd-client-2.9.5-4.el9_5.4.x86_64
```
After we get the SIGFPE signal (Arithmetic exception, such as divison by zero), enter 'bt'
```
(gdb) bt
#0  0x00007ffff7d56789 in __libc_early_init () from /lib64/libc.so.6
#1  0x00000000009b2ae7 in dl_open_worker_begin ()
#2  0x00000000009aa569 in _dl_catch_exception ()
#3  0x00000000009b1d0f in dl_open_worker ()
#4  0x00000000009aa569 in _dl_catch_exception ()
#5  0x00000000009b20b2 in _dl_open ()
#6  0x0000000000a0360a in do_dlopen ()
#7  0x00000000009aa569 in _dl_catch_exception ()
#8  0x00000000009aa619 in _dl_catch_error ()
#9  0x0000000000a03a5e in __libc_dlopen_mode ()
#10 0x00000000009fef9f in module_load ()
#11 0x00000000009ff3c5 in __nss_module_get_function ()
#12 0x00000000009ff56b in __nss_lookup ()
#13 0x00000000009a43f8 in getpwnam_r ()
#14 0x00000000009a42a8 in getpwnam ()
#15 0x0000000000404f52 in ngx_core_module_init_conf (cycle=0xc55a30, conf=0xc57ac0) at src/core/nginx.c:1193
#16 0x0000000000425760 in ngx_init_cycle (old_cycle=0x7fffffffe280) at src/core/ngx_cycle.c:303
#17 0x00000000004030e6 in main (argc=5, argv=0x7fffffffe628) at src/core/nginx.c:293
```
We see, the problem happened in libc.so.6
Nginx tries to initilize the config, calls getpwnam()  -  which resolves a username into a UID
```
#10 0x00000000009fef9f in module_load ()
#11 0x00000000009ff3c5 in __nss_module_get_function ()
#12 0x00000000009ff56b in __nss_lookup ()
#13 0x00000000009a43f8 in getpwnam_r ()
#14 0x00000000009a42a8 in getpwnam ()
#15 0x0000000000404f52 in ngx_core_module_init_conf (cycle=0xc55a30, conf=0xc57ac0) at src/core/nginx.c:1193
```
getpwnam() passes the user name as argument and returns structure
```
           struct passwd {
               char   *pw_name;       /* username */
               char   *pw_passwd;     /* user password */
               uid_t   pw_uid;        /* user ID */
               gid_t   pw_gid;        /* group ID */
               char   *pw_gecos;      /* user information */
               char   *pw_dir;        /* home directory */
               char   *pw_shell;      /* shell program */
           };
```
And __nss_ functions are name service switch functions which try to drop privilegies, and not working correctly when statically linked.

People say, musl could work better in this case, instead of libc.

The explanation was:
```
When you run NGINX as root, it tries to drop privileges by switching to the user defined in the config (user nobody;). But:

In a fully static binary , dynamic NSS (Name Service Switch) functions like getpwnam() may fail silently or cause crashes.
These failures can manifest as seemingly unrelated errors — like floating-point exceptions , even though no actual math is involved.
The crash happens because glibc's internal NSS code, which NGINX indirectly calls via getpwnam(), contains operations that behave incorrectly when statically linked — especially under certain optimization or CPU feature assumptions.
```
