import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 5001))
msg = s.recv(1024)
print(msg.decode("utf-8"))

file = open("status2.txt", "r")
data = file.read()
file.close()

try:
    while True:
        print("information from the station:", data)
        s.send(data.encode())
        ret = s.recv(1000)
        time.sleep(1)
except KeyboardInterrupt:
    print("end of program \ngood bye")