* Consider a system with the following requirements: a supercomputing cluster offers high-performance computing services to a scientific organization. This organization (and the cluster, too) is geographically distributed across different countries in several continents
* The system must be capable of running batch computing jobs sent by its clients and reporting the results (output files).
* List what types of transparencies are desirable and which not. Explain the reasons behind your choices.

![image](https://user-images.githubusercontent.com/114572512/222148246-960df1de-4bd1-4950-b596-493ebaeb9636.png)

##  Would it be relevant to hide the : 
 Acces | Location | Migration | Replication | Relocation | Concurrency | Fault
---|---|----|----|----|----|----
| Yes want to hide the framework used | Yes(if latency low),  No (if latency high) |  Yes (if location transparency possible) , No (if latency high) | Yes (if data can be stored in "equivalent") No (if replacing the data is relevant fomr a legal perspective) | Yes (while computing jobs are being executed) | Yes (not necessary to know that there are other users) No (could be relevant for estimating the current node of the system ) | Non-recoverable: someone pulls out the plug (No fault transparency ) Recovarable (Yes, case relocation transparrency can be provided) |
| * Data can be shared * Computing node can be shared | If there are two parts and they are far away |  |   | |  |  |
