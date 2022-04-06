with open("peers.json", 'r') as f:
    data = eval(f.read())
    for x in data:
        ip = x[0]
        port = x[1]
    print(ip, port)
