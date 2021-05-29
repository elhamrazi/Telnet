import threading
import os
import socket
from database_handler import *
from datetime import datetime, date
import ssl

IP = socket.gethostbyname(socket.gethostname())
PORT = 23
address = (IP, PORT)
buff_size = 5000
frmt = "utf-8"


def tls_handler(ip, port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('ia.crt', 'ia.key')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((ip, port))
        sock.listen()
        with context.wrap_socket(sock, server_side=True) as ssock:
            while True:
                conn, addr = ssock.accept()
                cmd = conn.recv(buff_size)
                print(cmd[1:].decode())


def get_datetime():
    now = datetime.now()
    curr_time = now.strftime("%H:%M:%S")
    today = date.today()
    strtoday = today.strftime("%d/%m/%Y")
    return curr_time, strtoday


def create_client_thread(conn, addr):
    print(f"**New Connection from {addr}**")
    conn.send("DONE@@Welcome".encode(frmt))

    while True:
        rcvd_data = conn.recv(buff_size).decode()
        rcvd_data = rcvd_data.split()
        # print(rcvd_data)
        cmd = rcvd_data[0]
        print(cmd)
        # print(type(addr))
        is_accepted = False

        if cmd == "exec":
            msg = rcvd_data[1]
            stream = os.popen(msg)
            output = stream.read()
            output = "DONE@@" + output
            conn.send(output.encode())
            print(output)

            is_accepted = True

        if cmd == 'help':

            help_str = "DONE@@upload <filename> : Upload the file\nexec <command>\n" \
                       "send <text> : send plain text message\nencrypt <text> : send encrypted text message" \
                       "\nhistory : show the history\n".encode()
            conn.send(help_str)
            is_accepted = True

        if cmd == 'send':
            msg_str = "DONE@@message received"
            print(*rcvd_data[1:])
            conn.send(msg_str.encode())
            is_accepted = True

        if cmd == 'upload':
            path = rcvd_data[1]
            filename, filesize = path.split("_")
            filesize = int(filesize)
            conn.send("Filename and filesize received".encode())
            size_tmp = 0
            name = f"recvd_{filename}"
            filepath = os.path.join("server_data", name)
            with open(filepath, "wb") as f1:
                while True:
                    data = conn.recv(buff_size)
                    # print(data)
                    size_tmp += len(data)
                    print(size_tmp, " bytes has received so far")
                    if not data:
                        break
                    if data == b'OVER':
                        break
                    f1.write(data)
                    conn.send("Data received".encode())
                    if size_tmp >= filesize:
                        break
            conn.send("DONE@@file is uploaded successfully!!".encode())
            is_accepted = True
            # conn.close()

        if cmd == 'history':
            histories = print_history(mycursor)
            conn.send(("DONE@@" + histories).encode())
            is_accepted = True

        if cmd == "quit":
            print("connection is about to close.")
            conn.send(b"DISCONNECTED@@bye bye")
            is_accepted = True
            break

        if cmd == 'encrypt':
            conn.send("DONE@@encrypted".encode())

        if is_accepted:
            curr_time, strtoday = get_datetime()
            insert_data(mycursor, str(addr[1]), cmd, curr_time, strtoday)

    conn.close()


file_path = "server_path"


print("STARTING...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen()
print("LISTENING...")

t = threading.Thread(target=tls_handler, args=(IP, 6412))
t.start()
while True:
    conn, addr = server_socket.accept()
    thread = threading.Thread(target=create_client_thread, args=(conn, addr))
    thread.start()



