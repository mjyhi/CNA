# Proxy.py
# Simple HTTP/1.1 Proxy Server with caching
# Author: mjyhi

import sys
import socket

def main():
    if len(sys.argv) != 3:
        print("Usage: python Proxy.py <host> <port>")
        return

    host = sys.argv[1]
    port = int(sys.argv[2])
    print(f"Starting proxy on {host}:{port}")

    # Step 1 set up socket
    
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow reuse of the socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the host and port
    server_socket.bind((host, port))
    
    # Start listening for incoming connections
    server_socket.listen(5)
    print("Proxy server is listening for connections...")
    
    while True:
        # Accept client connection
        client_socket, client_address = server_socket.accept()
        print(f"Received connection from {client_address}")

        # Receive client request (up to 4096 bytes)
        request = client_socket.recv(4096)
        print("Request from client:")
        print(request.decode(errors='ignore'))

        # Close connection (we're not handling the request yet)
        client_socket.close()
        
if __name__ == "__main__":
    main()
