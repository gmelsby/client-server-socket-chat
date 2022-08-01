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
    print(f"Chat operational. Connect at http://127.0.0.1:{port}")

    # makes new socket to handle each client
    client_socket, addr = listening_socket.accept()   

    # loop for chat
    while True:

        # receives incoming request and prints it
        incoming_message = client_socket.recv(1024).decode()
        print(incoming_message)
        
        print('>', end=' ')
        outgoing_message = input()
        client_socket.send(outgoing_message.encode())

    # close each individual connection to client after use
    # does not close the listening socket, so more connections can be made
    # Citation for following line:
    # Date: 06/30/2022
    # URL: according to https://docs.python.org/3/howto/sockets.html, it is polite to call shutdown before closing
    client_socket.shutdown(SHUT_RDWR)
    client_socket.close()
    
if __name__ == "__main__":
    main()