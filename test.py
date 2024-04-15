from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI

class CustomTopology(Topo):
    def build(self):
        # Create Switch
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        
        # Create Host Instruction
        hardDisk = self.addHost('hardDisk')
        printer = self.addHost('printer')
        secret = self.addHost('secret')
        
        # Create User Host
        user1 = self.addHost('user1')
        user2 = self.addHost('user2')
        user3 = self.addHost('user3')
        user4 = self.addHost('user4')
        
        # Create Links
        self.addLink(hardDisk, s1)
        self.addLink(printer, s1)
        self.addLink(secret, s1)
        
        self.addLink(s2, s1)
        self.addLink(s3, s1)
        self.addLink(s2, s3)
        
        self.addLink(user1, s2)
        self.addLink(user2, s2)
        self.addLink(user3, s3)
        self.addLink(user4, s3)
        
topos = {'simple': (lambda: CustomTopology() )}
net = Mininet(topo=CustomTopology(), controller=RemoteController, autoSetMacs=True, autoStaticArp=True)

# 启动Mininet拓扑
net.start()
CLI(net)
net.stop()