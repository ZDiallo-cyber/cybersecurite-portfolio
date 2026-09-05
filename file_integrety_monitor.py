import hashlib
import json
import os

def calculer_hash(chemin):
    with open(chemin,"rb") as fichier:
      contenu=fichier.read()

    empreinte=hashlib.sha256(contenu).hexdigest()
    return empreinte

def creer_baseline_dossier(dossier):
    if not os.path.exists(dossier):
        print("ERREUR : le dossier n'existe pas.")
        return
    
    fichiers=os.listdir(dossier)
    baseline={}
    for nom_fichier in fichiers:
        chemin_complet = os.path.join(dossier, nom_fichier)
        if not os.path.isfile(chemin_complet):
            continue
        hash_fichier= calculer_hash(chemin_complet)
        baseline[chemin_complet]=hash_fichier
    with open("baseline.json", "w", encoding="utf-8") as fichier:
       json.dump(baseline,fichier,indent=4)

def verifier_dossier(dossier):
   if not os.path.exists(dossier):
       print("ERREUR : le dossier surveillé n'existe pas.")
       return
   
   try:
    with open("baseline.json", "r", encoding="utf-8") as fichier:
        baseline=json.load(fichier)
   except FileNotFoundError:
       print("Aucune baseline n'a été trouvé!")
       return
   except json.JSONDecodeError:
       print("ERREUR : le fichier baseline.json est corrompu.")
       return
   
   
   fichiers_actuels=os.listdir(dossier)
   for nom_fichier in fichiers_actuels:
        chemin_complet=os.path.join(dossier,nom_fichier)
        if not os.path.isfile(chemin_complet):
            continue
        nouveau_hash=calculer_hash(chemin_complet)
        if chemin_complet not in baseline:
            print(f" NOUVEAU FICHIER : {nom_fichier}")
        elif baseline[chemin_complet]!=nouveau_hash:
            print (f"ALERTE : {nom_fichier} a été modifié")
        else:
            print(f"OK : {nom_fichier} est intact")
   for ancien_chemin in baseline:
       if not os.path.exists(ancien_chemin):
           print(f"FICHIER SUPPRIMÉ : {ancien_chemin}")
# while True:
#     print("=" * 40)
#     print("       FILE INTEGRITY MONITOR")
#     print("=" * 40)
#     print()
#     print("1 - Créer une nouvelle baseline")
#     print("2 - Vérifier l'intégrité du dossier")
#     print("3 - Quitter")
#     choix= input("Choisissez une option : ")
#     if choix=="1":
#         creer_baseline_dossier("dossier_surveille")
#         print("Baseline créée avec succès.")
#     elif choix=="2":
#         verifier_dossier("dossier_surveille")
#     elif choix=="3":
#         print("Fermeture du programme.")
#         break
#     else:
#         print("Option invalide.")
for racine, dossiers, fichiers in os.walk("dossier_surveille"):
    print("Racine :", racine)
    print("Dossiers :", dossiers)
    print("Fichiers :", fichiers)
    print("--------------------")