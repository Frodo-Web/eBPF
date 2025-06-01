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
