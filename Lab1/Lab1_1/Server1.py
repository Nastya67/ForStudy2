from socket import *
import _thread
import json
addr_arr = []
BUFF = 1024
HOST = '127.0.0.1'
PORT = 5000

def read_json(name):
    file_txt = open(name).read()
    json_list = json.loads(file_txt)
    return json_list

def response(request, addr_arr):
    json_list = read_json("Books.json")
    if(request.strip() == "all books"):        
        res = json.dumps(json_list)
    elif request.find("Hello") == 0:
        res = "Hello Client"
    elif request.find("books where name") == 0:
        res = compare_str(request, "name")
    elif request.find("books where author") == 0:
        res = compare_str(request, "author")
    elif request.find("books where edition") == 0:
        res = compare_int(request, "edition")
    elif request.find("books where size") == 0:
        res = compare_int(request, "size")
    elif request.find("books where date") == 0:
        res = compare_str(request, "date")
        if(res == "not found str"):            
            if request.find("year") != -1:
                res = compare_date(request, "year")
            elif request.find("month") != -1:
                res = compare_date(request, "month")
            elif request.find("day") != -1:
                res = compare_date(request, "day")
    elif request.find("count books") == 0:
        res = str(len(json_list))
    elif request.find("all client") == 0:
        res = str(addr_arr)
    else: res = "not found"
    res = res.replace(", ", "\n")
    res = res.replace("}", "}\n")
    return res

def compare_date(request, ymd):
    json_list = read_json("Books.json")
    start = 0
    end = 0
    if ymd == "year":
        start = 0
        end = 4
    elif ymd == "month":
        start = 5
        end = 7
    elif ymd == "day":
        start = 8
        end = 10
    condition = request[request.find(ymd)+len(ymd):]
    res = []
    if(condition.find("=")!= -1) :
        name = request[request.find("=")+1:]
        for i in json_list:
            if int(i["date"][start:end]) == int(name.strip()):
                res.append(i)
        res = json.dumps(res)
    elif(condition.find("<")!= -1) :
        name = request[request.find("<")+1:]
        for i in json_list:
            if int(i["date"][start:end]) < int(name.strip()):
                res.append(i)
        res = json.dumps(res)
    elif(condition.find(">")!= -1) :
        name = request[request.find(">")+1:]
        for i in json_list:
            if int(i["date"][start:end]) > int(name.strip()):
                res.append(i)
        res = json.dumps(res)
    else : res = "not found"
    return res
    
def compare_str(request, field):
    json_list = read_json("Books.json")
    res = []
    if request.find("=") != -1:
        name = request[request.find("=")+1:]
        for i in json_list:
            if i[field] == name.strip():
                res.append(i)
        res = json.dumps(res)
    else: res = "not found str"
    return res

def compare_int(request, field):
    json_list = read_json("Books.json")
    res = []
    if request.find("=") != -1:
        name = request[request.find("=")+1:]            
        for i in json_list:
            if i[field] == int(name.strip()):
                res.append(i)
        res = json.dumps(res)
    elif request.find("<") != -1:
        name = request[request.find("<")+1:]
        for i in json_list:
            if i[field] < int(name.strip()):
                res.append(i)
        res = json.dumps(res)
    elif request.find(">") != -1:
        name = request[request.find(">")+1:]
        for i in json_list:
            if i[field] > int(name.strip()):
                res.append(i)
        res = json.dumps(res)
    else: res = "not found str"
    return res

def handler(clientsock, addr_arr, addr):
    #print("hand\n\n"+str(addr_arr)+"\n\n")
    while 1:
        data = clientsock.recv(BUFF)
        udata = data.decode("utf=8")
        if udata[:-2] == "exit": break
        print (repr(addr) + ' recv:' + udata)
        mes = response(udata.strip(), addr_arr)
        clientsock.send(bytes(mes, "utf=8"))
        print (repr(addr) + ' sent:' + mes)
        if "exit" == mes: break # to close connection from the server side
    clientsock.close()
    addr_arr.remove(addr)
    print (addr, "- closed connection")


if __name__=='__main__':
    ADDR = (HOST, PORT)
    
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    print ('waiting for connection... listening on port', PORT)    
    while 1:        
        clientsock, addr = serversock.accept()
        print ('...connected from:', addr)
        addr_arr.append(addr)
        print(addr_arr);
        print("fdsgsdg");
        print("\n\n"+str(addr_arr)+"\n\n")
        _thread.start_new_thread(handler, (clientsock, addr_arr, addr))
      #  addr_arr.remove(addr)
