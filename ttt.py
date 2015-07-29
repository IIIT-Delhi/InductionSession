'''
    Simple socket server using threads
'''
 
import socket
import sys
import random
from thread import *
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'


def checkgrid(data):
    grid = list(data)
    grid = [grid[0:3],grid[3:6],grid[6:9]]
    #start winning conditions
    for i in grid:
        for j in i:
            if not (j=='0' or j=='1' or j=='2'):
                return "error parsing the grid"
        if ''.join(i) == '111':
            return "END - Player wins"
        if ''.join(i) == '222':
            return "END - Server wins"

    for i in range(3):
        if grid[0][i]=='1' and grid[1][i]=='1' and grid[2][i]=='1':
            return "END - Player Wins"
        if grid[0][i]=='2' and grid[1][i]=='2' and grid[2][i]=='2':
            return "END - Server Wins"

    if grid[0][0]=='1' and grid[1][1]=='1' and grid[2][2]=='1':
        return "END - Player Wins"
    if grid[0][0]=='2' and grid[1][1]=='2' and grid[2][2]=='2':
        return "END - Server Wins"
    if grid[0][2]=='1' and grid[1][1]=='1' and grid[2][0]=='1':
        return "END - Player Wins"
    if grid[0][2]=='2' and grid[1][1]=='2' and grid[2][0]=='2':
        return "END - Server Wins"

    if not '0' in data:
        return "END - Draw"
    #end winning conditions

    return data

def analyse(data):
    grid = list(data)
    grid = [grid[0:3],grid[3:6],grid[6:9]]
    # print grid

    check1 = checkgrid(data)
    if check1 != data:
        return check1


    indices = [i for i, x in enumerate(data) if x == "0"]

    random_choice = random.choice(indices)

    newdata = list(data)
    newdata[random_choice] = '2'
    newdata = ''.join(newdata)

    check2 = checkgrid(newdata)
    if check2 != newdata:
        return check2
    
    return newdata

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)

        if not data: 
            break
        
        reply = analyse(data)

        conn.sendall(reply)
     
    #came out of loop
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()   


