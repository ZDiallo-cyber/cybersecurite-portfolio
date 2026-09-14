Contexte : Analyse d'une capteur réseau(ch3.pcap) contenant un mot de passe utilisateur, Objectif : Trouver le mot de passe de l'autilisateur dans cette capture.

Démarche : Ouverture du fichier ch3.pcap dans Wireshark, application du filtre http pour isoler les requêtes HTTP. En sélectionnant le paquet contenant la requête d'authentification, un onglet "Basic Credentials" est apparu automatiquement en bas de la fenêtre — Wireshark reconnaît et décode lui-même les identifiants HTTP Basic quand ils sont présents dans le paquet.

Solution : Mot de passe trouvé en clair dans l'onglet "Basic Credentials" généré automatiquement par Wireshark, sans besoin de décodage manuel.MDP : Password

Ce que ça démontre : Compréhension du protocole HTTP et de sa vulnérabilité (authentification non chiffrée), lecture de capture réseau avec Wireshark, filtrage par protocole, et découverte des fonctionnalités de reconnaissance automatique de Wireshark pour les identifiants HTTP Basic.