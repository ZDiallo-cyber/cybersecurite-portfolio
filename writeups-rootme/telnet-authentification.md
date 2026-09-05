Contexte: Analyse d'un capture reseaux(ch2.pcap) contenant un echange telenet, Objectif: Trouver le mot de passe de l'utilisateur.

Démarche: Ouverture du fichier dans wireshark application du filtre "telnet" pour isoler les paquets du protocole. Comme en Telnet les caractères sont souvent envoyer un par un(chaque frappe clavier= un paquet), donc ont regarde plutôt via clique droit-->Follow-->TCP Stream pour reconctituer la session complète d'un coup,ce sera plus lisible que paquet par paquet

Solution: Mot de passe en clair via TCP Stream, après le prompt "password:": user

Ce que ça démontre: La compréhension du protocole telnet et de sa vulnérabilité(une authentification non chiffrée, comme ftp), utilisation de la fonction "Follow TCP Stream" de wireshark pour reconstituer une session complète plutôt que paquet par paquet, et compréhension du fonction l'écho caractère par caractère en Telnet. 