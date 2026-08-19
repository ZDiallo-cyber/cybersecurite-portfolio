import re
from datetime import datetime 

motif=r"\d+\.\d+\.\d+\.\d+"
motif_heure=r"\d{2}:\d{2}:\d{2}"
motif_user=r"for (\w+) from"

ROUGE="\033[31m"
VERT="\033[32m"
JAUNE="\033[33m"
CYAN="\033[36m"
RESET="\033[0m"
seuil=4
fenetre=60

def analyser_logs(Nom_Fichier):

    compteur={}
    heure_ip={}
    users_ip={}
    Lignes_ignorees=[]

    try:
     with open(Nom_Fichier, "r") as fichier:
      for ligne in fichier:

        if"Failed password" in ligne:
            resultat=re.search(motif,ligne)
            resultat_heure=re.search(motif_heure,ligne)
            resultat_user=re.search(motif_user,ligne)

            if resultat and resultat_heure and resultat_user:

                ip=resultat.group()
                heure=resultat_heure.group()
                user=resultat_user.group(1)
              
                if verifier_ip(ip):

                 if ip in heure_ip:
                     heure_ip[ip].append(heure)
                 else: 
                   heure_ip[ip]=[heure]
                  
                 if ip in compteur:
                     compteur[ip]+=1
                 else:
                  compteur[ip]=1

                  if ip in users_ip:
                     users_ip[ip].append(user)
                  else:
                     users_ip[ip]=[user]

                else:
                   Lignes_ignorees.append(f"IP invalide: {ip}")
            else:
                Lignes_ignorees.append(ligne.strip())
                
    except FileNotFoundError:
      print(f"ERREUR : le fichier {Nom_Fichier} est introuvable")
    return compteur, heure_ip, users_ip,Lignes_ignorees


def detecter_bruteforce(compteur,heure_ip,users_ip,seuil,fenetre):
  
  suspects=[]
  
  for ip,tentatives in compteur.items():
     heures=heure_ip[ip]

     if tentatives >=seuil:
         for i in range(len(heures)-seuil + 1):
             
             premiere=heures[i]
             derniere=heures[i+seuil-1]

             debut=premiere
             fin=derniere

             premiere=datetime.strptime(premiere,"%H:%M:%S")
             derniere=datetime.strptime(derniere,"%H:%M:%S")

             difference= derniere - premiere
             secondes=difference.total_seconds()
             gravite=calculer_gravite(secondes, tentatives)

             if secondes<=fenetre:

                suspects.append({
                   "ip": ip, 
                   "tentatives": tentatives,
                   "secondes":secondes,
                   "utilisateurs":list(set(users_ip[ip])),
                   "Debut":debut,
                   "Fin":fin,
                   "gravite":gravite,
                })
                break
  return suspects

def afficher_alertes(suspects):
   print()
   print(f"{JAUNE}IP suspectes détectées{RESET}: {len(suspects)}")
   print("\n" + "=" * 50)
   print(f"        {CYAN}RAPPORT DE DÉTECTION BRUTE FORCE{RESET}")
   print("=" * 50)

   if not suspects:
      print(f"{VERT}Aucune activité suspecte détectée{RESET}")
   else:
       for numero, suspect in enumerate(suspects, start=1): 
        print("-" * 50)
        print(f"{ROUGE}ALERTE #{numero}{RESET}")
        print("-" * 50)
        print()
        print(f"IP                    : {suspect['ip']}")
        print()
        print(f"Tentatives            : {suspect['tentatives']}")
        print()
        print(f"Gravité               : {suspect['gravite']}")
        print()
        utilisateurs_texte=", ".join(suspect['utilisateurs'])
        print(f"Comptes ciblés        : {utilisateurs_texte}")
        print()
        print(f"Heure de début        : {suspect['Debut']}")
        print()
        print(f"Heure de fin          : {suspect['Fin']}")
        print()
        print(f"Durée                 : {suspect['secondes']} secondes")
        print()

def verifier_ip(ip):
   parties=ip.split(".")
   if len(parties)!=4:
      return False
   ip_valide=True
   for partie in parties:
      try:
         nombre=int(partie)
      except ValueError:
         return False
      if nombre< 0 or nombre >255:
         ip_valide= False
         break
      return ip_valide 

def afficher_Lignes_ignorees(Lignes_ignorees):
   print()
   print("=" * 50)
   print(f"           {JAUNE}LIGNES IGNORÉES{RESET}")
   print("=" * 50)
   print(f"Nombre de lignes ignorées: {len(Lignes_ignorees)}")
   for element in Lignes_ignorees:
      print(f"- {element}")
   print()  

def afficher_resume(suspects,Lignes_ignorees):
   print("=" * 50)
   print("        RÉSUMÉ DE L'ANALYSE")
   print("=" * 50)
   print()
   print(f"IP suspectes détectées   : {len(suspects)}")
   print(f"Lignes ignorées          : {len(Lignes_ignorees)}") 
   print("Analyse terminée.")
   print()

def generer_rapport(suspects,Lignes_ignorees):
   maintenant=datetime.now()
   date_texte=maintenant.strftime("%d/%m/%Y à %H:%M:%S")
   with open("rapport_securite.txt", "w", encoding="utf-8") as fichier:
      fichier.write("RAPPORT DE DÉTECTION BRUTE FORCE\n")
      fichier.write(f"Rapport généré le : {date_texte}\n\n")
      fichier.write(f"IP suspectes détectées : {len(suspects)}\n")
      fichier.write(f"Lignes ignorées:{len(Lignes_ignorees)}\n")
      for numero, suspect in enumerate(suspects,start=1):
         fichier.write("=" * 50 + "\n")
         fichier.write(f"ALerte #{numero}\n")
         fichier.write("=" * 50 + "\n")
         utilisateurs_texte=", ".join(suspect["utilisateurs"])
         fichier.write(f"IP               : {suspect['ip']}\n")
         fichier.write(f"Tentatives       : {suspect['tentatives']}\n")
         fichier.write(f"Comptes ciblés   : {utilisateurs_texte}\n")
         fichier.write(f"Heure de début   : {suspect['Debut']}\n")
         fichier.write(f"Heure de fin     : {suspect['Fin']}\n")
         fichier.write(f"Durée            : {suspect['secondes']} secondes\n\n")
         fichier.write(f"Gravité          : {suspect['gravite']}\n")
      fichier.write("=" * 50 + "\n")
      fichier.write("LIGNES IGNORÉES\n")
      fichier.write("=" * 50 + "\n")
      fichier.write(f"Nombre de lignes ignorées : {len(Lignes_ignorees)}\n\n")
      for element in Lignes_ignorees:
          fichier.write(f"- {element}\n")

def calculer_gravite(secondes,tentatives):
   if tentatives>=10 and secondes<=5:
      return "critique"
   elif tentatives >=6 and secondes<=30:
      return "ÉLEVÉE"
   elif tentatives>=4 and secondes<=30:
      return "MOYENNE"
   elif tentatives>=4 and secondes<=60:
      return "FAIBLE"
   else:
      return "NON CLASSÉE"
      

compteur,heure_ip,users_ip,Lignes_ignorees=analyser_logs("auth_long.log")
ip_suspectes=detecter_bruteforce(compteur,heure_ip,users_ip,seuil,fenetre)
afficher_alertes(ip_suspectes)
afficher_Lignes_ignorees(Lignes_ignorees)  
afficher_resume(ip_suspectes,Lignes_ignorees) 
generer_rapport(ip_suspectes,Lignes_ignorees)


    