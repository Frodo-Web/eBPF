# bpftrace
![image](https://github.com/user-attachments/assets/8bfb83f4-92ca-44c8-b2e1-0bd01e82cdde)

## Сравнение bpftrace с другими инструментами
мониторинга
- perf(1): в сравнении с компактным и высокоуровневым языком bpftrace язык
сценариев perf(1) выглядит слишком многословным. perf(1) поддерживает
эффективный способ передачи событий в двоичном формате через perf record
и режимы формирования сводной информации в памяти — perf top. bpftrace
реализует эффективные методы обобщения информации в ядре, например по-
строение гистограмм, тогда как встроенные в ядро сводки perf(1) ограничены
счетчиками (perf stat). Возможности perf(1) расширяются с помощью программ
BPF, но пишутся на другом языке, не таком высокоуровневом, как bpftrace. При-
мер программы BPF для perf(1) ищите в приложении D.
 - Ftrace: bpftrace предлагает высокоуровневый язык программирования, похожий
на C и awk, тогда как средства инструментации в Ftrace, включая триггеры hist,
имеют свой, ни на что не похожий синтаксис. Ftrace имеет меньше зависимостей,
поэтому он лучше подходит для использования в небольших встраиваемых си-
стемах Linux. Также Ftrace поддерживает такие режимы инструментации, как
подсчет вызовов функций, которые действуют более оптимально, чем источни-
ки событий в bpftrace. (Моя версия funccount(8) на основе Ftrace запускается
и останавливается быстрее и имеет меньший оверхед, чем эквивалентная версия
на основе bpftrace.)
- SystemTap: оба трассировщика, bpftrace и SystemTap, предлагают высокоуровне-
вые языки программирования. Но bpftrace основан на технологиях, встроенных
в ядро Linux, а SystemTap добавляет свои модули ядра, которые оказались не-
надежными в системах, отличных от RHEL. Но в SystemTap уже идут работы
по реализации поддержки BPF по аналогии с bpftrace, что должно повысить
надежность трассировщика в этих других системах. Сейчас у SystemTap больше
вспомогательных функций в своих библиотеках для инструментации различных
событий.
 - LTTng: LTTng оптимизирует вывод дампов событий и предоставляет инструмен-
ты для их анализа. Он использует иной подход к анализу производительности,
чем bpftrace, ориентированный на выполнение анализа в масштабе реального
времени.
 - Прикладные инструменты: область применения прикладных инструментов
и инструментов среды выполнения ограничены пространством пользователя.
bpftrace, напротив, способен также инструментировать и обрабатывать события
в пространстве ядра, позволяя идентифицировать источники проблем, недоступ-
ные прикладным инструментам. Однако прикладные инструменты имеют свои
преимущества — обычно они адаптированы для использования с конкретным
приложением или средой выполнения. Профилировщик базы данных MySQL
уже знает, как инструментировать запросы, а профилировщик JVM — сборку
мусора. В bpftrace все это приходится реализовывать вручную.

## Примеры однострочных комманд
```
Подсчитывает число страниц, загруженных каждым процессом:
bpftrace -e 'software:major-faults:1 { @[comm] = count(); }'

Подсчитывает число отказов страниц для каждого процесса:
bpftrace -e 'software:faults:1 { @[comm] = count(); }'

Профилирует стек в пространстве пользователя для PID 189 с частотой 49 Гц:
bpftrace -e 'profile:hz:49 /pid == 189/ { @[ustack] = count(); }'

# bpftrace -l 'kprobe:vfs_*'
kprobe:vfs_fallocate
kprobe:vfs_truncate
kprobe:vfs_open
kprobe:vfs_setpos
kprobe:vfs_llseek
[...]
bpftrace -l 'kprobe:vfs_*' | wc -l
56

# bpftrace -e 't:block:block_rq_insert { @[kstack] = count(); }'
Attaching 1 probe...
^C
[...]
@[
blk_mq_insert_requests+203
blk_mq_sched_insert_requests+111
blk_mq_flush_plug_list+446
blk_flush_plug_list+234
blk_finish_plug+44
dmcrypt_write+593
kthread+289
ret_from_fork+53
]: 39

# bpftrace -e 'uprobe:/bin/bash:readline {
printf("PS1: %s\n", str(*uaddr("ps1_prompt"))); }'
Attaching 1 probe...
PS1: \[\e[34;1m\]\u@\h:\w>\[\e[0m\]
PS1: \[\e[34;1m\]\u@\h:\w>\[\e[0m\]
^C

# bpftrace -e 'tracepoint:timer:hrtimer_start { @[ksym(args->function)] = count(); }'
Attaching 1 probe...
^C
@[sched_rt_period_timer]: 4
@[watchdog_timer_fn]: 8
@[timerfd_tmrproc]: 15
@[intel_uncore_fw_release_timer]: 1111
@[it_real_fn]: 2269
@[hrtimer_wakeup]: 7714
@[tick_sched_timer]: 27092

# bpftrace -e 'k:do_nanosleep { printf("%s", ustack(perf)); }'
Attaching 1 probe...
[...]
7f220f1f2c60 nanosleep+64 (/lib/x86_64-linux-gnu/libpthread-2.27.so)
7f220f653fdd g_timeout_add_full+77 (/usr/lib/x86_64-linux-gnu/libglib-
2.0.so.0.5600.3)
7f220f64fbc0 0x7f220f64fbc0 ([unknown])
841f0f 0x841f0f ([unknown])

# bpftrace --unsafe -e 't:syscalls:sys_enter_nanosleep { system("ps -p %d\n",
pid); }'
Attaching 1 probe...
PID TTY TIME CMD
29893 tty2 05:34:22 mysqld
PID TTY TIME CMD
29893 tty2 05:34:22 mysqld
PID TTY TIME CMD
29893 tty2 05:34:22 mysqld
[...]

# bpftrace -e 't:syscalls:sys_enter_read { @reads = count(); }
interval:s:5 { exit(); }'
Attaching 2 probes...
@reads: 735
```

## Программирование на bpftrace
```
#!/usr/local/bin/bpftrace
// эта программа измеряет продолжительность выполнения vfs_read()
kprobe:vfs_read
{
@start[tid] = nsecs;
}
kretprobe:vfs_read
/@start[tid]/
{
$duration_us = (nsecs - @start[tid]) / 1000;
@us = hist($duration_us);
delete(@start[tid]);
}
```
### Комментарии
```
// это комментарий

/*
* это многострочный
* комментарий
*/
```
### Порядок использования
```
bpftrace -e program

bpftrace file.bt
```
### Структура
```
probes { actions }

probes /filter/ { actions }

probe1,probe2,... { actions }

Есть два специальных типа зондов, для которых не нужно указывать дополни -
тельные идентификаторы BEGIN и END. Они срабатывают в начале и в конце
программы bpftrace (в точности как в awk(1))
```
### Фильтры
```
/pid == 123/

/pid != 0/ то же самое что /pid/

/pid > 100 && pid < 1000/
```
### Действия
```
{ action one; action two; action three }

{ $x = 42; printf("$x is %d", $x); }
```
### Hello world
```
# bpftrace -e 'BEGIN { printf("Hello, World!\n"); }'
Attaching 1 probe...
Hello, World!
^C

#!/usr/local/bin/bpftrace
BEGIN
{
printf("Hello, World!\n");
}
```
### Функции

Кроме printf() — функции форматированного вывода — есть еще встроенные
функции, в том числе:
 - exit(): производит выход из программы bpftrace;
 - str(char *): возвращает строку по указателю;
 - system(format[, arguments ...]): выполняет команду в командной оболочке.
```
printf("got: %llx %s\n", $x, str($x)); exit();
```
выведет значение переменной $x в шестнадцатеричном формате, а затем попытается
интерпретировать его как указатель на массив символов, завершающийся пустым
символом NULL (char *), выведет его как строку и завершит выполнение программы.

### Переменные
- Встроенные переменные (built-in variables) предопределены и предоставляются
bpftrace. Обычно они доступны только для чтения. К ним относятся pid (иденти-
фикатор процесса), comm (имя процесса), nsecs (отметка времени в наносекундах)
и curtask (адрес task_struct текущего потока).
![image](https://github.com/user-attachments/assets/152954b6-c433-47f2-bdb1-80346911a2ab)

- Временные переменные (scratch variables) можно использовать для временного
хранения результатов вычислений. Их имена начинаются с префикса «$». Сама пере-
менная и ее тип определяются первой операцией присваивания.
```
$x = 1;
$y = "hello";
$z = (struct task_struct *)curtask;
```

- Переменные-карты (map variables) хранятся в хранилище карт BPF, и их имена
должны начинаться с префикса «@». В этих переменных можно сохранять данные
для их передачи между действиями. Программа

probe1 { @a = 1; }
probe2 { $x = @a; }

присвоит число 1 переменной @a, когда возникнет событие probe1, а затем, когда
возникнет событие probe2, присвоит значение @a переменной $x. Если сначала
возникнет событие probe1, а затем probe2, переменная $x получит значение 1, в про-
тивном случае — значение 0 (значение по умолчанию для неинициализированой
переменной).

После имени переменной-карты можно указать ключ и использовать такие пере-
менные на манер хеш-таблицы (ассоциативного массива). Инструкция

@start[tid] = nsecs;

часто используется в практике: в данном случае она сохранит значение встроенной
переменной nsecs в карте с именем @start и с ключом tid (идентификатором теку-
щего потока).

@path[pid, $fd] = str(arg0);

Это пример карты с множественными ключами, здесь роль ключей играют значение
встроенной переменной pid и значение временной переменной $fd.
### Функции карт
![image](https://github.com/user-attachments/assets/3b307fe6-894b-44f5-aecc-c0f2b7217398)

```
@x = count(); //Для каждого проца

@x++; //Общее но возможна погрешность

@y = sum($x);

@z = hist($x);

print(@x); // Но она используется не часто, потому что после завершения
bpftrace все карты выводятся автоматически.

delete(@start[tid]);
```
### Аннотации
```
$duration_us = (nsecs - @start[tid]) / 1000;
@us = hist($duration_us);

# bpftrace vfsread.bt
Attaching 2 probes...
^C
@us:
[0] 23 |@ |
[1] 138 |@@@@@@@@@ |
[2, 4) 538 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ |
[4, 8) 744 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[8, 16) 641 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ |
[16, 32) 122 |@@@@@@@@ |
[32, 64) 13 | |
[64, 128) 17 |@ |
[128, 256) 2 | |
[256, 512) 0 | |
[512, 1K) 1 | |
```

```
$duration_us = (nsecs - @start[tid]) / 1000;
@us[pid, comm] = hist($duration_us);

# bpftrace vfsread.bt
Attaching 2 probes...
^C
@us[1847, gdbus]:
[1] 2 |@@@@@@@@@@ |
[2, 4) 10 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[4, 8) 10 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
@us[1630, ibus-daemon]:
[2, 4) 9 |@@@@@@@@@@@@@@@@@@@@@@@@@@@ |
[4, 8) 17 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
@us[29588, device poll]:
[1] 13 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ |
[2, 4) 15 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[4, 8) 4 |@@@@@@@@@@@@@ |
[8, 16) 4 |@@@@@@@@@@@@@ |
[...]
```
### Формат определения зондов

Иерархия зависит от типа зонда. Например:
```
kprobe:vfs_read
uprobe:/bin/bash:readline
```
### Типы зондов 
![image](https://github.com/user-attachments/assets/5d993c57-6b8c-4382-8b33-f05bf438f47f)
#### tracepoint
```
# bpftrace -e 'tracepoint:syscalls:sys_enter_clone {
printf("-> clone() by %s PID %d\n", comm, pid); }
tracepoint:syscalls:sys_exit_clone {
printf("<- clone() return %d, %s PID %d\n", args->ret, comm, pid); }'
Attaching 2 probes...
-> clone() by bash PID 2582
<- clone() return 27804, bash PID 2582
<- clone() return 0, bash PID 27804

# bpftrace -e 't:syscalls:sys_*_execve { printf("%s %s PID %d\n", probe, comm,
pid); }'
Attaching 2 probes...
tracepoint:syscalls:sys_enter_execve bash PID 28181
tracepoint:syscalls:sys_exit_execve ls PID 28181
```
#### usdt
```
usdt:binary_path:probe_name
usdt:library_path:probe_name
usdt:binary_path:probe_namespace:probe_name
usdt:library_path:probe_namespace:probe_name

usdt:/.../libjvm.so:hotspot:method__entry

# bpftrace -l 'usdt:/usr/local/cpython/python'
usdt:/usr/local/cpython/python:line
usdt:/usr/local/cpython/python:function__entry
usdt:/usr/local/cpython/python:function__return
usdt:/usr/local/cpython/python:import__find__load__start
usdt:/usr/local/cpython/python:import__find__load__done
usdt:/usr/local/cpython/python:gc__start
usdt:/sur/local/cpython/python:gc__done
```
Можно получить и список зондов USDT в выполняющемся процессе, в этом случае
вместо имени файла следует использовать параметр -p PID.
#### kprobe и kretprobe
```
kprobe:function_name
kretprobe:function_name
```
#### uprobe и uretprobe
```
uprobe:binary_path:function_name
uprobe:library_path:function_name
uretprobe:binary_path:function_name
uretprobe:library_path:function_name
```
#### software и hardware
```
software:event_name:count
software:event_name:
hardware:event_name:count
hardware:event_name:
```
Программные события похожи на точки трассировки tracepoint, но определены для
метрик, основанных на подсчете и выборках. Аппаратные события — это счетчики
PMC для анализа на уровне процессора.

События этих двух типов могут возникать настолько часто, что инструментация
любого из них повлечет значительные издержки, снижающие производительность
системы. Этого можно избежать, использовав выборку и поле count. Если поле count
определено, зонд будет срабатывать один раз на каждые [count] событий. Если поля count нет, используется значение по умолчанию. Например, зонд software:page-faults:100 будет срабатывать один раз на каждые 100 отказов страниц.
![image](https://github.com/user-attachments/assets/36fd6598-4198-4c1b-b35f-d68ac8d329be)
![image](https://github.com/user-attachments/assets/1110ad8b-48cc-48cd-a5df-e5b67c22cd58)
#### profile и interval
Зонды этого типа инструментируют события, имеющие отношение к времени.
```
profile:hz:rate
profile:s:rate
profile:ms:rate
profile:us:rate
interval:s:rate
interval:ms:rate
```
Зонды profile срабатывают для всех процессоров и используются для определения
параметров загрузки процессора.

Зонды interval срабатывают только для одного
процессора и используются для вывода интервальных метрик.

Например, зонд profile:hz:99 срабатывает 99 раз в секунду для всех процессоров.
Частота 99 используется чаще, чем 100, чтобы избежать проблем, связанных с по-
паданием в одну и ту же точку. Зонд interval:s:1 будет срабатывать один раз в секунду
и может использоваться для вывода метрик раз в секунду.
### Тернарные операторы
```
test ? true_statement : false_statement

$abs = $x >= 0 ? $x : - $x;
```
### if
```
if (test) { true_statements }
if (test) { true_statements } else { false_statements }

if ($inet_family == $AF_INET) {
// IPv4
...
} else {
// IPv6
...
}
```
### Функции bpftrace
![image](https://github.com/user-attachments/assets/d9a85960-3e0e-455a-86e0-5549a83f9017)
