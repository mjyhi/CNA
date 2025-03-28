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

if __name__ == "__main__":
    main()
