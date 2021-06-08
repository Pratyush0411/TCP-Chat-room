import socket 
import threading 

# PROTOCOL: For sending messages
# Sender sends a header message containing integer representing the length
# Receiver decodes the header message using the .decode the function 
# Receiver allocated spaced according to the header 
# Sender sends the actual message


# To handle multiple clients multithreading has been used
# Every client is assigned a new thread and the processor takes care of the scheduling

# will put the constants in config.json later 
HEADER = 64 

PORT = 5050

SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)

FORMAT = 'utf-8'

DISCONNECT_MESSAGE= "exit()"

# mutable object by all threads
clients = []

# to avoid critical section problem
clients_lock = threading.Lock()


# binding 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)

# receive client messages

def receive(conn, addr):
    msg_length = conn.recv(HEADER).decode(FORMAT)

    if msg_length:
        msg_length = int(msg_length)

        msg = conn.recv(msg_length).decode(FORMAT)
    else: 
        pass

    return msg 

# broadcast message
def broadcast(message):
    message = message.encode(FORMAT)
    # finding the length of the encoded message
    msg_length = len(message)
    # sending the length of message 
    send_length = str(msg_length).encode(FORMAT)
    # padding the header message
    send_length += b' ' * (HEADER - len(send_length))

    # lock
    with clients_lock:
        for client in clients:
            client.send(send_length)
            client.send(message)

    


            
# handle client function
def handle_client(conn, addr):
    #print(f"[CONNECTED] {addr}")
    
    broadcast(f"[CONNECTED] {addr}")

    flag = True

    while flag:
        msg = receive(conn, addr)
        print(msg)
        #print (f"[{addr}]: {msg}")
        if msg == DISCONNECT_MESSAGE:
            with clients_lock:
                print(clients)
                index = clients.index(conn)
                clients.remove(conn)
                #conn.close()
            broadcast(f"[DISCONNECTED] {addr}")
            flag = False
        elif msg != None:
            msg = f"{addr}: "+f"{msg}"
            broadcast(message= msg)
    
    with clients_lock:
        clients.remove(conn)
        conn.close()

# start function
# allocates threads for clients 
def main():
    print("Server is starting...")
    server.listen()
    print(f"Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

main()








        