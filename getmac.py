import uuid
def get_mac_address():
    """
    获取本机物理地址，获取本机mac地址
    :return:
    """
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:].upper()
    return "-".join([mac[e:e+2] for e in range(0,11,2)])
if __name__ == '__main__':
    mac = get_mac_address()
    print('本机物理地址：',mac)
