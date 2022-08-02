# Name: Gregory Melsby
# OSU Email: melsbyg@oregonstate.edu
# Course: CS372 - Introduction to Computer Networks / Section 400
# Assignment: Project 5: Client Server Chat
# Due Date: 08/07/2022
# Description: Simple program that uses a socket to be a client for client/server chat

# Citation
# https://docs.python.org/3/howto/sockets.html

from socket import *

def main():
    # sets up variables to be used later
    # at top for easy modification
    # use port 80 for http
    port = 5834
    host = "127.0.0.1"
    
    # sets up socket and connection
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((host, port))
    
    closed_flag = False

    while True:
        # prompts for message
        print('>', end=' ')
        outgoing_message = input()
        if outgoing_message == '/q':
            break

        # generates header and appends to front of message
        header = hex(len(outgoing_message.encode()))[2:] + '!'
        outgoing_message = ''.join([header, outgoing_message])
        print(f"sending {outgoing_message}")
        server_socket.send(outgoing_message.encode())

        # waits to receive message

        # loop to get message length
        incoming_header = []
        expected_bytes = -1
        while expected_bytes == -1:
            received_char = server_socket.recv(1)
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
            received_string = server_socket.recv(min(10, expected_bytes - received_bytes))
            # case where server has closed connection
            if received_string == 0:
                closed_flag = True
                break

            received_bytes += len(received_string)
            incoming_byte_messages.append(received_string)
        
        if closed_flag:
            print('server has severed the connection')
            break

        # prints constructed string
        print(b''.join(incoming_byte_messages).decode())

if __name__ == "__main__":
    main()