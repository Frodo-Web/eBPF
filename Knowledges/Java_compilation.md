# Java compilation
```shell
bash configure --with-jvm-variants=server --enable-debug --enable-headless-only \
 --enable-warnings-as-errors --enable-dtrace --enable-jvm-feature-dtrace --with-num-cores=4 \
 --with-memory-size=12288 --with-boot-jdk=/opt/java24/jdk-24.0.1 \
 --with-extra-cflags="-march=native -O3 -g -g3 -ggdb -fPIC" --with-extra-cxxflags="-march=native \
 -O3 -g -g3 -ggdb -fPIC" --with-extra-ldflags="-g -Wl,--gc-sections" --enable-javac-server
```
