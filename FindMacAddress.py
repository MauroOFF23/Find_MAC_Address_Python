from netmiko import *
import re

switchip = input("Ingresa la IP origen: " )
username = input("¿Con qué usuario quieres ingresar?: ")
contraseña = input("¿Cuál es la contraseña?: ")
mac = input("¿Cuál mac quieres buscar?: ")
ip = switchip
 
while True:
  
    switch = {
        'device_type': "cisco_ios_ssh",
        'ip': ip,
        'username': username,
        'password': contraseña,}
    Conectar = ConnectHandler(**switch)
    


    macinclude = Conectar.send_command("show mac address-table | in " + mac)
    
 

 
    intport = re.compile(r'\w\w\w?\d\/\d/?\d?\d?')
    buscar_interfaz = intport.search(macinclude)
    interfaz = buscar_interfaz.group()
 
  
    buscar_MAC = re.search(mac, macinclude)
   
    
    if buscar_MAC is not None:
        cdpneighbor = Conectar.send_command("show cdp neighbors " + interfaz + " detail")
  
        IPcdp = re.compile(r'(\d\d\d[.]\d\d?\d?[.]\d\d?\d?[.]\d\d?\d?)')
        IP = IPcdp.search(cdpneighbor)
   

    
        try: 
            ip = IP.group()

        except:
            print("-------------------------------------------------------------------------------------------------------------------")
            print("En: ", interfaz)
            switch = (Conectar.send_command("sh running-config | include hostname"))
            print("En ", switch)
            break



    else:
        print("MAC no encontrada")
        break