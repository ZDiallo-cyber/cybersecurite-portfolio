# with open("text.txt","w") as fichier:
#     fichier.write("Bonjour\n")
#     fichier.write("RAPPORT DE SECURITE\n")
#     fichier.write("IP suspecte : 45.33.12.99")
from datetime import datetime
maintenant=datetime.now()
date_texte=maintenant.strftime("%d/%m/%Y à %H:%M:%S")
print(date_texte)