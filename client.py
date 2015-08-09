import socket
import sys
import os

def reference():
	print 'Use board as reference. Enter position number for next move'
	print "0|1|2"
	print "3|4|5"
	print "6|7|8\n"

def prettyprint(board):
	curr = list(board)
	for j in [0,3,6]:
		for i in range(0,3):
			if curr[i+j] is '0':
				print ' ',
			elif curr[i+j] is '1':
				print 'x',
			elif curr[i+j] is '2':
				print 'o',
			print '|',
		print ''

def move(board):
	prettyprint(board)
	cur = list(board)
	mymove = raw_input('Enter next move: ')
	if mymove >=0 and mymove <=8:
		if cur[int(mymove)] == '0':
			cur[int(mymove)] = '1'
			cur = ''.join(cur)
			return cur
	else:
		print 'Invalid move'
		move(board)

s = socket.socket()

try:
	addr = ('192.168.1.133',8888)
	s.connect(addr)
	print 'Connected to Server'
except socket.error as msg:
    print 'Error : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
board = '00000000000'
mymove = move(board)
s.sendall(mymove)

board = s.recv(50)

while 'END' not in board and 'WIN 1' not in board and 'WIN 2' :
	os.system('clear')
	reference()
	mymove = move()
	s.sendall(mymove)
	board = s.recv(50)

if 'END' in board:
	print board
















