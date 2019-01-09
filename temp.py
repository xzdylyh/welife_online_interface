#coding=utf8
from  urllib import urlencode
from collections import OrderedDict #有序字典
import hashlib
import time,json


#url = "https://api.acewill.net/charge/list"
appid = 'dp3Go73mm5jUiuQaWDe4W'
appkey='3ea8bfbf0574b89ae6b9e4717a34f53f'
#datas = {"begin_date":"2017-03-10","end_date":"2017-03-10","page":1,"sid2":4101315464,"cashier_id2":"1218054703","is_allday":1,"is_all":True}
ts = int(time.time())
v = 2.0
datas = {"begin_time":"9:00:00","end_time":"20:00:00","shop_id":1905736354}
url = 'https://api.acewill.net/charge/today'
fmt = 'JSON'

def sortDict(pyload):
    item = 'p.items()'
    if type(pyload).__name__=='list':
        p = sorted(pyload)
        item = 'enumerate(p)'
    if type(pyload).__name__ == 'dict':
        p=OrderedDict(sorted(pyload.items(),key=lambda a:a[0]))

    for k,v in eval(item):

        if type(v).__name__=='list':
            if not v or (v is None):
                p.pop(k)
            else:
                p[k]=list(sortDict(sorted(v)))
        elif type(v).__name__=='dict':
            if not v or (v is None):
                p.pop(k)
            else:
                p[k] =dict(sortDict(v))
            return p
        else:
            if v is None:
                p.pop(k)

    return p

#md5加密
def md5(str):
    h1 = hashlib.md5()
    h1.update(str.encode(encoding='utf-8'))
    return h1.hexdigest()

def urlencodeFunc(payload):
    newdict = {}
    payload = sortDict(payload)

    for k,v in payload.items():

        if type(v).__name__=='list':
            for i,listval in enumerate(v):
                if type(listval).__name__=='dict':
                    for m,vv in listval.items():
                        newdict['{}[{}][{}]'.format(k, i,m)] = vv
                else:
                    newdict['{}[{}]'.format(k,i)]=listval
        elif type(v).__name__=='dict':
            for ck,cv in v.items():
                i =0
                newdict['{}[{}]'.format(k, ck)] = cv
                i+=1
        else:
            newdict[k]=v

    ret= urlencode(OrderedDict(sorted(newdict.items(),key=lambda a:a[0])))

    return ret



urlcode = urlencodeFunc(datas)+'&appid='+appid+'&appkey='+appkey+'&v=2.0'+'&ts='+str(ts)
print urlcode
sig= str(md5(urlcode)).lower()

print sig

import requests


payload = '''------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"req\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"appid\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ts\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"sig\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"v\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'''
payload = payload.format(datas,appid,ts,sig,v)
print payload


print payload

headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    'postman-token': "6eb8950f-4839-3857-15e9-91a14c7e1663"
}

response = requests.request("POST", url, data=payload,headers=headers)

print(response.text)