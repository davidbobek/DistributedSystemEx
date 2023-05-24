#!/usr/bin/env python
# encoding: utf8
#
# Copyright © Ruben Ruiz Torrubiano <ruben.ruiz at fh-krems dot ac dot at>,
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#    3. Neither the name of the owner nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


#run with {mpiexec -n 3 python mpi_example.py}
#3 is the number of processes
import json
from mpi4py import MPI

#comm is a communicator object that represents a group of processes
comm = MPI.COMM_WORLD

#rank is a unique identifier for each process
if comm.rank == 0:
    tasks = [
        json.dumps({'parameter1': 1, 'parameter2': 2, 'parameter3': 3}),
        json.dumps({'parameter1': 3, 'parameter2': 1, 'parameter3': 2}),
        json.dumps({'parameter1': 2, 'parameter2': 3, 'parameter3': 1})
    ]
else:
    tasks = None


# Scatter parameters arrays
# scatter distributes an array of tasks to all processes in comm (tasks is a list of parameters) if comm.rank == 0
unit = comm.scatter(tasks, root=0)

#loading the json string into a python dictionary
p = json.loads(unit)
print(f'[{comm.rank}]: parameters {p}')

# do some calculation adding the parameters and multiplying by the third parameter
calc = (p['parameter1'] + p['parameter2']) * p['parameter3']

# gather results from all processes in comm
# sending my calc result to the root process
result = comm.gather(calc, root=0)

if comm.rank == 0:
    print("[root]: Result is ", result)

