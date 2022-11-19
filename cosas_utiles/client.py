
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50500))
# connect()->  to attach the socket directly to the remote address.
mesage='Hello, world'
mesage=bytes(mesage,'utf-8')
s.sendall(mesage)
 # sendall() -> Data is  transmitted from the connection
data = s.recv(1024)
# recv()-> Data is read from the connection 
s.close()
# close() -> When communication with a client is finished, the connection needs to be cleaned up
print ('Received', repr(data))