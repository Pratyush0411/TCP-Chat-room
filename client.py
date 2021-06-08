import socket 
import select
import sys

HEADER = 64 

PORT = 5050

# my computer internal ip address to connect with the server

SERVER = '127.0.1.1' # change to your ip when running server on your computer

ADDR = (SERVER, PORT)

FORMAT = 'utf-8'

DISCONNECT_MESSAGE= "exit()"

# connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def receive(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)

    if msg_length:
        msg_length = int(msg_length)

        msg = conn.recv(msg_length).decode(FORMAT)
    else: 
        pass

    return msg

def send(conn, message):

    message = message.encode(FORMAT)
    # finding the length of the encoded message
    msg_length = len(message)
    # sending the length of message 
    send_length = str(msg_length).encode(FORMAT)
    # padding the header message
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

# start function 
# switching between listening and writing
def main():
    #global client

    flag = True

    while flag:
        # defining sockets for reading and writing
        sockets = [sys.stdin, client]

        read, write, error = select.select(sockets, [], sockets)

        for socket in read:
            # reading from server (broadcast from server)
            if socket == client:
                message = receive(client)
                print(message)
            # sending message to server
            else:

                message = sys.stdin.readline()
                message= message.strip("\n")
                if message == DISCONNECT_MESSAGE:
                    flag = False
                send(client, message)
                sys.stdout.flush() 
    
    #client.close()

main()
    


