import socket,time,datetime
import threading


SECONDS=5
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.settimeout(8)
def WriteLog(target:str):
    with open('uptime_log.txt','a')as fil:
        fil.write(f'[x]{datetime.datetime.now()} Error Accessing {target}\n')
        fil.close()
def Check(addr,port):
        while 1:
            target=(addr,int(port))
            #print(f'Check {addr} port {port}')
            if not sock.connect_ex(target)== 0:
                    
                    WriteLog(f"{addr} Port {port}")
            time.sleep(SECONDS)

with open('monitor.txt','r') as f: 
    Targets=[]

    for line in f.readlines():
        addr,port=line.split(':')
        Targets.append(threading.Thread(target=Check,args=(addr,port,)))
