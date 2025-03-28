# Proxy.py
# Simple HTTP/1.1 Proxy Server with caching
# Author: mjyhi

import sys
import socket
#Step 2
import urllib.parse
#Step 3
import os


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
        decoded_request = request.decode(errors='ignore')
        print("Request from client:")
        print(request.decode(errors='ignore'))
        
        # Step 2 Parse the requested URL from the request line
        
        try:
            request_lines = request.decode(errors='ignore').split('\r\n')
            request_line = request_lines[0]
            print("Request line:", request_line)
            
            method, full_url, version = request_line.split()
            url = full_url.lstrip('/')  # remove leading "/"
            parsed_url = urllib.parse.urlparse(url)

            target_host = parsed_url.hostname
            target_port = parsed_url.port if parsed_url.port else 80
            target_path = parsed_url.path
            
            if parsed_url.query:
                target_path += '?' + parsed_url.query

            print(f"Target host: {target_host}")
            print(f"Target port: {target_port}")
            print(f"Target path: {target_path}")

        except Exception as e:
            print("Failed to parse request:", e)
            client_socket.close()
            continue
        
        # Step 3: Check if file is cached
        cache_dir = "cache"
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # If path is just '/', we use index.html
        filename = target_path.strip("/").replace("/", "_")
        if not filename:
            filename = "index.html"

        cache_file_path = os.path.join(cache_dir, f"{target_host}_{filename}")

        if os.path.exists(cache_file_path):
            print(f"Cache hit: {cache_file_path}")

        with open(cache_file_path, "rb") as cached_file:
            cached_data = cached_file.read()

        # Send basic HTTP 200 OK header + cached content
        response = b"HTTP/1.1 200 OK\r\n"
        response += b"Content-Length: " + str(len(cached_data)).encode() + b"\r\n"
        response += b"Connection: close\r\n\r\n"
        response += cached_data

        client_socket.sendall(response)
        print("Sent cached response to client.")

        client_socket.close()
        continue  # Skip contacting origin server (we'll do that in Step 4)
        
if __name__ == "__main__":
    main()
