#!/usr/bin/env python

import sys
import time

import zmq

def client(id: str, sleep_time: float, task: str):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    time.sleep(2)
    print(f"Client {id} started: It wants {task}")
    
    items_received = 0
    
    for _ in range(20):
        try:
            status = ""
            while status != "done":
                message_send = {"message": f"{id} wants something", "task": task}
                socket.send_json(message_send)
                print(f"Client {id} sends: '{message_send}'")
                message_recv = socket.recv_json()
                print(f"Client {id} receives: '{message_recv}'")
                status = message_recv["status"]
            items_received += 1
            time.sleep(sleep_time)
        except Exception:
            socket.close()
            context.term()
            break
    print(f"*** Client {id} received {items_received} {task} ***")
    
if __name__ == "__main__":
    time.sleep(0.5)
    client(sys.argv[1], float(sys.argv[2]), sys.argv[3])
    