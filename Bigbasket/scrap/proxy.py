import random


ips = ['64.225.4.12:9996', '64.225.4.12:9996']
def rand_proxy():
    proxy = random.choice(ips)
    return(proxy)
