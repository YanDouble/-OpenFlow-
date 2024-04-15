import requests
import json
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController, Host
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI

def authenticateUI(username, password):
    valid_credentials = {
        'user1': '123456',
        'user2': '123456',
        'user3': '123456',
        'user4': '123456'
    }
    return valid_credentials.get(username) == password

class AuthHost(Host):
    def __init__(self, name, **kwargs):
        super(AuthHost, self).__init__(name, **kwargs)
        
    def pop_terminal(self):
        # Add your logic to pop up a terminal and get user input
        print(f"Opening terminal for {self.name}...")

        # Use read command to get user input
        self.cmd('xterm -e "read -p \'Enter username: \' username && read -s -p \'Enter password: \' password && echo $username $password" > temp.txt &')

        # Read the temporary file to get username and password
        with open('temp.txt', 'r') as file:
            user_input = file.read().split()
            self.username = user_input[0]
            self.password = user_input[1] 

    def authenticate(self):
        if authenticateUI(self.username, self.password):
            return True
        else:
            return False

    def send_flow_table(self):
        if self.authenticate():
            flow_rule = {
            "flow": {
                "id": f"stp-{self.name}",
                "priority": 200,
                "table_id": 0,
                "match": {
                    "dl_src": f"{self.mac}",
                    "nw_src": f"{self.ip}"
                },
                "instructions": {
                    "instruction": [{
                        "order": 0,
                        "apply-actions": {
                        "action": [{
                            "order": 0,
                            "output-action": { "output-node-connector": "openflow:2:1" }
                        }]
                        }
                    }]
                }
            }
            }
            
            json_data = json.dumps(flow_rule)
            url = "http://localhost:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:2/table/0/"
            headers = {"Content-Type": "application/json"}
            auth = ("admin", "admin") 
            
            response = requests.put(url, headers=headers, auth=auth, data=json_data)
            print(f"Flow table sent for {self.name}")
        else:
            print(f"Your validation did not pass for {self.name}.")


if __name__ == '__main__':
    class CustomTopology(Topo):
        def build(self):
            # Create Switch
            s1 = self.addSwitch('s1')
            s2 = self.addSwitch('s2')
            s3 = self.addSwitch('s3')
            
            # Create Host Instruction
            hardDisk = self.addHost('hardDisk', ip='10.3.0.1', mac='00:10:00:00:00:01')
            printer = self.addHost('printer', ip='10.3.0.2', mac='00:10:00:00:00:02')
            secret = self.addHost('secret', ip='10.3.0.3', mac='00:10:00:00:00:03')
            
            # Create User Host
            user1 = self.addHost('user1', cls=AuthHost, ip='10.3.0.4', mac='00:10:00:00:00:04')
            user2 = self.addHost('user2', cls=AuthHost, ip='10.3.0.5', mac='00:10:00:00:00:05')
            user3 = self.addHost('user3', cls=AuthHost, ip='10.3.0.6', mac='00:10:00:00:00:06')
            user4 = self.addHost('user4', cls=AuthHost, ip='10.3.0.7', mac='00:10:00:00:00:07')
            
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
            
    net = Mininet(topo=CustomTopology(), link=TCLink, controller=RemoteController)

    net.start()
    
    # Pop up terminals and simulate user input for each host
    for host_name in ['user1', 'user2']:
        host = net.get(host_name)
        host.pop_terminal()

    # Enter Mininet CLI
    CLI(net)
    
    # Stop Mininet
    net.stop()
