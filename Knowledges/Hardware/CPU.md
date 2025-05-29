# CPU
## Режимы работы
- Выполнение в пользовательском режиме
- Выполнение в системном режиме (Ядро)
- Простой (Idle)

Обычно ядро работает только по требованию, когда происходит системный вызов
или прерывание. Но есть исключения, например служебные потоки, которые дей-
ствуют в фоновом режиме, потребляя ресурсы CPU.

## Планировщик
### CFS Scheduler
Completely Fair Scheduler

if there are 2 tasks running, then it runs each at 50% physical power --- i.e., actually in parallel.
On real hardware, we can run only a single task at once, so we have to introduce the concept of “virtual runtime.” The virtual runtime of a task specifies when its next timeslice would start execution on the ideal multi-tasking CPU described above. In practice, the virtual runtime of a task is its actual runtime normalized to the total number of running tasks.

In CFS the virtual runtime is expressed and tracked via the per-task p->se.vruntime (nanosec-unit) value. This way, it’s possible to accurately timestamp and measure the “expected CPU time” a task should have gotten.

CFS’s task picking logic is based on this p->se.vruntime value and it is thus very simple: it always tries to run the task with the smallest p->se.vruntime value (i.e., the task which executed least so far). CFS always tries to split up CPU time between runnable tasks as close to “ideal multitasking hardware” as possible.

Most of the rest of CFS’s design just falls out of this really simple concept, with a few add-on embellishments like nice levels, multiprocessing and various algorithm variants to recognize sleepers.

https://docs.kernel.org/scheduler/sched-design-CFS.html
### EEVDF Scheduler
CFS can be replaced with Earliest Eligible Virtual Deadline (EEVDF) First starting from kernel version 6.6 as an option.

Similarly to CFS, EEVDF aims to distribute CPU time equally among all runnable tasks with the same priority. To do so, it assigns a virtual run time to each task, creating a “lag” value that can be used to determine whether a task has received its fair share of CPU time. In this way, a task with a positive lag is owed CPU time, while a negative lag means the task has exceeded its portion. EEVDF picks tasks with lag greater or equal to zero and calculates a virtual deadline (VD) for each, selecting the task with the earliest VD to execute next. It’s important to note that this allows latency-sensitive tasks with shorter time slices to be prioritized, which helps with their responsiveness.

There are ongoing discussions on how to manage lag, especially for sleeping tasks; but at the time of writing EEVDF uses a “decaying” mechanism based on virtual run time (VRT). This prevents tasks from exploiting the system by sleeping briefly to reset their negative lag: when a task sleeps, it remains on the run queue but marked for “deferred dequeue,” allowing its lag to decay over VRT. Hence, long-sleeping tasks eventually have their lag reset. Finally, tasks can preempt others if their VD is earlier, and tasks can request specific time slices using the new sched_setattr() system call, which further facilitates the job of latency-sensitive applications.

https://docs.kernel.org/scheduler/sched-eevdf.html
### Потребители
1. Потоки выполнения
Основными потребителями
являются потоки выполнения (их также называют задачами), которые принадлежат
процессам или процедурам ядра.
2. Обработчики прерываний
Прерывания могут быть программными (вызываются
ПО) или аппаратными.
![image](https://github.com/user-attachments/assets/88e8b508-54f7-4900-bcbc-38f433366a5a)
Здесь изображены потоки в трех состояниях: НА ПРОЦЕССОРЕ — потоки,
выполняющиеся на CPU, ГОТОВЫ К ВЫПОЛНЕНИЮ — потоки, которые
готовы к работе и ожидают своей очереди, и ПРИОСТАНОВЛЕНЫ — потоки,
заблокированные в ожидании некоторого события. Сюда же относятся пото -
ки, находящиеся в состоянии непрерываемого ожидания.

(Очереди выполнения — это то, как
первоначально было реализовано планирование, этот термин и ментальная модель
все еще используются для описания ожидающих задач. При этом планировщик
CFS (Completely Fair Scheduler) в Linux в реальности использует красно-черное
дерево будущего выполнения задач.)

 термин «на CPU» (оn-CPU) обозначает состояние НА ПРОЦЕССОРЕ,
а «вне CPU» (off-CPU) — все другие состояния, то есть когда поток не выполня-
ется на CPU.

Потоки покидают CPU одним из двух способов: (1) намеренно, если блокируются
при вводе/выводе, блокировке или спящем режиме; (2) принудительно, если пре-
высили свое запланированное выделение процессорного времени и отменяются,
чтобы другие потоки могли работать, либо если они вытеснены потоком с более
высоким приоритетом. Когда процессор переключается с одного процесса или потока на другой, он переключает адресные пространства и другие метаданные.
Это называется переключением контекста1.

Кроме переключения контекста может также выполняться переключение режима: небло-
кирующие системные вызовы Linux могут (в зависимости от процессора) переключаться
только между режимами пользователя и ядра.
## Доступ к памяти
- Неоднородный доступ к памяти (non-uniform memory access, NUMA) - архитектура организации оперативной памяти, используемая в мультипроцессорных системах, в которой процессор имеет быстрый доступ к локальной памяти через свой контроллер, а также более медленный канал до памяти, подключённой к контроллерам (слотам) других процессоров, реализуемый через шину обмена данными.

Доступ одного процессора к памяти, присоединённой к другому, осуществляется через специализированную шину, соответственно, задержки такого доступа выше, а пропускная способность может быть ниже. 
![NUMA_CPU](https://github.com/user-attachments/assets/c9624b2b-0466-43e7-9765-e2342e61a8e9)

- Однородный доступ к памяти (uniform memory access, UMA) - архитектура многопроцессорных компьютеров с общей памятью, в которой все процессоры используют физическую память одновременно, по общим путям и с равномерными задержками и пропускной способностью. В некоторых случаях каждый процессор может использовать свой собственный кэш.

Такая схема работы с памятью используется в системах с симметричной мультипроцессорностью (SMP-машинах), поэтому термины UMA и SMP часто используются вместе как «SMP/UMA». 
