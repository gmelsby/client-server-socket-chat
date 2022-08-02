# Name: Gregory Melsby
# OSU Email: melsbyg@oregonstate.edu
# Course: CS372 - Introduction to Computer Networks / Section 400
# Assignment: Project 5: Client Server Chat
# Due Date: 08/07/2022
# Description: Simple program that uses a socket to be a server for client/server chat

# Citation
# https://docs.python.org/3/howto/sockets.html

from socket import *

def main():
    # sets up variables to be used later
    # at top for easy modification
    # use a random port number above 1023 (below is reserved)
    port = 5834
    # socket will be bound to 127.0.0.1 for local access
    host = "127.0.0.1"

    # socket the server will listen to new connections on
    listening_socket = socket(AF_INET, SOCK_STREAM)
    # Citation for following line:
    # Date: 08/07/2022
    # Adapted from https://stackoverflow.com/questions/4465959/python-errno-98-address-already-in-use
    # Allows immediate reuse of socket
    listening_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    listening_socket.bind((host, port))

    # only allow one connection at a time
    # if more connections are attempted, rejects
    listening_socket.listen(1)
    
    # prints message with address of site
    print(f"Chat operational. Connect client to http://127.0.0.1:{port}")

    # makes new socket to handle connection to client
    client_socket, addr = listening_socket.accept()   

    closed_flag = False

    # loop for chat
    while True:

        # loop to get message length
        incoming_header = []
        expected_bytes = -1
        while expected_bytes == -1:
            received_char = client_socket.recv(1)
            # case where other socket closed
            if received_char == 0:
                closed_flag = True
                break

            received_char = received_char.decode()
            if received_char == '!':
                # assemble header
                incoming_header = ''.join(incoming_header)
                expected_bytes = int(incoming_header, 16)

            else:
                incoming_header.append(received_char)


        # loop to receive payload data
        received_bytes = 0
        incoming_byte_messages = []
        while received_bytes < expected_bytes:
            received_string = client_socket.recv(min(10, expected_bytes - received_bytes))
            # case where server has closed connection
            if received_string == 0:
                closed_flag = True
                break

            received_bytes += len(received_string)
            incoming_byte_messages.append(received_string)
        
        if closed_flag:
            print('client has severed the connection')
            break

        # prints constructed string
        print(b''.join(incoming_byte_messages).decode())


        print('>', end=' ')
        outgoing_message = input()

        if outgoing_message == '/q':
            break

        header = hex(len(outgoing_message.encode()))[2:] + '!'
        outgoing_message = ''.join([header, outgoing_message])

        client_socket.send(outgoing_message.encode())

if __name__ == "__main__":
    main()