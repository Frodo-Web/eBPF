# Program and shared libraries at user space
## Shared libraries are not shared when they statically linked
## 📚 Shared libraries
libc.so.6, libpthread.so.0, and libm.so.6 are shared libraries provided by glibc (GNU C library).
| Library | Purpose | Example Functions | Description of Functions | Languages That Use It |
|--------|---------|-------------------|----------------------------|------------------------|
| `libc.so.6` | Core C library providing essential system calls and basic functions | `malloc`, `free`, `fopen`, `read`, `write`, `strcpy`, `strlen` | Memory allocation, file I/O, string manipulation, process control | All languages (C/C++, Python, Java, Go, Rust, etc.) via runtime or FFI |
| `libpthread.so.0` | POSIX threads for concurrent execution | `pthread_create`, `pthread_join`, `pthread_mutex_lock` | Create threads, manage synchronization, avoid race conditions | Python (`threading`), Java (`Thread`), Node.js, Go (goroutines), Rust |
| `libm.so.6` | Mathematical operations | `sin`, `cos`, `sqrt`, `log`, `exp` | Trigonometric, logarithmic, exponential math functions | Python (NumPy), R, MATLAB, Java, C/C++, Fortran |
| `ld-linux.so.2` / `ld-linux-x86-64.so.2` | Dynamic linker/loader | N/A | Loads shared libraries and resolves symbols at runtime | All dynamically linked programs |
| `libdl.so.2` | Dynamic loading of shared libraries | `dlopen`, `dlsym`, `dlclose` | Load `.so` files at runtime, call functions dynamically | Python (`ctypes`), Java (`JNI`), Lua, Ruby, C/C++ |
| `libX11.so.6` | X Window System client interface | `XOpenDisplay`, `XCreateWindow`, `XDrawLine` | GUI drawing, window management on X11 systems | GTK apps, Qt apps, Java AWT/Swing, Python (Tkinter) |
| `libGL.so.1` | OpenGL rendering | `glClear`, `glBegin`, `glVertex3f`, `glColor3f` | 2D/3D graphics rendering | Games, Unity, Blender, Java (LWJGL), Python (PyOpenGL) |
| `libgtk-3.so.0` | GTK+ GUI toolkit | `gtk_window_new`, `gtk_button_new`, `g_signal_connect` | Create buttons, windows, handle events in GUIs | GNOME apps, Python (GTK bindings), Vala |
| `libQt5Core.so.5` | Qt framework core | `QApplication`, `QString`, `QObject`, `QSignalMapper` | UI components, signals/slots, file handling | KDE apps, Qt-based software, Python (PyQt) |
| `libasound.so.2` | ALSA sound API | `snd_pcm_open`, `snd_pcm_writei` | Audio playback/recording using ALSA drivers | Multimedia apps, games, Python (alsaaudio), C/C++ |
| `libpulse.so.0` | PulseAudio sound server | `pa_simple_new`, `pa_simple_play` | Stream audio through PulseAudio | Media players, VoIP clients, Python, C/C++ |
| `libavcodec.so.58` | FFmpeg codec library | `avcodec_encode_video2`, `av_read_frame` | Encode/decode video/audio streams | FFmpeg tools, VLC, Python (ffmpeg-python), C/C++ |
| `libv4l2.so.0` | Video4Linux2 interface | `v4l2_ioctl`, `v4l2_open` | Capture from webcams, TV tuners | Webcam apps, OpenCV, Python (cv2), C/C++ |
| `libpython3.x.so` | Python interpreter library | `Py_Initialize`, `PyRun_SimpleString`, `PyObject_CallObject` | Embed Python, run scripts, call Python objects | Embedded Python, C extensions |
| `libjvm.so` | Java Virtual Machine | `JNI_CreateJavaVM`, `CallStaticVoidMethod` | Start JVM, invoke Java methods from native code | Java applications, JNI, embedded Java |
| `libnode.so` | Node.js engine | `node::Start`, `v8::Isolate`, `v8::HandleScope` | Run JavaScript, manage V8 context | Node.js apps, native addons |
| `libgo.so` | Go runtime with CGO enabled | `runtime.main`, `C.CString`, `C.malloc` | Interact with C libraries, dynamic linking | Go apps with CGO |
| `libstd-*.so` | Rust standard library | `Vec::new`, `println!`, `HashMap` | Memory safety, collections, concurrency primitives | Rust binaries compiled dynamically |
| `libssl.so` | OpenSSL cryptographic functions | `SSL_CTX_new`, `SSL_connect`, `EVP_EncryptInit` | TLS/SSL encryption, hashing, symmetric/asymmetric crypto | Python (`ssl`), Java (`JSSE`), C/C++, Node.js |
| `libcurl.so` | URL transfer library | `curl_easy_init`, `curl_easy_setopt`, `curl_easy_perform` | HTTP, FTP, SMTP requests | Python (`requests`), PHP, C/C++, Node.js |
| `libsqlite3.so` | SQLite database engine | `sqlite3_open`, `sqlite3_exec`, `sqlite3_prepare_v2` | Query, insert, update data in local SQL DB | Python (`sqlite3`), Java (SQLite JDBC), C/C++, Rust |
| `libffi.so` | Foreign Function Interface | `ffi_call`, `ffi_prep_cif` | Call functions in other languages dynamically | Python (`cffi`), GObject introspection, Scheme, LuaJIT |

## uprobes and shared libraries
This attaches to every malloc() call executed by any application that uses libc.so.6. 
```
SEC("uprobe/libc.so.6:malloc")
```
This only works for dynamically linked binaries that use libc.so.6. If the program is statically linked to its own libc, it won't work until you specify the program itself.

This works because the Linux kernel’s uprobe mechanism can resolve sonames (shared object names), like libc.so.6, based on where they’re mapped in memory, so you don't need to specify full path.
## Program Languages and shared libraries
### Python
ldd - print shared object dependencies
```
ldd /usr/bin/python3
..
        linux-vdso.so.1 (0x00007ffd1a0ed000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f6dcde7a000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f6dcde5e000)
        libexpat.so.1 => /lib/x86_64-linux-gnu/libexpat.so.1 (0x00007f6dcde32000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f6dcdc20000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f6dcdf6a000)
```
#### malloc example
Python uses different malloc call, which is like a wrap over libc maloc, you can see this
```
nm -D /lib/x86_64-linux-gnu/libc.so.6 | grep malloc
..
00000000000ad650 T __libc_malloc@@GLIBC_2.2.5
000000000020a140 V __malloc_hook@GLIBC_2.2.5
000000000020a160 B __malloc_initialize_hook@GLIBC_2.2.5
00000000000ad650 T malloc@@GLIBC_2.2.5
00000000000af4c0 W malloc_info@@GLIBC_2.10
00000000000af050 W malloc_stats@@GLIBC_2.2.5
00000000000aeba0 W malloc_trim@@GLIBC_2.2.5
00000000000aee70 W malloc_usable_size@@GLIBC_2.2.5

nm -D /usr/bin/python3 | grep malloc
..
00000000004f960d T PyInit__tracemalloc
                 U malloc@GLIBC_2.2.5
```
This tells perf to attach a user-space probe (uprobe) at the symbol malloc inside /usr/bin/python3.
```
sudo perf probe -x /usr/bin/python3 malloc
```
- Python may have its own internal symbol named malloc, perhaps for wrapping or debugging.
- Or it could be a PLT (Procedure Linkage Table) stub , which is how calls to malloc are resolved dynamically when calling into libc.
- But this is NOT the actual malloc implementation — that lives in libc.so.6.
### Go
```
file /lib/go-1.22/bin/go
..
/lib/go-1.22/bin/go: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, Go BuildID=NaY_ztiU3LVZa2ji7gGb/BVafZ6p0TFQDhlr26dey/GDhy7NgRyoIxk9Nb4BU_/OzCYuwTwGmoJDQmAoNlQ, stripped
```
### Find out static libraries
There are some tracks of libc in golang though
```
strings  /lib/go-1.22/bin/go | grep -i 'GLIBC\|openssl\|libcrypto\|libc\|pthread'
...
*macho.DylibCmd
*runtime.libcall
...
cmd/go/internal/bug.printGlibcVersion
cmd/go/internal/bug.printGlibcVersion.deferwrap2
cmd/go/internal/bug.printGlibcVersion.deferwrap1
```
### What languages also use libc?
- Java (fork() calls at least)
- Ruby (All memory allocations, threads, and syscalls go through libc)
- PHP
- Perl
- Python/
- Node.js / Javascript (V8)
- Rust (But you can build no_std binaries that avoid libc, The musl target allows statically linking with musl, a lightweight libc alternative)
- C/C++ (untill syscalls explicitly specified)
### What languages don't use libc?
- Golang (You usually get a static binary, Go runtime makes direct syscalls instead of going through libc, Go also has its own memory allocator and scheduler. But seems like its possible to build goland with shared libc or musl)
