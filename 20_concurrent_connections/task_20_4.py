# -*- coding: utf-8 -*-
'''
Задание 20.4

Создать функцию send_commands_to_devices, которая отправляет команду show или config на разные устройства
в параллельных потоках, а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* show - команда show, которую нужно отправить (по умолчанию, значение None)
* config - команды конфигурационного режима, которые нужно отправить (по умолчанию, значение None)
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Пример вызова функции:
In [5]: send_commands_to_devices(devices, show='sh clock', filename='result.txt')

In [6]: cat result.txt
R1#sh clock
*04:56:34.668 UTC Sat Mar 23 2019
R2#sh clock
*04:56:34.687 UTC Sat Mar 23 2019
R3#sh clock
*04:56:40.354 UTC Sat Mar 23 2019

In [11]: send_commands_to_devices(devices, config='logging 10.5.5.5', filename='result.txt')

In [12]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.5.5.5
R1(config)#end
R1#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#logging 10.5.5.5
R2(config)#end
R2#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#logging 10.5.5.5
R3(config)#end
R3#

In [13]: send_commands_to_devices(devices,
                                  config=['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0'],
                                  filename='result.txt')

In [14]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#router ospf 55
R1(config-router)#network 0.0.0.0 255.255.255.255 area 0
R1(config-router)#end
R1#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#router ospf 55
R2(config-router)#network 0.0.0.0 255.255.255.255 area 0
R2(config-router)#end
R2#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#router ospf 55
R3(config-router)#network 0.0.0.0 255.255.255.255 area 0
R3(config-router)#end
R3#


Для выполнения задания можно создавать любые дополнительные функции.
'''
import yaml, netmiko, logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException


logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.basicConfig(format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)

def send_commands_to_device(dev, command_list, conf):
    ip = dev['ip']
    logging.info(f'Connect to {ip}...')
    with netmiko.ConnectHandler(**dev) as ssh:
        ssh.enable()
        if conf:
            res = ssh.send_config_set(command_list, strip_prompt=False, strip_command=False).split('\n')
            host = res.pop()
            res[0] = host + res[0]
            result = '\n'.join(res) + '\n'
        else:
            result = ''
            for command in command_list:
                res = ssh.send_command(command, strip_prompt=False, strip_command=False).split('\n')
                host = res.pop()
                res[0] = host + res[0]
                result += '\n'.join(res) + '\n'
        logging.info(f'Receive from {ip}')
        return result

def send_commands_to_devices(devices, filename, show=None, config=None, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        if show:
            futures = [executor.submit(send_commands_to_device, device, show[device['ip']], 0) for device in devices]
        else:
            futures = [executor.submit(send_commands_to_device, device, config[device['ip']], 1) for device in devices]
        with open(filename, 'w') as dst:
            for future in futures:
                try:
                    dst.write(future.result())
                except (NetMikoAuthenticationException, NetMikoTimeoutException) as e:
                    print(e)



# don't run on import
if __name__ == "__main__":
    yaml_file = 'devicess.yaml'
    file_name_show = 'commands_show.txt'
    file_name_config = 'commands_config.txt'
    commands_show = {'10.111.111.11': ['sh ip int br', 'sh arp'],
                     '10.111.111.4':  ['sh arp'],
                     '10.111.111.3':  ['sh ip int br', 'sh ip route | ex -']}
    commands_config = {'10.111.111.11': ['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0'],
                       '10.111.111.4':  ['logging 10.5.5.5'],
                       '10.111.111.3':  ['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']}
    with open(yaml_file) as src:
        devicess = yaml.safe_load(src)
    send_commands_to_devices(devicess, show=commands_show, filename=file_name_show)
    send_commands_to_devices(devicess, config=commands_config, filename=file_name_config)