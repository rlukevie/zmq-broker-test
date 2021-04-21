#!/usr/bin/env python

import sys
import time

import zmq

def worker(id: str, sleep_time: float, capability: str):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect("tcp://localhost:5556")
    print(f"    Worker {id} started. It can deliver {capability}")
    
    while True:
        try:
            message = socket.recv_json()
            print(f"    Worker {id} receives message: {message}")
            if message["task"] == capability:
                time.sleep(sleep_time)
                worker_message = {"status": "done", 
                                  "message": f"Worker {id} finished {message}"}
                print(f"    Worker {id} sends: {worker_message}")
                socket.send_json(worker_message)
            else:
                worker_message = {"status": "rejected",
                                  "message": f"Worker {id} cannot process {message['task']}"}
                print(f"    Worker {id} sends: {worker_message}")
                socket.send_json(worker_message)
        except Exception:
            socket.close()
            context.term()
            break
            
        
        
if __name__ == "__main__":
    worker(sys.argv[1], float(sys.argv[2]), sys.argv[3])