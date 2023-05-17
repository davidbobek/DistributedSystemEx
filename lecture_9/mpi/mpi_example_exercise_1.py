###############________________DESCRIPTION_________________###############

#run with {mpiexec -n 3 python mpi_example.py}
#3 is the number of processes
"""
Change the example so that each tasks includes a command to be executed by the worker
ADD if worker adds all parameters
SUB if worker substracts the last two parameters from the first one
POW if worker should sum the first two parameters and elevate it to the power given by the third one

The worker will then execute the operation and send the result back, along with its rank. If the operation is not known, it will return the string ‘UNKNOWN’

"""


import json
from mpi4py import MPI

#comm is a communicator object that represents a group of processes
comm = MPI.COMM_WORLD

#rank is a unique identifier for each process
if comm.rank == 0:
    tasks = [
        json.dumps({'parameter1': 1, 'parameter2': 2, 'parameter3': 3, 'command': 'ADD'}),
        json.dumps({'parameter1': 3, 'parameter2': 1, 'parameter3': 2, 'command': 'SUB'}),
        json.dumps({'parameter1': 2, 'parameter2': 3, 'parameter3': 1, 'command': 'POW'}),
        json.dumps({'parameter1': 2, 'parameter2': 3, 'parameter3': 1, 'command': 'HelloWorld3'})
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

if p['command'] == 'ADD':
    calc = p['parameter1'] + p['parameter2'] + p['parameter3']
    rank = comm.rank
elif p['command'] == 'SUB':
    calc = p['parameter1'] - p['parameter2'] - p['parameter3']
    rank = comm.rank
elif p['command'] == 'POW':
    calc = (p['parameter1'] + p['parameter2']) ** p['parameter3']
    rank = comm.rank
else:
    calc = 'UNKNOWN'
    rank = comm.rank

# gather results from all processes in comm
# sending my calc result to the root process
result = comm.gather([calc,{"rank":rank}], root=0)

if comm.rank == 0:
    print("[root]: Result is ", result)

