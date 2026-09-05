resultats={
    21:"ouvert",
    22:"ouvert",
    23:"ouvert",
    80:"ouvert",
    443:"fermé",
    8080:"fermé"
}
compteur1=0
compteur2=0
for port, etat in resultats.items():
    if etat=="ouvert":
        compteur1+=1
    else:
        compteur2+=1

print(f"les ports ouverts sont :{compteur1}")
print(f"Les porst fermés sont:{compteur2}")