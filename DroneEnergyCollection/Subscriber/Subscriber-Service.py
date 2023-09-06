import zmq

def relay_data(subscriber_address, publisher_address):
    context = zmq.Context()
    
    # Subscriber socket
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect(subscriber_address)
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")
    
    # Publisher socket
    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind(publisher_address)

    while True:
        message = sub_socket.recv_string()
        print(message)  # print the received message
        pub_socket.send_string(message)  # relay the received message

if __name__ == "__main__":
    relay_data("tcp://172.18.0.2:6001", "tcp://*:5555")
