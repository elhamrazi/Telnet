import socket
import base64
SIZE = 1024
FORMAT = "utf-8"
CRLF = "\r\n"


class Mail:

    def send_mail(self):
        user = input(">user name: ")
        password = input(">password: ")
        email_address = input(">your email address: ")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to mail server...")
        s.connect(("mail.aut.ac.ir", 587))
        print("Connected successfully.")

        # establishing the connection
        recv_msg = s.recv(SIZE).decode(FORMAT)
        print(recv_msg)
        reply = recv_msg[:3]
        if reply != '220':
            print("220 reply is not received from server.")

        # helo command
        helo = "EHLO Elham"+CRLF
        s.send(helo.encode(FORMAT))
        recv_msg = s.recv(SIZE).decode()
        print("EHLO command sent")
        print(recv_msg)
        reply = recv_msg[:3]
        if reply != '250':
            print("250 reply was not received from server.")

        # Authentication
        userpass = base64.b64encode(("\x00"+user+"\x00"+password).encode())
        auth = "AUTH PLAIN ".encode(FORMAT)
        auth = auth + userpass + CRLF.encode(FORMAT)
        s.send(auth)

        # Check Sender and Recipient
        s.send(("MAIL FROM:<"+email_address+">"+CRLF).encode(FORMAT))
        recv_msg = s.recv(SIZE).decode()
        print(recv_msg)
        recipient = "RCPT TO:<"+email_address+">"+CRLF
        s.send(recipient.encode())
        recv_msg = s.recv(SIZE).decode()
        print(recv_msg)

        # Data Command
        data = "DATA"+CRLF
        s.send(data.encode())
        recv_msg = s.recv(SIZE).decode()
        print(recv_msg)

        # Send mail
        mail_subj = "Subject: test email" + CRLF + CRLF
        s.send(mail_subj.encode())
        s.send((CRLF+" Hi from Elham to Elham!").encode())
        s.send("\r\n.\r\n".encode())
        recv_msg = s.recv(SIZE).decode()
        print(recv_msg)

        # Close Connection
        quit_server = "QUIT"+CRLF
        s.send(quit_server.encode())
        recv_msg = s.recv(SIZE).decode()
        print(recv_msg)
        s.close()



