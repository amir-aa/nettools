import socket
def run_Server(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(3)
    print(f"listening on {port} for {host}...")
    while True:
       addr= s.accept()
       print(f"{addr[0]}:{addr[1]} has Connected")