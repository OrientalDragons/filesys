import requests as rq

# url = "http://127.0.0.1:8000/get_file"
# url = "http://127.0.0.1:8000/xxxx"
# file_to_save = './xx.xlsx'

import sys

# print ('参数个数为:', len(sys.argv), '个参数。')
# print ('参数列表:', str(sys.argv))
# print(type(sys.argv[0]))
# print(type(sys.argv[1]))
# print(type(sys.argv[2]))

url = None
file_to_save = None
method = None
try:
    if len(sys.argv) ==2:
        url = sys.argv[1]
    elif len(sys.argv) ==3:
        url = sys.argv[1]
        file_to_save = sys.argv[2]
    elif len(sys.argv) ==4:
        method = sys.argv[1]
        url = sys.argv[2]
        file_to_save = sys.argv[3]
    print(method,url,file_to_save)
    if url!=None:
        if method == None or method == 'get':

            with  rq.get(url, stream = True) as r:

                req_type= r.headers["Content-Type"]
                if  req_type== "application/json" :
                    print(req_type)
                    print(r.status_code)
                    print(r.json())
                elif req_type == "text/html; charset=utf-8":
                    print(req_type)
                    print(r.status_code)
                    print(r.text)
                else:
                    print(r.status_code)
                    chunk_size = 128
                    if file_to_save == None:
                        file_to_save = "./detail.txt"
                    with open(file_to_save, "wb") as fw:
                        for chunk in r.iter_content(chunk_size):
                            fw.write(chunk)
        elif method == 'post':

            files = {'file': open(file_to_save, 'rb')}
            r = rq.post(url, files=files)
            print(r)
            
    else:
        print("please input URL argv")

except Exception as e:
    print(e)