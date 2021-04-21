#!/usr/bin/env python

import zmq

def broker():
    context = zmq.Context()
    
    router = context.socket(zmq.ROUTER)
    router.bind("tcp://*:5555")
    
    dealer = context.socket(zmq.DEALER)
    dealer.bind("tcp://*:5556")
    
    poller = zmq.Poller()
    poller.register(router, zmq.POLLIN)
    poller.register(dealer, zmq.POLLIN)
    
    print("  Broker started")
    
    while True:
        try: 
            socks = dict(poller.poll())
        except Exception:
            dealer.close()
            router.close()
            context.term()
            break
        
        if router in socks:
            message = router.recv_multipart()
            # print(f"  Router receives: {message}")
            # print(f"  Dealer sends: {message}")
            dealer.send_multipart(message)
            
        if dealer in socks:
            message = dealer.recv_multipart()
            # print(f"  Dealer receives: {message}")
            # print(f"  Router sends: {message}")
            router.send_multipart(message)

    

if __name__ == "__main__":
    broker()