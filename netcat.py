import sys
import socket
import getopt
import threading
import subprocess





# define some global
listen= False
command=False
upload=False
execute=""
target=""
upload_destination =""
port=55502
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def showhelp():
    print ("-l --listen  listen [host]:[port]")

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target,port))
        if len(buffer):
            client.send(buffer)
            while True:
            # now wait for data back
                recv_len = 1
                response = ""
                while recv_len:
                    data = client.recv(4096)
                    recv_len = len(data)
                    response += data
                    if recv_len < 4096:
                        break
                    print(response)
                    buffer= input("")
                    buffer += "\n"

                    client.send(buffer.encode())
    except:
        print("[*] Exception! Exiting.")

        client.close()

def main():
    global listen
    if not len (sys.argv[1:]):
        showhelp()

    else:
        try:
            opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute","target","port","command","upload"])

        except getopt.GetoptError as err:
            print(str(err))
    for o,a in opts:
        if o in ("-h", "--help"):
            showhelp()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

        buffer = sys.stdin.read()
        client_sender(buffer)
    if listen:
        server_loop()
main()

#server.bind(('0.0.0.0',port))
#server.listen(2)

def server_loop():
    global target
    # if no target is defined, we listen on all interfaces
    if not len(target):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(3)
    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler,  args = (client_socket,))
        client_thread.start()
def run_command(command):
    #trim the newline
    command = command.rstrip()
    # run the command and get the output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT,shell=True)
    except:
        output = "Failed to execute command.\r\n"
    return output
def client_handler(client_socket):
    global upload
    global execute
    global command
    if len(upload_destination):
        # read in all of the bytes and write to our destination
        file_buffer = ""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
                # now we take these bytes and try to write them out
            try:
                file_descriptor = open(upload_destination, "wb")
                file_descriptor.write(bytearray(file_buffer))
                file_descriptor.close()
                client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
            except:
                client_socket.send("Failed to save file to %s\r\n" % upload_destination)
            # check for command execution
    if len(execute):
     # run the command
        output = run_command(execute)
        client_socket.send(output)
     # now we go into another loop if a command shell was requested
    if command:
        while True:
            # show a simple prompt
            client_socket.send("Rexnetcat>>")

            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
                # send back the command output
                response = run_command(cmd_buffer)
                # send back the response
                client_socket.send(response)



def handle_client(client_socket):
    #server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("* We are listening on Port 55502")
    while True:
        c, addr = server.accept()
        print( "[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))
        #print( 'Got connection from', addr)

        # send a thank you message to the client.
        c.send(b'Thank you for connecting')
        got=c.recv(1024)
        print(got.decode())

        # Close the connection with the client
        #c.close()


#listen('0.0.0.0',port)