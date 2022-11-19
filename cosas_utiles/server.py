#link con informacion
# http://pymotw.com/2/socket/tcp.html
# https://steelkiwi.com/blog/working-tcp-sockets/


import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50500))    
#bind()->to associate the socket with the server address. 
# In this case, the address is localhost, referring to the current server, and the port number is 50500

s.listen(1)
#listen()-> puts the socket into server mode
conn, addr = s.accept()
#accept()-> waits for an incoming connection
#   returns an open connection between the server and client, along with the address of the client
while 1:
    data = conn.recv(1024)
    # recv()-> Data is read from the connection 
    if not data:
        break
    data=data.decode()
    data+=" its me"
    data=bytes(data,'utf-8')
    conn.sendall(data)
    # sendall() -> Data is  transmitted from the connection
conn.close()
# close() -> When communication with a client is finished, the connection needs to be cleaned up