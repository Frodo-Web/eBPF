# CPU perf
### TLB misses cause a walk
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
### L1 Cache misses and migrations
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

stress-ng --cpu 2 --io 0 --vm 1 --vm-bytes 1G --timeout 360s

perf stat -e cpu-cycles,cpu-migrations,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,L1-icache-load-misses -a sleep 5

 Performance counter stats for 'system wide':

       59609629131      cpu-cycles
              1067      cpu-migrations
       20874259912      L1-dcache-loads
        1177849418      L1-dcache-load-misses            #    5.64% of all L1-dcache accesses
       12484812923      L1-dcache-stores
         292129082      L1-icache-load-misses

       5.003335702 seconds time elapsed
```
### Page faults
```
openssl speed -multi 4

perf stat -e major-faults,minor-faults,page-faults -a sleep 10

 Performance counter stats for 'system wide':

                 0      major-faults
                80      minor-faults
                80      page-faults

      10.002624583 seconds time elapsed

openssl speed -multi 64

perf stat -e major-faults,minor-faults,page-faults -a sleep 10

 Performance counter stats for 'system wide':

                 0      major-faults
               209      minor-faults
               209      page-faults

      10.032003481 seconds time elapsed

stress-ng --cpu 4 --vm 2 --fork 4 --switch 4 --timeout 1m

perf stat -e major-faults,minor-faults,page-faults -a sleep 10

 Performance counter stats for 'system wide':

                 0      major-faults
           1833069      minor-faults
           1833069      page-faults

      10.003890280 seconds time elapsed
```
### Branch instructions, branch misses
```
perf stat -e branch-instructions,branch-misses,instructions -a sleep 10

 Performance counter stats for 'system wide':

           7420378      branch-instructions
            386706      branch-misses                    #    5.21% of all branches
          32208453      instructions

      10.001062681 seconds time elapsed

perf stat -e branch-instructions,branch-misses,instructions -a sleep 10

openssl speed -multi 4

 Performance counter stats for 'system wide':

        8172979753      branch-instructions
           5620132      branch-misses                    #    0.07% of all branches
      252741618034      instructions

      10.001855385 seconds time elapsed

stress-ng --cpu 4 --vm 2 --fork 4 --switch 4 --timeout 1m

perf stat -e branch-instructions,branch-misses,instructions -a sleep 10

 Performance counter stats for 'system wide':

       28195651327      branch-instructions
         276974391      branch-misses                    #    0.98% of all branches
      170019755390      instructions

      10.004069634 seconds time elapsed
```
### Cache references and misses
```
perf stat -e cache-references,cache-misses -a sleep 10

 Performance counter stats for 'system wide':

           2118696      cache-references
             79318      cache-misses                     #    3.74% of all cache refs

      10.001057746 seconds time elapsed

openssl speed -multi 4

perf stat -e cache-references,cache-misses -a sleep 10

 Performance counter stats for 'system wide':

            814845      cache-references
             60696      cache-misses                     #    7.45% of all cache refs

stress-ng --cpu 4 --vm 2 --fork 4 --switch 4 --timeout 1m

perf stat -e cache-references,cache-misses -a sleep 10

 Performance counter stats for 'system wide':

        1238234420      cache-references
         104724132      cache-misses                     #    8.46% of all cache refs

      10.004109657 seconds time elapsed
```
