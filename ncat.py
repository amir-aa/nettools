import socket,subprocess,testserver,sys
filecontent=''
def netcat(hostname, port, content,filewrite):
    global filecontent
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, int(port)))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        output = run_command(content)

        if len(filewrite):
            try:
                filecontent = str(output.decode())
                make_file(filewrite)
            except Exception as e:
                print(f"making file has an Error!!! \n {e}")
                sys.exit()


        #print(str(output.decode()))
        #data = s.recv(1024)
        if output :
            main()
            #break
        #print ("Received:", repr(data))
   #print ("Connection closed.")
    #s.close()
def run_command(command):
    #trim the newline
    command = command.rstrip()
    # run the command and get the output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT,shell=True)

    except:
        output = "Failed to execute command.\r\n"
    return output


def main():
    check_server=input("Hi . Welcome To RexCAT Powered By rexcom.ir.\n is this a server System?[Y/N] \t")
    if check_server.lower() =='y' or check_server.lower()=='yes':
        h=input("Enter the Host Target (Blank value would be 0.0.0.0) \t ")
        p=input("Enter The Port to listen \t")
        if h=="":
            testserver.run_Server('0.0.0.0',int(p))
        else:
            try:
                testserver.run_Server(h, int(p))
            except:
                print("Something is Wrong! maybe Port is blank \n")
                sys.exit()
    elif(check_server.lower()=='n' or check_server.lower()=='no'):
        target=input("Enter Your Target IP? \t")
        command=input("What You wanna do on the target?? \t ")
        port=input("The Port that is listening on Target ?  ")
        file=input("if you want to save the output of command in a file please enter address? \t")
        netcat(target,port,command,file)

    else:
        print("Please run the program again!! ")
        sys.exit()
def make_file(address):
    global filecontent
    file= open(address,'w+',encoding='utf-8')

    file.write(filecontent)
    print(filecontent)
    #file.newlines()
main()