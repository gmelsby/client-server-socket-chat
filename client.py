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
        server_socket.send(outgoing_message.encode())

        # receives response
        incoming_message = server_socket.recv(response_len_max)
        print(incoming_message.decode())

if __name__ == "__main__":
    main()