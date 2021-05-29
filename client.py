import os
import socket
import time
from mail_client import Mail
import dns.resolver
import ssl
from tqdm import tqdm


IP = socket.gethostbyname(socket.gethostname())
PORT = 23
address = (IP, PORT)
buff_size = 5000
frmt = "utf-8"


while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    while True:
        data = sock.recv(buff_size).decode()
        # print(data)
        command, msg = data.split("@@")

        if command == "DONE":
            print(msg)
        elif command == "DISCONNECTED":
            print(msg)
            break

        input_str = input("telnet ")
        data = input_str.split()
        cmd = data[0]
        print(cmd)

        # implementing different commands

        if cmd == 'exec':
            cmd_type = data[1]
            print(cmd_type)
            sock.send(input_str.encode())

        if cmd == 'help':
            sock.send(cmd.encode())

        if cmd == 'send':
            plain_msg = data[1]
            sock.send(input_str.encode())

        if cmd == 'upload':
            f_name = data[1]
            f_size = os.path.getsize(f_name)
            input_str += "_" + str(f_size)
            sock.send(input_str.encode())
            msg = sock.recv(buff_size).decode()
            print(msg)

            with open(f_name, "rb") as f:
                while True:
                    dt = f.read(buff_size)

                    if not dt:
                        sock.send("OVER".encode())
                        break
                    sock.sendall(dt)
                    mesg = sock.recv(buff_size).decode()
                    print(mesg)

        if cmd == 'history':
            sock.send(cmd.encode())

        if cmd == "quit":
            sock.send(cmd.encode())

        if cmd == "encrypt":
            context = ssl.SSLContext()

            with socket.create_connection((IP, 6412)) as sock1:
                with context.wrap_socket(sock1, server_hostname=IP) as ssock:
                    print(ssock.version())

            # sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # sock1.connect((IP, 6412))
                    ssock.send(input_str.encode())
                    print(type(ssock))
                    print(type(sock1))
            sock.send(cmd.encode())
            # sock1.close()
            # continue

        # print("Connection lost")
    sock.close()


