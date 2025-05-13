# Build nginx
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
  [25] .debug_aranges    PROGBITS         0000000000000000  00814c74
  [26] .debug_info       PROGBITS         0000000000000000  00816f14
  [27] .debug_abbrev     PROGBITS         0000000000000000  00b1c986
  [28] .debug_line       PROGBITS         0000000000000000  00b42b37
  [29] .debug_str        PROGBITS         0000000000000000  00bc1dba
  [30] .debug_line_str   PROGBITS         0000000000000000  00be3260
  [31] .debug_rnglists   PROGBITS         0000000000000000  00be541e
```
