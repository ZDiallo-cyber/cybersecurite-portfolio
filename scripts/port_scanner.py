import socket
import sys
print("Le script démarre")   # ligne de test temporaire
print(f"IP reçue : {sys.argv[1]}")
def scan_port(ip,port):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    resultat=s.connect_ex((ip,port))
    banniere=""
    if resultat==0:
        try:
            banniere=s.recv(1024).decode().strip()
        except:
            banniere="Pas de bannière"
    s.close()
    return resultat==0, banniere

ip=sys.argv[1]
ports= range(1,1025)
for port in ports:
    ouvert,banniere= scan_port(ip,port)
    if ouvert:
        print(f"Port {port} ouvert -{banniere}")
    else:
        print(f"Port {port} fermé")