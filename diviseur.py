Liste_ports=[21,22,23,80,443,8080]
def port_a_position(Liste_ports,position):
    try:
        return Liste_ports[position]
    except IndexError:
        return "Position invalide"
    
print(port_a_position(Liste_ports,0))
print(port_a_position(Liste_ports,2))
print(port_a_position(Liste_ports,10))

