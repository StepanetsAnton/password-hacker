import sys
import socket


def main():
    if len(sys.argv) != 4:
        print("Usage: python hack.py <IP> <port> <message>")
        return

    ip = sys.argv[1]
    port = int(sys.argv[2])
    message = sys.argv[3]

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))

            s.sendall(message.encode())

            response = s.recv(1024).decode()

            print(response)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
