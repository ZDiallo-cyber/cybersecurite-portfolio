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

print(verifier_ip("192.168.1.50"))
print(verifier_ip("10.0.0.1"))
print(verifier_ip("192.168.999.50"))
print(verifier_ip("192.abc.1.50"))
print(verifier_ip("192.168.1"))