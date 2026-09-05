Contexte : Analyse d'une capture réseau (ch1.pcap) contenant un échange FTP, objectif : retrouver le mot de passe utilisé.

Démarche : Ouverture du fichier dans Wireshark, application du filtre `ftp` pour isoler les paquets du protocole. Le FTP en clair transmet les identifiants via les commandes USER et PASS — repérage du paquet contenant la commande PASS dans la colonne Info.

Solution : Mot de passe en clair trouvé dans le paquet : cdts3500

Ce que ça démontre : Compréhension du protocole FTP et de sa vulnérabilité (authentification non chiffrée), lecture de capture réseau avec Wireshark, filtrage par protocole.