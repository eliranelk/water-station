import socket
import _sqlite3
import time
from datetime import datetime
from tqdm import tqdm
from random import randint

for i in tqdm (range(5)):
    time.sleep(0.10)

def DB():
    file_name = 'station'
    connection = _sqlite3.connect(file_name)

    msg = '''
    CREATE TABLE IF NOT EXISTS station_status 
    (id INT,
    date text,
    alrm1 INT,
    alrm2 INT,
    PRIMARY KEY(id))  
    '''

    connection.execute(msg)
    connection.commit()
    cursor = connection.cursor()
    cursor.execute("select * from station_status")
    myresult = cursor.fetchall()
    for row in myresult:
        print(row)

    connection.close()



def db_insert(id,status1=0,status2=0):
    file_name = 'station'
    connection = _sqlite3.connect(file_name)
    msg = """ INSERT OR REPLACE INTO station_status (id,date,alrm1,alrm2)
     values (?, ?, ?, ?)""", (id,str(datetime.today().strftime("%d/%m/%Y %H:%M:%S")), status1, status2)
    try:
       connection.execute(*msg)
    except Exception as ex:
        print(ex)
    """except:
       print('error DB')"""
    connection.commit()
    connection.close()


HOST = ""
PORT = 5001
DB()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
s.settimeout(1)
client_list=[]
print("\n****Welcome to the server!****")
time.sleep(1)

while True:
    #print("\twait to connect!")
    try:
        clientsocket, address = s.accept()
        client_list.append(clientsocket)
        print(f"\n****Welcome client: {address}**** \n\tyou are connected! \n")
        clientsocket.send(bytes("\nWelcome to the server!\n", "utf-8"))
        clientsocket.settimeout(1)

    except socket.timeout:
        for con in client_list:
                try:
                    data = con.recv(1024)
                    print(data.decode())
                    txt = data.decode()
                    l_txt = txt.split('\n')
                    id = l_txt [1]
                    status1 = l_txt [2]
                    status2 = l_txt [3]
                    db_insert(id,status1,status2)
                    print(f'client id = {id}, status 1 = {status1}, status 2 = {status2}.')
                    con.send(bytes("\nWelcome to the server!\n", "utf-8"))
                except socket.timeout:
                    pass
                except:
                    print("the client",address,"has disconnect\n")
                    client_list.remove(con)
                    con.close()
