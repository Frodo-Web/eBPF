# CPU perf
TLB misses cause a walk
```
openssl speed -multi 2

perf stat -e dTLB-loads,dTLB-stores,iTLB-loads,dtlb_load_misses.miss_causes_a_walk,dtlb_store_misses.miss_causes_a_walk,itlb_misses.miss_causes_a_walk -a sleep 5

 Performance counter stats for 'system wide':

       10975822966      dTLB-loads
        5544184747      dTLB-stores
             18248      iTLB-loads
             75429      dtlb_load_misses.miss_causes_a_walk
           1137670      dtlb_store_misses.miss_causes_a_walk
             53060      itlb_misses.miss_causes_a_walk

       5.003970099 seconds time elapsed

perf stat -e dTLB-loads,dTLB-stores,iTLB-loads,dtlb_load_misses.miss_causes_a_walk,dtlb_store_misses.miss_causes_a_walk,itlb_misses.miss_causes_a_walk -a sleep 5

 Performance counter stats for 'system wide':

       16065796401      dTLB-loads
       10468747109      dTLB-stores
             12395      iTLB-loads
             90483      dtlb_load_misses.miss_causes_a_walk
            376078      dtlb_store_misses.miss_causes_a_walk
            125098      itlb_misses.miss_causes_a_walk

       5.002948220 seconds time elapsed
```
L1 Cache misses and migrations
```
openssl speed -multi 6

perf stat -e cpu-cycles,cpu-migrations,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,L1-icache-load-misses -a sleep 5

 Performance counter stats for 'system wide':

       61895983417      cpu-cycles
                72      cpu-migrations
       24147346350      L1-dcache-loads
           1686087      L1-dcache-load-misses            #    0.01% of all L1-dcache accesses
       13657672453      L1-dcache-stores
           1083799      L1-icache-load-misses

       5.003084790 seconds time elapsed
```
