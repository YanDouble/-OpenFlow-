from mininet.net import Mininet
from mininet.node import Host, OVSSwitch, RemoteController
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import requests
import json

# 示例身份验证函数
def authenticate(username, password):
    valid_credentials = {
        'user1': '123456',
        'user2': '123456',
        'user3': '123456',
        'user4': '123456'
    }
    return valid_credentials.get(username) == password

def addHost(net, switch_name, host_name, host_cls):
    """
    动态添加一个主机并连接到指定的交换机
    """
    switch = net.get(switch_name)
    new_host = net.addHost(host_name, cls=host_cls)
    net.addLink(new_host, switch)
    new_host.start()
    return new_host


#控制器URL和认证: 请确保将controller_url替换为OpenDaylight控制器的实际URL。此外，如果控制器需要认证，可能需要在请求中添加适当的认证头或参数。
#设备ID和流表ID: 这里的switch_name和流表ID (flow/1和flow/2) 需要根据实际网络配置来调整。
#主机IP: 在调用这些函数时，需要提供正确的主机IP地址。
# 示例函数来允许或阻止流量（需要根据OpenDaylight API进行实现）
def allow_traffic(controller_url, host_ip, switch_name):
    # 构建允许特定主机流量的OpenFlow流表规则
    flow_rule = {
        "flow": {
            "id": "1",
            "priority": "32768",
            "timeout": "0",
            "isPermanent": "true",
            "deviceId": switch_name,
            "treatment": {
                "instructions": [
                    {"type": "OUTPUT", "port": "NORMAL"}
                ]
            },
            "selector": {
                "criteria": [
                    {"type": "ETH_TYPE", "ethType": "0x800"},
                    {"type": "IPV4_DST", "ip": host_ip}
                ]
            }
        }
    }

    # 发送请求到OpenDaylight控制器
    url = f"{controller_url}/restconf/config/opendaylight-inventory:nodes/node/{switch_name}/table/0/flow/1"
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, data=json.dumps(flow_rule), headers=headers)

    if response.status_code == 200:
        print("流量允许规则已成功添加")
    else:
        print("添加流量允许规则失败:", response.text)

def block_traffic(controller_url, host_ip, switch_name):
    # 构建阻止特定主机流量的OpenFlow流表规则
    flow_rule = {
        "flow": {
            "id": "2",
            "priority": "32768",
            "timeout": "0",
            "isPermanent": "true",
            "deviceId": switch_name,
            "treatment": {},  # 没有处理指令意味着丢弃包
            "selector": {
                "criteria": [
                    {"type": "ETH_TYPE", "ethType": "0x800"},
                    {"type": "IPV4_SRC", "ip": host_ip}
                ]
            }
        }
    }

    # 发送请求到OpenDaylight控制器
    url = f"{controller_url}/restconf/config/opendaylight-inventory:nodes/node/{switch_name}/table/0/flow/2"
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, data=json.dumps(flow_rule), headers=headers)

    if response.status_code == 200:
        print("流量阻止规则已成功添加")
    else:
        print("添加流量阻止规则失败:", response.text)


# 自定义主机类
class AuthHost(Host):
    def __init__(self, name, controller_url, switch_name, **kwargs):
        Host.__init__(self, name, **kwargs)
        self.controller_url = controller_url
        self.switch_name = switch_name

    def startShell(self, *args, **kwargs):
        Host.startShell(self, *args, **kwargs)
        authenticated = authenticate(self.name, '123456')  # 假设的密码
        print(self.controller_url)
        if authenticated:
            print(f"{self.name} 认证成功")
            allow_traffic(self.controller_url, self.name, self.switch_name)
        else:
            print(f"{self.name} 认证失败")
            block_traffic(self.controller_url, self.name, self.switch_name)

# 网络拓扑
class GRETopo(Topo):
    def build(self):
        controller_url = 'http://localhost:8181'
        # 创建三台交换机
        s1 = self.addSwitch('s1', cls=OVSSwitch)
        s2 = self.addSwitch('s2', cls=OVSSwitch)
        s3 = self.addSwitch('s3', cls=OVSSwitch)

        # 分配IP和MAC地址，并连接用户主机到交换机s2和s3
        user1 = self.addHost('user1', cls=AuthHost, controller_url=controller_url, switch_name='s2', ip='10.0.0.1', mac='00:00:00:00:00:01')
        user2 = self.addHost('user2', cls=AuthHost, controller_url=controller_url, switch_name='s2', ip='10.0.0.2', mac='00:00:00:00:00:02')
        user3 = self.addHost('user3', cls=AuthHost, controller_url=controller_url, switch_name='s3', ip='10.0.0.3', mac='00:00:00:00:00:03')
        user4 = self.addHost('user4', cls=AuthHost, controller_url=controller_url, switch_name='s3', ip='10.0.0.4', mac='00:00:00:00:00:04')

        # 添加网络服务主机并连接到交换机s1
        hardDisk = self.addHost('hardDisk')
        printer = self.addHost('printer')
        secret = self.addHost('secret')

        # 连接用户主机和交换机
        self.addLink(user1, s2)
        self.addLink(user2, s2)
        self.addLink(user3, s3)
        self.addLink(user4, s3)

        # 连接网络服务主机和交换机s1
        self.addLink(hardDisk, s1)
        self.addLink(printer, s1)
        self.addLink(secret, s1)

        # 交换机之间相互连接
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s1)

# topos = {'simple': (lambda: GRETopo() )}
if __name__ == '__main__':
    setLogLevel('info')
    topo = GRETopo()
    net = Mininet(topo=topo, link=TCLink, controller=RemoteController)

    # 使动态添加主机的函数在CLI环境中可用
    net.start()
    CLI(net)
    # globals()['addHost'] = lambda x, y, z: addHost(net, x, y, AuthHost)

    net.stop()

