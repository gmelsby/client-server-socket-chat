# Name: Gregory Melsby
# OSU Email: melsbyg@oregonstate.edu
# Course: CS372 - Introduction to Computer Networks / Section 400
# Assignment: Project 5: Client Server Chat
# Due Date: 08/07/2022
# Description: Simple program that uses a socket to be a client for client/server chat


from socket import *

def main():
    # sets up variables to be used later
    # at top for easy modification
    # use port 80 for http
    port = 5834
    host = "127.0.0.1"
    # indicates that the maximum amount of bytes to receive is 2048
    response_len_max = 2048
    
    # sets up socket and connection
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((host, port))
    
    while True:
        # prompts for message
        print('>', end=' ')
        outgoing_message = input()
        if outgoing_message == '/q':
            break

        header = hex(len(outgoing_message))[2:] + '!'
        outgoing_message = ''.join([header, outgoing_message])
        print(f"sending {outgoing_message}")
        server_socket.send(outgoing_message.encode())

        incoming_messages = []
        incoming_header = ''

        expected_chars = -1
        received_characters = 0
        while expected_chars == -1 or received_characters < expected_chars:
            received_string = server_socket.recv(10).decode()
            if not received_string:
                incoming_messages.append(0)
                break

            if expected_chars == -1:
                incoming_header += received_string

                if '!' in incoming_header:
                    split_header = incoming_header.split('!', 1)
                    expected_chars = int(split_header[0], 16)
                    if len(split_header) > 1:
                        incoming_messages.append(split_header[1])
                        received_characters += len(split_header[1])
                
                continue

            received_characters += len(received_string)
            incoming_messages.append(received_string)
        
        if not incoming_messages[-1]:
            print('server has severed the connection')
            break

        # prints constructed string
        print(''.join(incoming_messages))

if __name__ == "__main__":
    main()