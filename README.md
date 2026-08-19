
# Portfolio Cybersécurité — Zakaria Diallo

Labo personnel et projets pratiques réalisés dans le cadre de ma préparation à une alternance en cybersécurité (rentrée 2027-2028), actuellement en Prépa Cycle Ingénieur à ESIEE-IT.

Tout le contenu de ce repo est produit sur un environnement de laboratoire personnel isolé (VirtualBox — Kali Linux, Metasploitable, Windows Server), à des fins d'apprentissage.

## 🧰 Scripts Python

| Script | Description |
|---|---|
| [`scripts/port_scanner.py`](scripts/port_scanner.py) | Scanner de ports TCP avec récupération de bannières de service, plage de ports configurable, arguments en ligne de commande |
| [`scripts/ssh_bruteforce.py`](scripts/ssh_bruteforce.py) | Outil de test d'authentification SSH par wordlist (Paramiko), avec gestion des erreurs de compatibilité de chiffrement |
| [`scripts/log_analyzer.py`](scripts/log_analyzer.py) | Détecteur de brute-force par analyse de journaux d'authentification : extraction par expressions régulières, classification de gravité, génération de rapport |

## 📚 Notes techniques

| Fiche | Contenu |
|---|---|
| [`notes/fiche_cybersecurite_zak.md`](notes/fiche_cybersecurite_zak.md) | Modèle OSI, TCP/IP, ARP, DNS, HTTP/HTTPS, Wireshark, Nmap, Metasploit, John the Ripper, GoPhish, commandes Linux essentielles |
| [`notes/subnetting-dhcp-ssh.md`](notes/subnetting-dhcp-ssh.md) | Sous-réseaux IPv4 (calcul, VLSM), DHCP (processus DORA, angle sécurité), SSH vs Telnet (démonstration Wireshark) |

## 🖥️ Labo Active Directory

Mise en place d'un environnement Active Directory complet :
- Contrôleur de domaine (Windows Server 2025), structure avec unités d'organisation, comptes et groupes de sécurité
- Énumération depuis Kali Linux (Nmap, CrackMapExec/NetExec, Impacket, smbclient)
- Exploration des protections modernes de Windows Server 2025 face aux techniques classiques (Kerberoasting, collecte BloodHound) — voir [`active-directory/notes-labo-ad.md`](active-directory/notes-labo-ad.md)

## 🎯 Compétences couvertes

Réseaux (OSI, TCP/IP, sous-réseaux, VLSM) · DHCP/DNS/ARP · SSH/Telnet · Nmap · Metasploit · John the Ripper · GoPhish · Active Directory · CrackMapExec/Impacket · Python (scripting, regex, gestion d'erreurs) · Wireshark

---

*Ce repo est mis à jour au fil de ma progression.*
86e12d9 (Ajout scripts Python, notes reseaux et structure du portfolio)
