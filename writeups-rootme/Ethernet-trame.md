Contexte: Analyse d'une capture réseau(ch12.txt) contenant une authentification http basic, Objectif: retrouver les données normalement confidentielles contenues dans cette trame.

Démarche : Comme le fichier était un fichier .txt et non un .pcap, je suis passé de Wireshark à CyberChef avec l'opération "From Hex" pour obtenir du texte lisible. J'ai repéré une requête HTTP contenant une ligne "Authorization: Basic ...". Sachant que l'authentification HTTP Basic encode toujours les identifiants en Base64, j'ai ajouté l'opération "From Base64" pour décoder cette chaîne.

Solution: le résultat obtenus(confi:dential) montre qu'il s'agit d'un couple d'identifiant:mot de passe.

Ce que ça démontre: La reconnaissance d'un format de fichier brut(hexa) nécessitant un outil de conversion, l'utilisation de Cyberchef pour enchainer plusieurs decodages, la connaissance du protocole HTTP et de sa méthode d'authentification Basic