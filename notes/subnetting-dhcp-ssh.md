# Sous-réseaux, DHCP & SSH

## 1. IPv4 et sous-réseaux

### Structure d'une adresse IPv4
Une adresse IPv4 = 32 bits, écrite en 4 octets décimaux (0-255) séparés par des points.

Elle se divise en deux parties : **partie réseau** + **partie hôte**, séparées par le masque (notation CIDR `/xx`).

### Trouver bits réseau / bits hôte

```
bits réseau = le nombre après le "/" (ex: /26 → 26 bits réseau)
bits hôte   = 32 − bits réseau
taille du bloc = 2^(bits hôte)
adresses utilisables = 2^(bits hôte) − 2
```

Le −2 s'explique par deux adresses toujours réservées dans un bloc :
- **1ère adresse** = adresse réseau → désigne le sous-réseau lui-même, jamais une machine
- **Dernière adresse** = adresse broadcast → veut dire "tout le monde en même temps", jamais une seule machine

### Table CIDR à connaître par cœur (/24 à /30)

| CIDR | Masque décimal | Taille bloc | Utilisables |
|---|---|---|---|
| /24 | 255.255.255.0 | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 126 |
| /26 | 255.255.255.192 | 64 | 62 |
| /27 | 255.255.255.224 | 32 | 30 |
| /28 | 255.255.255.240 | 16 | 14 |
| /29 | 255.255.255.248 | 8 | 6 |
| /30 | 255.255.255.252 | 4 | 2 |

Astuce : la taille du bloc est divisée par 2 à chaque cran (256→128→64→32→16→8→4).

Le `/30` (2 adresses utilisables) sert typiquement pour un **lien point-à-point entre 2 routeurs** — exactement 2 IP nécessaires, pas de gaspillage.

### Découper un réseau en N sous-réseaux

```
1. Trouver les bits à emprunter : 2^(bits) ≥ N
2. Nouveau CIDR = CIDR de départ + bits empruntés
3. Taille de chaque bloc = 2^(nouveaux bits hôte)
4. Lister les blocs par paliers de cette taille
```

⚠️ Piège classique : si N n'est pas une puissance de 2 (ex: 5 ou 6 sous-réseaux voulus), on crée toujours **plus** de sous-réseaux que demandé (le nombre supérieur en puissance de 2), les blocs en trop restent en réserve.

⚠️ Si on part d'un `/16` (ou moins), les bits empruntés tombent sur l'octet suivant la partie réseau fixe (ex: 3ᵉ octet pour un /16), pas forcément le dernier octet.

### VLSM (Variable Length Subnet Mask)

Cas d'entreprise : découper un réseau en sous-réseaux de **tailles différentes** selon les besoins réels de chaque service.

Règle : toujours allouer le **plus gros bloc en premier**, chaque bloc démarre juste après la fin du précédent (pas de paliers fixes réguliers comme un découpage classique).

Exemple (`192.168.20.0/24`, 3 services) :

| Service | Besoin | CIDR | Réseau | Broadcast | Plage utilisable |
|---|---|---|---|---|---|
| Compta | 50 machines | /26 (62 util.) | .0 | .63 | .1 à .62 |
| Technique | 20 machines | /27 (30 util.) | .64 | .95 | .65 à .94 |
| Direction | 5 machines | /29 (6 util.) | .96 | .103 | .97 à .102 |

---

## 2. DHCP (Dynamic Host Configuration Protocol)

Attribue automatiquement une config IP (IP, masque, passerelle, DNS, durée de bail) à une machine qui rejoint le réseau, sans configuration manuelle.

### Processus DORA

```
Client                          Serveur DHCP
  |----(1) DISCOVER (broadcast)----->|   "Je cherche un serveur DHCP"
  |<---(2) OFFER----------------------|   "Voici une IP disponible"
  |----(3) REQUEST (broadcast)------->|   "Je confirme vouloir cette IP"
  |<---(4) ACK-------------------------|  "Validé, voici la config complète"
```

- **Discover en broadcast** : le client n'a pas encore d'IP, il ne peut adresser aucun serveur précis
- **Request en broadcast** : permet aux autres serveurs DHCP (s'il y en a plusieurs) de savoir que leur offre n'a pas été retenue

### Vocabulaire clé
- **Scope/pool** : plage d'IP distribuable par le serveur
- **Reservation** : IP fixe associée à une adresse MAC précise (serveurs, imprimantes)
- **Lease time** : durée avant renouvellement obligatoire de l'IP

### Angle sécurité
- **DHCP starvation** : un attaquant sature le pool d'IP avec de faux Discover (fausses adresses MAC) → déni de service, plus personne ne peut obtenir d'IP
- **Rogue DHCP** : un attaquant installe un faux serveur DHCP qui répond plus vite que le vrai → il distribue sa propre passerelle/DNS → man-in-the-middle sur tout le trafic de la victime

---

## 3. SSH (Secure Shell)

Protocole de connexion distante **chiffrée** (port 22 par défaut), remplace Telnet qui envoie tout en clair (identifiants inclus).

### Établissement de la connexion
1. **Échange de clés** (Key Exchange / Diffie-Hellman) : client et serveur négocient un secret partagé sans jamais l'envoyer directement sur le réseau
2. **New Keys** : marque la fin de la négociation — à partir de ce paquet, **tout le trafic est chiffré**
3. **Authentification du client** : par mot de passe ou par clé publique/privée

### Méthodes d'authentification

| Méthode | Description | Sécurité |
|---|---|---|
| Mot de passe | `ssh user@serveur` | Vulnérable au brute-force |
| Clé publique/privée | `ssh-keygen` + `ssh-copy-id` | Recommandée en entreprise — la clé privée ne quitte jamais la machine |

### Angle sécurité / pentest
- Port 22 souvent scanné/bruteforcé en premier par les attaquants
- Bonne pratique : désactiver l'authentification par mot de passe, n'autoriser que les clés
- **Fail2ban** : bannit automatiquement une IP après X échecs de connexion SSH

### Démonstration pratique (labo Kali/Metasploitable, capture Wireshark)

Comparaison SSH vs Telnet sur le même labo :

| | Telnet | SSH |
|---|---|---|
| Mot de passe visible dans Wireshark | ✅ Oui, en clair (confirmé par capture + Follow TCP Stream) | ❌ Non, chiffré dès le paquet "New Keys" |
| Commandes tapées visibles | ✅ Oui | ❌ Non |
| Vol d'identifiants par sniffing | ✅ Trivial | ❌ Impossible sans casser le chiffrement |

Sur la capture Telnet réelle, le login apparaît lettre par lettre en double (client + echo serveur), et le mot de passe apparaît en clair en une seule couleur (écho désactivé pendant la saisie du mot de passe, mais le paquet réseau contient quand même la valeur en clair).

---

## Exercices de calcul de sous-réseaux (auto-évaluation)

1. `192.168.10.0/28` → réseau, broadcast, plage utilisable, nb d'adresses utilisables ?
2. Découper un `/24` en 5 sous-réseaux → combien de bits emprunter, combien de sous-réseaux réellement créés ?
3. Pourquoi la 1ère et la dernière adresse d'un bloc ne sont-elles jamais assignables à une machine ?
4. Explique le processus DORA en une phrase par étape.
5. Différence entre DHCP starvation et rogue DHCP ?
6. Pourquoi SSH est-il sécurisé alors que Telnet ne l'est pas ?
7. Les deux méthodes d'authentification SSH, laquelle est recommandée en entreprise et pourquoi ?
8. À partir de quel paquet le trafic SSH devient-il illisible dans Wireshark, et pourquoi ?
9. Pourquoi le DHCP Discover est-il en broadcast plutôt qu'en unicast ?
10. Un `/30` est utilisé pour quel cas concret, et pourquoi cette taille précisément ?
