import os
import socket
import time
from mail_client import Mail
import dns.resolver


IP = socket.gethostbyname(socket.gethostname())
PORT = 23
address = (IP, PORT)
buff_size = 5000
frmt = "utf-8"


while True:
    print("WELCOME!")
    print("Send Request to:\n1-web server\n2-mail server\n3-scan ip for open ports")
    c = input(">")

    if c == '1':
        print("You can use http requests HEAD and GET for now!")
        print("command structure: <Request type> <host> <port number>")
        cmd = input("Telnet> ").split()
        host = cmd[1]
        target_port = int(cmd[2])
        command = cmd[0]
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, target_port))
        request = command + " / HTTP/1.1\r\nHost:+ " + host + "\r\nAccept: text/html\r\n\r\n"
        client.sendall(request.encode())
        print(str(client.recv(buff_size), frmt))
        client.close()

    if c == '2':
        mail_servers = []
        domain = 'aut.ac.ir'
        for x in dns.resolver.resolve(domain, 'MX'):
            print(x)
            mail_servers.append(x)
        email = Mail()
        email.send_mail()

    if c == '3':
        hosts = []
        print("Enter host(s) you wish to be scanned.")
        while True:
            host = input()
            if host == "":
                break
            hosts.append(host)
        start_time = time.time()
        for h in hosts:
            target_host = socket.gethostbyname(h)
            print("starting scan for host:", target_host)

            for i in range(1, 1025):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                conn = s.connect_ex((target_host, i))
                if conn == 0:
                    print('Port %d: OPEN' % (i,))
                s.close()

            print("Time taken:", time.time() - start_time)







