# CPU
Если в системе с 10 процессорами скорость переключения контекста составляет 1 M/с, добавление 1 микросекунды на обработку каждого переключения
контекста потребует 10% ресурсов процессора (100% × (1 × 1 000 000 / 10 × 1 000 000)).
## Режимы работы
- Выполнение в пользовательском режиме
- Выполнение в системном режиме (Ядро)
- Простой (Idle)

Обычно ядро работает только по требованию, когда происходит системный вызов
или прерывание. Но есть исключения, например служебные потоки, которые дей-
ствуют в фоновом режиме, потребляя ресурсы CPU.
## Потоки процессора
- Аппаратные

Там где есть поддержка SMT (Simultaneous MultiThreading) - несколько аппаратных потоков может работать на одном ядре. Это технологии:
- Intel's Hyper-Threading
- AMD's SMT

Потоки одного ядра физически разделяют его ресурсы: L1, L2, Execution units (ALU, FPU), Branch predictor, Prefetchers
Но не разделяют Registers. У каждого потока свои.

L3 общий для всех ядер. 

Плюсы SMT:
- Более высокая пропускная способность на системе с большим количеством программных потоков, преимущественно однотипных чтобы L1, L2 кеш горячие были.
- Лучшая утилизация на такой системе.
## Планировщик
### CFS Scheduler
Completely Fair Scheduler

if there are 2 tasks running, then it runs each at 50% physical power --- i.e., actually in parallel.
On real hardware, we can run only a single task at once, so we have to introduce the concept of “virtual runtime.” The virtual runtime of a task specifies when its next timeslice would start execution on the ideal multi-tasking CPU described above. In practice, the virtual runtime of a task is its actual runtime normalized to the total number of running tasks.

In CFS the virtual runtime is expressed and tracked via the per-task p->se.vruntime (nanosec-unit) value. This way, it’s possible to accurately timestamp and measure the “expected CPU time” a task should have gotten.

CFS’s task picking logic is based on this p->se.vruntime value and it is thus very simple: it always tries to run the task with the smallest p->se.vruntime value (i.e., the task which executed least so far). CFS always tries to split up CPU time between runnable tasks as close to “ideal multitasking hardware” as possible.

Most of the rest of CFS’s design just falls out of this really simple concept, with a few add-on embellishments like nice levels, multiprocessing and various algorithm variants to recognize sleepers.

https://docs.kernel.org/scheduler/sched-design-CFS.html

https://en.wikipedia.org/wiki/Completely_Fair_Scheduler
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

#### Переключение контекса и режима
Потоки покидают CPU одним из двух способов: (1) намеренно, если блокируются
при вводе/выводе, блокировке или спящем режиме; (2) принудительно, если пре-
высили свое запланированное выделение процессорного времени и отменяются,
чтобы другие потоки могли работать, либо если они вытеснены потоком с более
высоким приоритетом. Когда процессор переключается с одного процесса или потока на другой, он переключает адресные пространства и другие метаданные.
Это называется переключением контекста1.

Кроме переключения контекста может также выполняться переключение режима: небло-
кирующие системные вызовы Linux могут (в зависимости от процессора) переключаться
только между режимами пользователя и ядра.

#### Миграция потока
Если поток находится в состоянии готовности к выполнению и ожидает в очереди, когда другой CPU простаивает, плани-
ровщик может перенести поток в очередь на выполнение неактивного CPU, чтобы
запустить его пораньше.

Но для оптимизации производительности планировщик
старается избегать миграций, если стоимость миграции может превысить ее выгоды, предпочитая оставлять потоки на одном и том же CPU, кэш которого может
все еще оставаться «горячим».
#### Cache-friendly design
The Linux scheduler is designed to be cache-aware :
 - Tasks are often scheduled on the same CPU (cache affinity) to take advantage of cached data. This reduces cache misses and improves performance.
## Кеши процессоров
![image](https://github.com/user-attachments/assets/2db3c3b9-94e2-4988-b861-a64b2a5d1cc8)
На процессоре с тремя уровнями кэшем
последнего уровня является кэш уровня 3. Кэши уровней 1 и 2 обычно есть отдельно
для каждого ядра CPU, а кэш уровня 3 — общий для всего кристалла.

Блок управления памятью (Memory Management Unit, MMU), отвечающий за преобразование
виртуальных адресов в физические, имеет свой кэш — буфер ассоциативной трансляции (Translation Lookaside Buffer, TLB).

## TLB
- A translation table walk occurs as the result of a TLB miss, and starts with a read of the appropriate starting-level translation table. The result of that read determines whether additional translation table reads are required, for this stage of translation


A translation lookaside buffer (TLB) is a memory cache that stores the recent translations of virtual memory to physical memory. It is used to reduce the time taken to access a user memory location.[1] It can be called an address-translation cache. It is a part of the chip's memory-management unit (MMU). A TLB may reside between the CPU and the CPU cache, between CPU cache and the main memory or between the different levels of the multi-level cache. 

Similar to caches, TLBs may have multiple levels. CPUs can be (and nowadays usually are) built with multiple TLBs, for example a small L1 TLB (potentially fully associative) that is extremely fast, and a larger L2 TLB that is somewhat slower. When instruction-TLB (ITLB) and data-TLB (DTLB) are used, a CPU can have three (ITLB1, DTLB1, TLB2) or four TLBs. 

These are typical performance levels of a TLB:

 - Size: 12 bits – 4,096 entries
 - Hit time: 0.5 – 1 clock cycle
 - Miss penalty: 10 – 100 clock cycles
 - Miss rate: 0.01 – 1% (20–40% for sparse/graph applications)

On an address-space switch, as occurs when context switching between processes (but not between threads), some TLB entries can become invalid, since the virtual-to-physical mapping is different. The simplest strategy to deal with this is to completely flush the TLB. This means that after a switch, the TLB is empty, and any memory reference will be a miss, so it will be some time before things are running back at full speed. Newer CPUs use more effective strategies marking which process an entry is for. This means that if a second process runs for only a short time and jumps back to a first process, the TLB may still have valid entries, saving the time to reload them.

![image](https://github.com/user-attachments/assets/aaa853d4-400e-4c7e-a168-9959d0afefcc)

## Page faults
Page fault is an exception that the memory management unit (MMU) raises when a process accesses a memory page without proper preparations. Accessing the page requires a mapping to be added to the process's virtual address space. Furthermore, the actual page contents may need to be loaded from a back-up, e.g. a disk. The MMU detects the page fault, but the operating system's kernel handles the exception by making the required page accessible in the physical memory or denying an illegal memory access. 

Page faults degrade system performance and can cause thrashing. Major page faults on a conventional computer using hard disk drives can have a significant impact on their performance, as a typical hard disk drive had an average rotational latency of 3 ms, a seek time of 5 ms and a transfer time of 0.05 ms/page. Therefore, the total time for paging is near 8 ms (8,000 μs). If the memory access time is 0.2 μs, then the page fault would make the operation about 40,000 times slower. With a more modern system using a fast solid-state drive with a page read latency of 0.030 ms (30 μs)[2] and a memory access latency of 70 ns (0.070 μs),[3] a hard page fault is still over 400 times slower. 

Thrashing occurs in a system with virtual memory when a computer's real storage resources are overcommitted, leading to a constant state of paging and page faults, slowing most application-level processing.[1] This causes the performance of the computer to degrade or even collapse. The situation can continue indefinitely until the user closes some running applications or the active processes free up additional virtual memory resources. 

 - Minor page faults

If the page is loaded in memory at the time the fault is generated, but is not marked in the memory management unit as being loaded in memory, then it is called a minor or soft page fault. The page fault handler in the operating system merely needs to make the entry for that page in the memory management unit point to the page in memory and indicate that the page is loaded in memory; it does not need to read the page into memory. This could happen if the memory is shared by different programs and the page is already brought into memory for other programs. 

 - Major page faults

This is the mechanism used by an operating system to increase the amount of program memory available on demand. The operating system delays loading parts of the program from disk until the program attempts to use it and the page fault is generated. If the page is not loaded in memory at the time of the fault, then it is called a major or hard page fault. The page fault handler in the OS needs to find a free location: either a free page in memory, or a non-free page in memory. This latter might be used by another process, in which case the OS needs to write out the data in that page (if it has not been written out since it was last modified) and mark that page as not being loaded in memory in its process page table. Once the space has been made available, the OS can read the data for the new page into memory, add an entry to its location in the memory management unit, and indicate that the page is loaded. Thus major faults are more expensive than minor faults and add storage access latency to the interrupted program's execution. 

 - Invalid page fault

If a page fault occurs for a reference to an address that is not part of the virtual address space, meaning there cannot be a page in memory corresponding to it, then it is called an invalid page fault. The page fault handler in the operating system will then generally pass a segmentation fault to the offending process, indicating that the access was invalid; this usually results in abnormal termination of the code that made the invalid reference. A null pointer is usually represented as a pointer to address 0 in the address space; many operating systems set up the MMU to indicate that the page that contains that address is not in memory, and do not include that page in the virtual address space, so that attempts to read or write the memory referenced by a null pointer get an invalid page fault. 

Kernel Page Table Isolation, KPTI устраняет уязвимость Meltdown
![image](https://github.com/user-attachments/assets/f281afe7-12c1-42e1-a93a-2626487ab279)

## Branches, branch misses
Branch instructions are those that change the flow of execution, such as:
 - Conditional branches (if, else, loops)
 - Function calls
 - Returns
 - Jumps

Branch misses are incorrect predictions made by the CPU. <br>
In modern CPUs, branch prediction is used to guess the direction of a branch (like an if statement or loop) before it's actually known.

Branch mispredictions cause performance issues because:
 - The CPU speculatively executes instructions based on its predicted path.
 - If the prediction was wrong:
   - All those speculative instructions must be discarded.
   - The correct instructions must then be fetched and executed.
   - This wastes time and CPU resources (pipeline flushes, wasted computation).

To reduce branch misses:
 - Replace unpredictable branches with branchless code (e.g., using bitwise operations or conditional moves).
 - Avoid deeply nested or complex conditionals when possible.
 - Use data structures with predictable access patterns.

## Cache references
Memory accesses that reference the CPU cache . This includes both hits and misses — it's just a count of how often the CPU tried to access data/instructions from the cache.

## Bus cycles
Cycles during which the CPU bus was in use . The CPU bus connects the processor to other components (like memory or I/O devices).
High bus cycles can indicate heavy communication with external components, possibly due to cache misses or memory access bottlenecks.
## Доступ к памяти
- Неоднородный доступ к памяти (non-uniform memory access, NUMA) - архитектура организации оперативной памяти, используемая в мультипроцессорных системах, в которой процессор имеет быстрый доступ к локальной памяти через свой контроллер, а также более медленный канал до памяти, подключённой к контроллерам (слотам) других процессоров, реализуемый через шину обмена данными.

Доступ одного процессора к памяти, присоединённой к другому, осуществляется через специализированную шину, соответственно, задержки такого доступа выше, а пропускная способность может быть ниже. 
![NUMA_CPU](https://github.com/user-attachments/assets/c9624b2b-0466-43e7-9765-e2342e61a8e9)

- Однородный доступ к памяти (uniform memory access, UMA) - архитектура многопроцессорных компьютеров с общей памятью, в которой все процессоры используют физическую память одновременно, по общим путям и с равномерными задержками и пропускной способностью. В некоторых случаях каждый процессор может использовать свой собственный кэш.

Такая схема работы с памятью используется в системах с симметричной мультипроцессорностью (SMP-машинах), поэтому термины UMA и SMP часто используются вместе как «SMP/UMA». 
