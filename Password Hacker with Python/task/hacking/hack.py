import sys
import socket
import itertools
import string


def main():
    if len(sys.argv) != 3:
        print("Usage: python hack.py <IP> <port>")
        return

    ip = sys.argv[1]
    port = int(sys.argv[2])

    characters = string.ascii_lowercase + string.digits

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))

            for length in range(1, len(characters) + 1):
                for password_tuple in itertools.product(characters, repeat=length):
                    password = ''.join(password_tuple)

                    s.sendall(password.encode())

                    response = s.recv(1024).decode()

                    if response == "Connection success!":
                        print(password)
                        return
                    elif response == "Too many attempts":
                        print("Too many attempts. Aborting.")
                        return

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
