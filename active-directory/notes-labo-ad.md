# Labo Active Directory — Compte-rendu

> Environnement : Windows Server 2025 (contrôleur de domaine) + Kali Linux, réseau Host-Only VirtualBox (192.168.56.0/24), aux côtés de Metasploitable.

## 1. Mise en place du contrôleur de domaine

- Installation de Windows Server 2025 (Standard Evaluation, Desktop Experience) sur VirtualBox
- Configuration réseau : IP statique sur l'interface Host-Only, carte NAT séparée pour l'accès Internet
- Installation du rôle **Active Directory Domain Services (AD DS)**
- Promotion du serveur en contrôleur de domaine — création d'une nouvelle forêt/domaine `labo.local`

## 2. Structure Active Directory

- Création d'une **Unité d'Organisation (OU)** `IT`
- Création de comptes utilisateurs (ex: `jdupont`, `msmith`) au sein de cette OU
- Création d'un **groupe de sécurité** `IT-Admins`, avec ces comptes comme membres
- Création d'un compte de service (`svc-sql`) avec un **SPN** associé (`MSSQLSvc/labo.local:1433`), pour expérimenter le principe du Kerberoasting

## 3. Énumération depuis Kali Linux

Reconnaissance réalisée avec des identifiants de domaine valides (compte utilisateur standard, sans droits d'administration) :

- **Nmap** (`nmap -p- <ip>`) : identification de la signature typique d'un contrôleur de domaine (ports 53 DNS, 88 Kerberos, 389 LDAP, 445 SMB, 464 kpasswd, 636 LDAPS, 3268/3269 Global Catalog...)
- **CrackMapExec / NetExec** : validation d'identifiants via SMB, énumération des partages réseau disponibles et des permissions associées (`--shares`)
- **smbclient** : exploration du partage `SYSVOL` (structure des GPO — `Policies`, `MACHINE`, `USER`, fichiers `Registry.pol`, `GPT.INI`)

## 4. Tentatives d'attaque et limites rencontrées

Deux techniques classiques ont été testées et ont révélé des protections modernes bloquant les méthodes "legacy" habituellement documentées dans les tutoriels (souvent basés sur Windows Server 2016/2019) :

### Kerberoasting (Impacket `GetUserSPNs`)
- SPN correctement identifié sur le compte `svc-sql`
- Échec de récupération du ticket TGS : `KDC_ERR_ETYPE_NOSUPP` (type de chiffrement non supporté)
- Persistant même après activation d'AES 128/256 sur le compte et modification de la stratégie de chiffrement Kerberos locale
- **Conclusion** : Windows Server 2025 semble imposer par défaut des restrictions de chiffrement (probable désactivation de RC4) qui cassent la méthode Kerberoasting classique en l'état

### Collecte BloodHound (bloodhound-python)
- Installation de BloodHound CE via Docker, interface fonctionnelle
- Échec de la collecte LDAP : `LDAPSocketOpenError` lié au **LDAP channel binding / signing**, activé par défaut
- **Conclusion** : la collecte nécessiterait le collecteur officiel **SharpHound** exécuté depuis une machine Windows jointe au domaine, plutôt qu'un outil Linux — piste à explorer dans une prochaine itération du labo (ajout d'une VM Windows cliente)

## 5. Enseignement principal

Au-delà des techniques elles-mêmes, ce labo a permis de constater concrètement que les **durcissements de sécurité par défaut** des versions récentes de Windows Server changent la donne par rapport aux attaques "manuel de pentest classique" — une nuance rarement mise en avant dans les tutoriels grand public, mais représentative de ce qu'un environnement d'entreprise moderne peut opposer à un attaquant.

---

*Prochaines pistes : ajout d'une VM Windows cliente jointe au domaine, test de SharpHound, ajustement de la stratégie de chiffrement Kerberos du domaine pour reproduire l'attaque Kerberoasting classique.*