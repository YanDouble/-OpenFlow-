import requests
import json
import getpass
import sqlite3
import netifaces as ni

def getMAC(username):
    mac = ni.ifaddresses(f'{username}-eth0')[ni.AF_LINK][0]['addr']
    return mac

def getInformation():
    username = input('Please input your username:\n')
    service = input('Please input your want to use service:\n')
    password = getpass.getpass("Enter your password:\n")
    
    return username, password, service
    
def authenticate(username, password,service):
    #连接数据库并创建游标
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? and password = ?",(username, password))
    if not cursor.fetchall():
        print("Username Or Password Error.")
        return False
    else :
        print("Log In Successfully!")
    cursor.execute("SELECT * FROM rules WHERE user = ? and service = ?",(username,service))
    if not cursor.fetchall():
        print(f"You don't have the {service}")
        return False
    else :
        print("Successfully! You can use the service.")
    # 关闭数据库连接
    conn.close()
    return True

def send_flow_table(username, password, service, mac, ip, switch, infer):
    switch_infer = {'2': '4', '3': '5'}
    service_infer = {'hardDisk': '1', 'printer': '2', 'secret': '3'}
    service_mac = {'hardDisk': '2a:b3:a3:0b:e1:46', 'printer': '12:82:cc:55:c7:f0', 'secret': '16:8b:5b:04:f4:39'}
    if authenticate(username, password, service):
        # request information
        headers = {"Content-Type": "application/json"}
        auth = ("admin", "admin") 
        
        # flow rule
        stp_user_To_ip = {
            "flow": {
            "id": f"stp-s{switch}-{infer}-1-{service}-ip-{username}",
            "priority": 200,
            "table_id": 0,
            "match": {
                "ethernet-match": {"ethernet-type": {"type": 2048}, "ethernet-source": {"address": f"{mac}"}}
            },
            "instructions": {
                "instruction": [{
                "order": 0,
                "apply-actions": {
                    "action": [{
                    "order": 0,
                    "output-action": { "output-node-connector": f"openflow:{switch}:1" }
                    }]
                }
                }]
            }
            }
        }
        
        json_stp_user_To_ip = json.dumps(stp_user_To_ip)
        url_stp_user_To_ip = f"http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:{switch}/table/0/flow/stp-s{switch}-{infer}-1-{service}-ip-{username}"
        response_stp_user_To_ip = requests.put(url_stp_user_To_ip, headers=headers, auth=auth, data=json_stp_user_To_ip)
        print(response_stp_user_To_ip)
        
        stp_service_To_ip = {
            "flow": {
            "id": f"stp-s1-{switch_infer[switch]}-{service_infer[service]}-{service}-ip-{username}",
            "priority": 200,
            "table_id": 0,
            "match": {
                "in-port": f"openflow:1:{switch_infer[switch]}",
                "ethernet-match": {"ethernet-type": {"type": 2048}}
            },
            "instructions": {
                "instruction": [{
                "order": 0,
                "apply-actions": {
                    "action": [{
                    "order": 0,
                    "output-action": { "output-node-connector": f"openflow:1:{service_infer[service]}" }
                    }]
                }
                }]
            }
            }
        }
        
        json_stp_service_To_ip = json.dumps(stp_service_To_ip)
        url_stp_service_To_ip = f"http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/stp-s1-{switch_infer[switch]}-{service_infer[service]}-{service}-ip-{username}"
        response_stp_service_To_ip = requests.put(url_stp_service_To_ip, headers=headers, auth=auth, data=json_stp_service_To_ip)
        print(response_stp_service_To_ip)
        
        stp_user_To_mac = {
            "flow": {
            "id": f"stp-s{switch}-{infer}-1-{service}-mac-{username}",
            "priority": 200,
            "table_id": 0,
            "match": {
                "ethernet-match": {"ethernet-type": {"type": 2054}, "ethernet-source": {"address": f"{mac}"}}
            },
            "instructions": {
                "instruction": [{
                "order": 0,
                "apply-actions": {
                    "action": [{
                    "order": 0,
                    "output-action": { "output-node-connector": f"openflow:{switch}:1" }
                    }]
                }
                }]
            }
            }
        }
        
        json_stp_user_To_mac = json.dumps(stp_user_To_mac)
        url_stp_user_To_mac = f"http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:{switch}/table/0/flow/stp-s{switch}-{infer}-1-{service}-mac-{username}"
        response_stp_user_To_mac = requests.put(url_stp_user_To_mac, headers=headers, auth=auth, data=json_stp_user_To_mac)
        print(response_stp_user_To_mac)
        
        stp_service_To_mac = {
            "flow": {
            "id": f"stp-s1-{switch_infer[switch]}-{service_infer[service]}-{service}-mac-{username}",
            "priority": 200,
            "table_id": 0,
            "match": {
                "in-port": f"openflow:1:{switch_infer[switch]}",
                "ethernet-match": {"ethernet-type": {"type": 2054}}
            },
            "instructions": {
                "instruction": [{
                "order": 0,
                "apply-actions": {
                    "action": [{
                    "order": 0,
                    "output-action": { "output-node-connector": f"openflow:1:{service_infer[service]}" }
                    }]
                }
                }]
            }
            }    
        }
        
        json_stp_service_To_mac = json.dumps(stp_service_To_mac)
        url_stp_service_To_mac = f"http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/stp-s1-{switch_infer[switch]}-{service_infer[service]}-{service}-mac-{username}"
        response_stp_service_To_mac = requests.put(url_stp_service_To_mac, headers=headers, auth=auth, data=json_stp_service_To_mac)
        print(response_stp_service_To_mac)
        
        stp_user_From_ip = {
            "flow": {
            "id": f"stp-s{switch}-1-{infer}-{service}-ip-{username}",
            "priority": 200,
            "table_id": 0,
            "match": {
                "in-port": f"openflow:{switch}:1",
                "ethernet-match": {"ethernet-type": {"type": 2048}, "ethernet-destination": {"address": f"{mac}"}}
            },
            "instructions": {
                "instruction": [{
                "order": 0,
                "apply-actions": {
                    "action": [{
                    "order": 0,
                    "output-action": { "output-node-connector": f"openflow:{switch}:{infer}" }
                    }]
                }
                }]
            }
            }
        }
        
        json_stp_user_From_ip = json.dumps(stp_user_From_ip)
        url_stp_user_From_ip = f"http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:{switch}/table/0/flow/stp-s{switch}-1-{infer}-{service}-ip-{username}"
        response_stp_user_From_ip = requests.put(url_stp_user_From_ip, headers=headers, auth=auth, data=json_stp_user_From_ip)
        print(response_stp_user_From_ip)
        
        stp_service_From_ip = {
            "flow": {
            "id": f"stp-s1-{service_infer[service]}-{switch_infer[switch]}-{service}-ip-{username}",
            "priority": 200,
            "table_id": 0,
            "match": {
                "in-port": f"openflow:1:{service_infer[service]}",
                "ethernet-match": {"ethernet-type": {"type": 2048}}
            },
            "instructions": {
                "instruction": [{
                "order": 0,
                "apply-actions": {
                    "action": [{
                    "order": 0,
                    "output-action": { "output-node-connector": f"openflow:1:{switch_infer[switch]}" }
                    }]
                }
                }]
            }
            }
        }
        
        json_stp_service_From_ip = json.dumps(stp_service_From_ip)
        url_stp_service_From_ip = f"http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/stp-s1-{service_infer[service]}-{switch_infer[switch]}-{service}-ip-{username}"
        response_stp_service_From_ip = requests.put(url_stp_service_From_ip, headers=headers, auth=auth, data=json_stp_service_From_ip)
        print(response_stp_service_From_ip)
        
        stp_user_From_mac = {
            "flow": {
            "id": f"stp-s{switch}-1-{infer}-{service}-mac-{username}",
            "priority": 200,
            "table_id": 0,
            "match": {
                "in-port": f"openflow:{switch}:1",
                "ethernet-match": {"ethernet-type": {"type": 2054}, "ethernet-destination": {"address": f"{mac}"}}
            },
            "instructions": {
                "instruction": [{
                "order": 0,
                "apply-actions": {
                    "action": [{
                    "order": 0,
                    "output-action": { "output-node-connector": f"openflow:{switch}:{infer}" }
                    }]
                }
                }]
            }
            }
        }
        
        json_stp_user_From_mac = json.dumps(stp_user_From_mac)
        url_stp_user_From_mac = f"http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:{switch}/table/0/flow/stp-s{switch}-1-{infer}-{service}-mac-{username}"
        response_stp_user_From_mac = requests.put(url_stp_user_From_mac, headers=headers, auth=auth, data=json_stp_user_From_mac)
        print(response_stp_user_From_mac)
        
        stp_service_From_mac = {
            "flow": {
            "id": f"stp-s1-{service_infer[service]}-{switch_infer[switch]}-{service}-mac-{username}",
            "priority": 200,
            "table_id": 0,
            "match": {
                "in-port": f"openflow:1:{service_infer[service]}",
                "ethernet-match": {"ethernet-type": {"type": 2054}}
            },
            "instructions": {
                "instruction": [{
                "order": 0,
                "apply-actions": {
                    "action": [{
                    "order": 0,
                    "output-action": { "output-node-connector": f"openflow:1:{switch_infer[switch]}" }
                    }]
                }
                }]
            }
            }  
        }

        json_stp_service_From_mac = json.dumps(stp_service_From_mac)
        url_stp_service_From_mac = f"http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/stp-s1-{service_infer[service]}-{switch_infer[switch]}-{service}-mac-{username}"
        response_stp_service_From_mac = requests.put(url_stp_service_From_mac, headers=headers, auth=auth, data=json_stp_service_From_mac)
        print(response_stp_service_From_mac)
        
        print(f"All flow rule were sent for {username}")
    else:
        print(f"Your validation did not pass for {username}.")
        

             
if __name__ == '__main__':
    username, password, service = getInformation()
    user_mac = {'user1': '00:00:00:00:00:04', 'user2': '00:00:00:00:00:05','user3': '00:00:00:00:00:06', 'user4': '00:00:00:00:00:07'}
    user_ip = {'user1': '10.0.0.4/8', 'user2': '10.0.0.5/8','user3': '10.0.0.6/8', 'user4': '10.0.0.7/8'}
    userMac = getMAC(username)
    user_switch = {'user1': '2', 'user2': '2', 'user3': '3', 'user4': '3'}
    user_infer = {'user1': '3', 'user2': '4', 'user3': '3', 'user4': '4'}
    send_flow_table(username, password, service, user_mac[username], user_ip[username], user_switch[username], user_infer[username])
    