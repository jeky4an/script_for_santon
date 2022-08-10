import netbox
import ipaddress
from netmiko import ConnectHandler
def createConfig (nameOfMkt,whiteIP,defaultGateway,graySubnet,remoteIpGre="178.154.200.189",defaultGatewayCloud="ether1"):
        mikrotik_router_1 = {
        'device_type': 'mikrotik_routeros',
        'host': '',
        'port': '22',
        'username': 'admin',
        'password': ''
        }
        mikrotik_router_1 ["host"] = whiteIP
        check = netbox.createDevice(nameOfMkt)
        if check >= 1:
            raise Exception("Микротик существует")
        else:
            print("В netbox был создан " + nameOfMkt)
        IdOfInterface = netbox.returnIdOfinterface(nameOfMkt)
        IdOfDevice = netbox.returnIdOMikrot(nameOfMkt)
        IdOfP2PInterface = netbox.returnIdOfinterfaceGRE(nameOfMkt)
        idInterfaceLocal = netbox.returnIdOfinterfaceLOCAL(nameOfMkt)
        idPrefixLocal = netbox.checkAndCreatePrefix(graySubnet)
        try:
            sshCli = ConnectHandler(**mikrotik_router_1)
            commands = [ "/ip service",
            "set telnet disabled=yes",
            "set ftp address=85.114.0.0/22,172.19.0.0/16,172.16.0.0/16,192.168.0.0/16",
            "set www address=85.114.0.0/22,172.19.0.0/16,172.16.0.0/16,192.168.0.0/16",
            "set ssh address=85.114.0.0/22,172.19.0.0/16,172.16.0.0/16,192.168.0.0/16",
            "set api disabled=yes",
            "set winbox address=85.114.0.0/22,172.19.0.0/16,172.16.0.0/16,192.168.0.0/16,10.14.0.0/23,10.12.0.0/23"
            "set api-ssl disabled=yes" ]
            sshCli.send_config_set(commands)

            grayP2P = str(netbox.returnP2Pprefix())
            lo0 = str(netbox.returnLo0())
            lo0 = lo0.split("/")
            lo0 = lo0[0]
            ipv4 = ipaddress.ip_network(grayP2P)
            newList = list(ipv4.hosts())
            netbox.setLocalIpAdress(idPrefixLocal, idInterfaceLocal, IdOfDevice, nameOfMkt)
            netbox.setIpaddress(IdOfDevice, IdOfInterface, lo0, nameOfMkt)
            netbox.setIpaddressGRE(IdOfDevice, IdOfP2PInterface, grayP2P, nameOfMkt)
            commandsIpRouteX = f"/ip route add distance=2 gateway={defaultGateway}"
            sshCli.send_command(commandsIpRouteX)
            commandsIpRoute0 = f"/ip firewall nat add action=masquerade chain=srcnat out-interface-list=WAN"
            sshCli.send_command(commandsIpRoute0)
            commandsIpRoute1 = f"/ip route add distance=1 dst-address={remoteIpGre} gateway={defaultGateway}"
            sshCli.send_command(commandsIpRoute1)
            commandsIpRoute2 = f"/interface gre add allow-fast-path=no local-address={whiteIP} name=mkt.cli.sto.cloud remote-address={remoteIpGre}"
            sshCli.send_command(commandsIpRoute2)
            commandsIpRouteipAdd = f"/ip address add address={newList[0]}/30 interface=mkt.cli.sto.cloud network={ipv4.network_address}"
            sshCli.send_command(commandsIpRouteipAdd)
            commandsIpRoute3 = f"/routing filter add action=accept chain=any prefix=0.0.0.0/0 prefix-length=0-32 set-in-nexthop={newList[1]}"
            sshCli.send_command(commandsIpRoute3)
            commandsIpRoute4 = f"/routing bgp peer add in-filter=any name=mkt.cli.sto.cloud nexthop-choice=force-self remote-address={newList[1]} remote-as=65002"
            sshCli.send_command(commandsIpRoute4)
            commandsIpRoute5 = "/routing bgp instance set default as=65002 client-to-client-reflection=no ignore-as-path-len=yes"
            sshCli.send_command(commandsIpRoute5)
            commandsIpRoute6 = f"/routing bgp network add network={lo0}"
            sshCli.send_command(commandsIpRoute6)
            commandsIpRoute7 = f"/routing bgp network add network={graySubnet}"
            sshCli.send_command(commandsIpRoute7)
            commandsIpRoute8 = "/interface bridge add name=lo0 protocol-mode=none"
            sshCli.send_command(commandsIpRoute8)
            commandsIpRoute9 = f"/ip address add address={lo0} interface=lo0 network={lo0}"
            sshCli.send_command(commandsIpRoute9)
            commandsIpRoute14 = f"/system identity set name={nameOfMkt}"
            sshCli.send_command(commandsIpRoute14)
            print("Конфиг загружен на "+ lo0 + ":" + nameOfMkt)
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
            print(error)
        try:
            mikrotik_router_1["host"] = remoteIpGre
            sshCli = ConnectHandler(**mikrotik_router_1)
            commandsIpRoute11 = f"/interface gre add allow-fast-path=no name={nameOfMkt} remote-address={whiteIP}"
            commandsIpRoute12 = f"/ip address add address={newList[1]}/30 interface={nameOfMkt} network={ipv4.network_address}"
            commandsIpRoute10 = f"/routing bgp peer add in-filter=NO-DEFAULT name={nameOfMkt} out-filter=NO-DEFAULT remote-address={newList[0]} remote-as=65002 route-reflect=yes"
            commandsIpRoute13 = f"/ip route add distance=1 dst-address={whiteIP} gateway={defaultGatewayCloud}"

            sshCli.send_command(commandsIpRoute11)
            sshCli.send_command(commandsIpRoute12)
            sshCli.send_command(commandsIpRoute10)
            sshCli.send_command(commandsIpRoute13)
            print("Конфиг загружен на mkt.cli.sto.cloud!")
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
            print(error)

#createConfig (whiteIP,grayP2P,defaultGateway,graySubnet,lo0,remoteIpGre="178.154.200.189"):
nameOfMkt = input("Введите имя микротика в формате mkt.cli.sto.xxxx , где xxxx - город или улица")
whiteIP = input("Введите белый ip адрес филиала")
defaultGateway = input("Введите шлюз филиала")
graySubnet = input("Введите серую сеть филиала")
createConfig(nameOfMkt,whiteIP,defaultGateway,graySubnet,remoteIpGre="178.154.200.189")
# "test"