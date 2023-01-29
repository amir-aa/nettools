import select,socket,queue
s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
BADDRESS='127.0.0.1'
PORT=300
s.bind((BADDRESS,PORT))
s.listen(5)
message_queues={}
inputs=[s]
outputs=[]
while inputs:
    myinput,myoutput,myexcept = select.select(inputs,outputs,[])
    for sock in myinput:
        if sock is s:
            
            conn,addr=sock.accept()
            sock.setblocking(False)
            inputs.append(conn)
            message_queues[conn]=queue.Queue()
        else:
            data=sock.recv(1024)
            if data:
                message_queues[sock].put(data)
                #print(data.decode())
                if sock not in outputs:
                    outputs.append(sock)
            else:
                if sock in outputs:
                    outputs.remove(sock)
                inputs.remove(sock)
                sock.close()
                del message_queues[sock]
for sock in myoutput:
    try:
        next_msg=message_queues[sock].get_nowait()
    except queue.Empty:
        outputs.remove(sock)
    else:
        sock.send(next_msg)
for sock in myexcept:
    inputs.remove(sock)
    if sock in outputs:
        outputs.remove(sock)
    sock.close()
    del message_queues[sock]







