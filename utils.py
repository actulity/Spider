def get_ips():
    # ip pool
    ip_pool = []
    with open("verified.txt", "r") as f:
        while True:
            ll = f.readline()
            if not ll: break
            line = ll.strip().split('|')
            ip = line[1]
            port = line[2]
            realip = ip + ':' + port
            ip_pool.append(realip)
    return ip_pool

def get_hrefs():
    hrefs = []
    with open("href.txt", "r") as f:
        while True:
            ll = f.readline()
            if not ll: break
            line = ll.strip()
            hrefs.append(line)
    return hrefs
