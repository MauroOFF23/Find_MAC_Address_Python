import netmiko
import re

switchip = input("Ingresa la IP origen: " )
username = input("¿Con qué usuario quieres ingresar?: ")
contraseña = input("¿Cuál es la contraseña?: ")

INICIO = {
        "device_type":"cisco_ios",
        "host":switchip,
        "username":username,
        "password":contraseña,
        "port":"22",
        "secret":"cisco",
        }   


SESION = netmiko.ConnectHandler(**INICIO)
print("Connected succesfully")



def cdpdetail():
    detailneighbors = SESION.send_command("sh cdp neighbor "+DIRECTPORTINT+" detail")
    #print(detailneighbors)
    ipcdp = re.findall(r"\d\d\d[.]\d\d?\d?[.]\d\d?\d?[.]\d\d?\d?", detailneighbors)
    IP = (ipcdp[0])
    print(IP)
    

    NEXTSW= {
            "device_type":"cisco_ios",
            "host":IP,
            "username":"cisco",
            "password":'cisco',
            "port":"22",
            "secret":"cisco",
        }
    
    




mac = input("¿Cuál mac quieres buscar?: ")

while True:
    macinclude = SESION.send_command("sh mac address | include"+" "+ mac)
    #print(macinclude)
    DIRECTINT = re.findall(r"(Gi|Fa)", macinclude)
    DIRECTPORT = re.findall(r"(\d\/\d\/?\d?\d?)", macinclude)

    DIRECTINT1 = (DIRECTINT[0])
    DIRECTPORT1 = (DIRECTPORT[0])
    DIRECTPORTINT = (DIRECTINT1) + (DIRECTPORT1)
    #print(DIRECTPORT1)
    print(DIRECTPORTINT)

    shneighbor = SESION.send_command("show cdp neighbors")
    INTERF = re.findall(r"(Gi|Fa)", shneighbor)
    PORTNUM = re.search(DIRECTPORT1, shneighbor)
    if PORTNUM is None:
        print("nimodo")
        break
    #print(PORTNUM)
    else:
        INTERF1 = (INTERF[0])
        PORTNUM1 = (PORTNUM[0])
        TESTPORT = (INTERF1) + (PORTNUM1)
        print(TESTPORT)

    if DIRECTPORTINT == TESTPORT:
        cdpdetail()
    else:
        print("La mac address esta en el mismo dispositivo")


    
