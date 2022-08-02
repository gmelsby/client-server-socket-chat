# Name: Gregory Melsby
# OSU Email: melsbyg@oregonstate.edu
# Course: CS372 - Introduction to Computer Networks / Section 400
# Assignment: Project 5: Client Server Chat
# Due Date: 08/07/2022
# Description: Simple program that uses a socket to be a server for client/server chat


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

    # loop for chat
    while True:

        incoming_messages = []
        incoming_header = ''

        expected_chars = -1
        received_characters = 0
        while expected_chars == -1 or received_characters < expected_chars:
            received_string = client_socket.recv(10).decode()
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
            print('client has severed the connection')
        
        # prints constructed string
        print(''.join(incoming_messages))
        
        print('>', end=' ')
        outgoing_message = input()

        if outgoing_message == '/q':
            break

        header = hex(len(outgoing_message))[2:] + '!'
        outgoing_message = ''.join([header, outgoing_message])
        print(f"sending {outgoing_message}")

        client_socket.send(outgoing_message.encode())

if __name__ == "__main__":
    main()