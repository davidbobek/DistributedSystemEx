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

import sys
import pickle
import zmq
from zmq.error import ZMQError, Again
import threading

is_coordinator = False
local_port = 0
port_coordinator = 0
processes = {}


def wait_for_messages():
    """
    Waits for an election message to arrive
    :return:
    """
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f'tcp://*:{local_port}')
    global port_coordinator

    while True:
        try:
            message = pickle.loads(socket.recv())
            print("Received message: %s" % message)
            if 'type' in message:
                if message['type'] == 'election':
                    response = {'type': 'election_ok', 'origin': local_port}
                    socket.send(pickle.dumps(response))
                    start_election()
                elif message['type'] == 'election_won':
                    response = {'type': 'election_ok', 'origin': local_port}
                    socket.send(pickle.dumps(response))
                    port_coordinator = message['winner']
                    print(f'New coordinator is {port_coordinator}')
                    check_coordinator()
                if 'type' in message and message['type'] == 'heartbeat':
                    processes[message['origin']] = True
                    print(f'Current processes: {processes}')
                    response = {'type': 'ack', 'processes': processes}
                    socket.send(pickle.dumps(response))
        except ZMQError as err:
            print(f"Exception: {err}")


def check_coordinator():
    """
    Checks if coordinator is alive by means of a heart beat message
    :return:
    """
    global processes
    # EXERCISE 1

    
    """
    Implement the check_coordinator function. It will send a heartbeat message to the current coordinator and start an election if the coordinator is considered to be down (after 5 sec. inactivity)
The coordinator returns a copy of its list of current processes, which will be stored by the process, too
Hint : Use socket.setsockopt(zmq.RCVTIMEO, timeout) to set a timeout upon receive. When timeout is exceeded, an exception ZMQError.Again will be raised

    
    """
    try:
        if port_coordinator != 0 and not is_coordinator:
            
            #send heartbeat to the coordinator
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            #setting a timer for 5 seconds for the socket to receive a message
            socket.setsockopt(zmq.RCVTIMEO, 5000)
            socket.connect(f'tcp://localhost:{port_coordinator}')
            message = {'type': 'heartbeat', 'origin': local_port}
            #converting to string form
            socket.send(pickle.dumps(message))
        
            response = pickle.loads(socket.recv())
            if 'type' in response and response['type'] == 'ack':
                processes = response['processes']
                print(f'Current processes: {processes}')
    except Again:
        print('Coordinator is down')
        start_election()
        return 
            
    threading.Timer(5, check_coordinator).start()

    
    

def start_election():
    """
    Starts an election (Bully algorithm)
    :return:
    """
    # EXERCISE 2
    # 1. Send election message to all processes with higher port number
    # 2. Wait for response
    # 3. If no response, declare itself as coordinator
    # 4. If response, wait for new coordinator message, coordinator is the one with highest port number
    # 5. Notify all processes of the new coordinator
    global processes
    message_sent = False
    print(f'Current processes: {processes}')
    for process in processes:
        print("My local port", local_port)
        if process <= local_port:
            continue
        message = {'type': 'election', 'origin': local_port}
        try:
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect(f'tcp://localhost:{process}')
            socket.send(pickle.dumps(message))
            message_sent = True
            response = pickle.loads(socket.recv())
            if 'type' in response and response['type'] == 'election_ok':
                print(f'Process {process} is alive')
                return
        except Again:
            pass
        
    if not message_sent:
        notify_new_coordinator()
        return

def notify_new_coordinator():
    """
    Notifies all processes of the new coordinator
    :return:
    """
    # EXERCISE 3
    
    if is_coordinator:
        return
    global processes
    
    
    
    
if __name__ == '__main__':
    nargs = len(sys.argv)
    if nargs <= 1:
        print('Usage: python bully_exercise.py <local_port> <port_coordinator> '
              'If port_coordinator is omitted then a new coordinator will be started')
        exit(0)
    local_port = int(sys.argv[1])
    if local_port <= 0:
        print(f'Invalid port number: {local_port}')
        exit(1)
    is_coordinator = True
    if nargs > 2:
        port_coordinator = int(sys.argv[2])
        is_coordinator = False
    if is_coordinator:
        print(f'Started coordinator on port {local_port}')
    else:
        print(f'Started node on port {local_port}')
        check_coordinator()

    thread = threading.Thread(target=wait_for_messages)
    thread.start()
