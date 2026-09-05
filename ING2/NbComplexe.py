from math import sqrt,atan2,degrees

a=float(input("Entre la partie réelle:"))
b=float(input("Entre la partie imaginaire:"))
module=sqrt((a**2)+(b**2))
module=round(module,2)
argument=degrees(atan2(b,a))
argument=int(round(argument))
print(f"Le module est {module} et l'argument est {argument} degrés")
