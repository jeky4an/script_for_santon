import netbox
import ipaddress
from netmiko import ConnectHandler


def createConfig(nameOfMkt,whiteIP,defaultGateway,graySubnet,remoteIpGre="51.250.79.142",defaultGatewayCloud="ether8"):
    mikrotik_router_1 = {
        'device_type': 'mikrotik_routeros',
        'host': '',
        'port': '22',
        'username': 'admin',
        'password': ''
    }
    mikrotik_router_1["host"] = whiteIP
    grayP2P = str(netbox.returnP2Pprefix())
    ipv4 = ipaddress.ip_network(grayP2P)
    newList = list(ipv4.hosts())
    IdOfP2PInterface = netbox.returnIdOfinterfaceGRERes(nameOfMkt)
    IdOfDevice = netbox.returnIdOMikrot(nameOfMkt)
    netbox.setIpaddressGRE(IdOfDevice, IdOfP2PInterface, grayP2P, nameOfMkt)
    try:
        sshCli = ConnectHandler(**mikrotik_router_1)
        commandsIpRoute1 = f"/ip route add distance=1 dst-address={remoteIpGre} gateway={defaultGateway}"
        sshCli.send_command(commandsIpRoute1)
        commandsIpRoute2 = f"/interface gre add allow-fast-path=no local-address={whiteIP} name=mkt.cli.sto.cloud-res remote-address={remoteIpGre}"
        sshCli.send_command(commandsIpRoute2)
        commandsIpRouteipAdd = f"/ip address add address={newList[0]}/30 interface=mkt.cli.sto.cloud-res network={ipv4.network_address}"
        sshCli.send_command(commandsIpRouteipAdd)
        commandsIpRoute5 = f"/routing filter add action=accept chain=any-res prefix=0.0.0.0/0 prefix-length=0-32 set-in-nexthop={newList[1]} set-bgp-local-pref=90"
        sshCli.send_command(commandsIpRoute5)
        commandsIpRoute6 = f"/routing filter add action=accept chain=out-res prefix=0.0.0.0/0 prefix-length=0-32 set-bgp-med=500"
        sshCli.send_command(commandsIpRoute6)
        commandsIpRoute4 = f"/routing bgp peer add in-filter=any-res out-filter=out-res name=mkt.cli.sto.cloud-res nexthop-choice=force-self remote-address={newList[1]} remote-as=65002"
        sshCli.send_command(commandsIpRoute4)
        commandsIpRouteX = f"/ip route add distance=1 dst-address=0.0.0.0/0 gateway={defaultGateway}"
        sshCli.send_command(commandsIpRouteX)
        print("На "+ nameOfMkt +" созданы резервный gre туннель и bgp сессия!")
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

    try:
        mikrotik_router_1["host"] = remoteIpGre
        sshCli = ConnectHandler(**mikrotik_router_1)
        commandsIpRoute11 = f"/interface gre add allow-fast-path=no name={nameOfMkt}-res local-address=192.168.49.250 remote-address={whiteIP}"
        commandsIpRoute12 = f"/ip address add address={newList[1]}/30 interface={nameOfMkt}-res network={ipv4.network_address}"
        commandsIpRoute10 = f"/routing bgp peer add in-filter=NO-DEFAULT name={nameOfMkt}-res out-filter=NO-DEFAULT remote-address={newList[0]} remote-as=65002 route-reflect=yes"
        commandsIpRoute13 = f"/ip route add distance=1 dst-address={whiteIP} gateway={defaultGatewayCloud} routing-mark=res-tun"
        sshCli.send_command(commandsIpRoute11)
        sshCli.send_command(commandsIpRoute12)
        sshCli.send_command(commandsIpRoute10)
        sshCli.send_command(commandsIpRoute13)
        print("На snto.ya.cloud созданы резервный gre туннель и bgp сессия!")
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

nameOfMkt = input("Введите имя микротика в формате mkt.cli.sto.xxxx , где xxxx - город или улица")
whiteIP = input("Введите белый ip адрес филиала")
defaultGateway = input("Введите шлюз филиала")
graySubnet = input("Введите серую сеть филиала")
createConfig(nameOfMkt,whiteIP,defaultGateway,graySubnet)