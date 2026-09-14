Contexte : Challenge "HTML - Code source" (Root-Me), page web avec un formulaire de connexion par mot de passe. Objectif : retrouver le mot de passe permettant de valider le challenge.

Démarche : Affichage du code source de la page via clic droit → "Afficher le code source". Le code contenait un commentaire HTML (`<!-- -->`) dont le texte débordait largement à droite de l'écran, rendant certaines lignes illisibles. En cochant la case "Retour automatique à la ligne" en haut de la vue, le texte s'est réorganisé et a révélé un second commentaire contenant le mot de passe en clair.

Solution : Mot de passe en clair trouvé : "nZ^&@q5&sjJHev0"

Ce que ça démontre : Le réflexe d'analyser systématiquement le code source d'une page web avant de chercher des méthodes plus complexes — des informations sensibles (mots de passe, commentaires de développeurs) peuvent parfois s'y trouver directement en clair.