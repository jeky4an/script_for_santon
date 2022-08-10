import ipaddress
import pynetbox
import pprint


nb = pynetbox.api(
    'http://10.21.13.2:8000',
    token='38bc1a28db41a7153d03bbb0d613e6a07c3b7f6e'
)
def returnP2Pprefix():  #выделяет свободный префикс /30 для p2p
    prefix = nb.ipam.prefixes.get(269)
    new_prefix = prefix.available_prefixes.create({"prefix_length": 30})
    new_prefix.update({"vrf": {"name": "Corp-Net"}, "tenant": {
        "id": 1,
        "name": "Santechnika Online",
        "slug": "santechnika-online"
    }, "role": {
        "id": 1,
        "name": "p2p",
        "slug": "p2p"
    }})
    print("Был создан и добавлен p2p " + new_prefix["prefix"])
    return new_prefix
def returnLo0(): #выделяет свободный префикс /32 для лупбека
    prefix1 = nb.ipam.prefixes.get(1)
    lo0 = prefix1.available_prefixes.create({"prefix_length": 32})
    lo0.update({"vrf": {"name": "Corp-Net"}, "tenant": {
        "id": 1,
        "name": "Santechnika Online",
        "slug": "santechnika-online"
    },"role": {
        "id": 3,
        "name": "loopback",
        "slug": "loopback"

    }})
    print("Был создан и добавлен lo0 " + lo0["prefix"])
    return lo0
def createDevice(nameOfMikrot): #создаёт девайс если он не создан
    devices = nb.dcim.devices.count(name=nameOfMikrot)
    if devices >= 1:
        print(nameOfMikrot + " уже создан! ")
        return devices
    else:
        device = nb.dcim.devices.create(name=nameOfMikrot,device_type= {
        "id": 2,
        "manufacturer": {
            "id": 2,
            "name": "Mikrotik",
            "slug": "mikrotik"
        },
        "model": "mipsbe hEX PoE",
        "slug": "mipsbe-hex-poe"
        },device_role= {
        "id": 1,
        "name": "Router",
        "slug": "router"
        },tenant = {
        "id": 1,
        "name": "Santechnika Online",
        "slug": "santechnika-online"
        },site = {
            "id": 3,
            "name": "Moscow",
            "slug": "moscow"})
        return 0
def returnIdOfinterface(nameOfMikroot): # возвращает id interface lo0
    device = nb.dcim.devices.get(name=nameOfMikroot)
    idOfDevice = device["id"]
    interfaces = nb.dcim.interfaces.all()
    newListInterface = list(interfaces)
    for dictWithInterface in newListInterface:
        if dictWithInterface.device.id == idOfDevice and dictWithInterface.name == "lo0":
            updateToIpAddress = nb.dcim.interfaces.get(id=dictWithInterface.id)
            print("id lo0 - " + str(updateToIpAddress["id"]))
            return updateToIpAddress["id"]

def returnIdOMikrot(nameOfMikroot): # возвращает id device
    device = nb.dcim.devices.get(name=nameOfMikroot)
    idOfDevice = device["id"]
    print("id нового микротика " + str(idOfDevice))
    return idOfDevice

def setIpaddress(idOfMikrotik,idOfinterface,ipaddress,nameofMikrotik): #Привязывает ip к lo0
    prefix = nb.ipam.prefixes.all()
    prefix = list(prefix)
    ipaddress += "/32"
    for p in prefix:
        if str(p.prefix) == ipaddress:
            ipaddresCreate = p.available_ips.create({"address": str(ipaddress), "vrf": {"name": "Corp-Net"}, "assigned_object_type": "dcim.interface","assigned_object_id": int(idOfinterface), "assigned_object": {
                "id": int(idOfinterface),
                "device": {
                    "id": int(idOfMikrotik),
                    "name": str(nameofMikrotik)
            }}})
            print("Привязка ip к lo0 прошла успешно")

def returnIdOfinterfaceGRE(nameOfMikroot):  # возвращает id interface GRE
    device = nb.dcim.devices.get(name=nameOfMikroot)
    idOfDevice = device["id"]
    interfaces = nb.dcim.interfaces.all()
    newListInterface = list(interfaces)
    for dictWithInterface in newListInterface:
        if dictWithInterface.device.id == idOfDevice and dictWithInterface.name == "snto.ya.cloud":
            updateToIpAddress = nb.dcim.interfaces.get(id=dictWithInterface.id)
            print("id p2p prefix'a - " + str(updateToIpAddress["id"]))
            return updateToIpAddress["id"]

def returnIdOfinterfaceGRERes(nameOfMikroot):  # возвращает id interface GRE-резерв
    device = nb.dcim.devices.get(name=nameOfMikroot)
    idOfDevice = device["id"]
    interfaces = nb.dcim.interfaces.all()
    newListInterface = list(interfaces)
    for dictWithInterface in newListInterface:
        if dictWithInterface.device.id == idOfDevice and dictWithInterface.name == "snto.ya.cloud-res":
            updateToIpAddress = nb.dcim.interfaces.get(id=dictWithInterface.id)
            print("id p2p prefix'a - " + str(updateToIpAddress["id"]))
            return updateToIpAddress["id"]

def setIpaddressGRE(idOfMikrotik,idOfinterface,ipaddressGRE,nameofMikrotik): #Привязывает ip к GRE
    prefix = nb.ipam.prefixes.all()
    prefix = list(prefix)
    for p in prefix:
        if str(p.prefix) == ipaddressGRE:
            ipv4 = ipaddress.ip_network(ipaddressGRE)
            newList = list(ipv4.hosts())
            ipaddresCreate = p.available_ips.create({"address": str(newList[0]), "vrf": {"name": "Corp-Net"}, "assigned_object_type": "dcim.interface","assigned_object_id": int(idOfinterface), "assigned_object": {
                "id": int(idOfinterface),
                "device": {
                    "id": int(idOfMikrotik),
                    "name": str(nameofMikrotik)
            }}})
            print("Привязка ip к P2P интерфейсу прошла успешно")

def returnIdOfinterfaceLOCAL(nameOfMikroot):  # возвращает id interface GRE
    device = nb.dcim.devices.get(name=nameOfMikroot)
    idOfDevice = device["id"]
    interfaces = nb.dcim.interfaces.all()
    newListInterface = list(interfaces)
    for dictWithInterface in newListInterface:
        if dictWithInterface.device.id == idOfDevice and dictWithInterface.name == "ether3":
            updateToIpAddress = nb.dcim.interfaces.get(id=dictWithInterface.id)
            print("id ether3 - " + str(updateToIpAddress["id"]))
            return updateToIpAddress["id"]

def checkAndCreatePrefix(grayPrefix,idOfMikrotik=0,idOfinterface=0,nameOfMikrotik="test"): #Проверяет существует ли префикс, создаёт и возвращает id
    prefix = nb.ipam.prefixes.all()
    prefix = list(prefix)
    for p in prefix:
          if str(p.prefix) == grayPrefix:
              raise Exception("Префикс существует")

    prefixValue = nb.ipam.prefixes.create({"family": {
                "value": 4,
                "label": "IPv4"
            }, "vrf": {"name": "Corp-Net"},
                  "prefix": str(grayPrefix),
                  "tenant": {
                      "id": 1,
                      "name": "Santechnika Online",
                      "slug": "santechnika-online"
                  },
                  "role": {
                "id": 2,
                "name": "local",
                "slug": "local"
            }

              })
    print(f"Префикс {grayPrefix} добавлен в нетбокс!")
    return str(prefixValue.id)


def setLocalIpAdress(idPrefix,idOfinterface,idOfMikrotik,nameofMikrotik):#
    prefix = nb.ipam.prefixes.get(idPrefix)
    ipv4 = ipaddress.ip_network(prefix.prefix)
    newList = list(ipv4.hosts())
    ipaddresCreate = prefix.available_ips.create(
        {"address": str(newList[0]), "vrf": {"name": "Corp-Net"}, "assigned_object_type": "dcim.interface", "assigned_object_id": int(idOfinterface),
         "assigned_object": {
             "id": int(idOfinterface),
             "device": {
                 "id": int(idOfMikrotik),
                 "name": str(nameofMikrotik)
             }}})
    print(f"Привязка ip адреса {str(newList[0])} к ether3 прошла успешно! ")