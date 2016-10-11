import socket
sock = socket.socket()
sock.bind(("127.0.0.1", 5000))
sock.listen(3)
print("listen\n")

conn, addr = sock.accept()
while 1:
    data = conn.recv(1000)
    udata = data.decode("utf=8")
    if udata == "exit": break
    print("Data: " + udata)
    res = input()
    conn.send(bytes(res, "utf=8"))
conn.close()
