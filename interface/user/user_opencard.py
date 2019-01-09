#_*_coding:utf-8_*_
import requests,json
from interface_project.base.base_config import BaseConfig
from interface_project.library.scripts import getYamlfield
from interface_project.library.scripts import retry
from interface_project.globalVar import gl

class DealClass(object):
    url = "/user/opencard"
    payload = '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="req"\r\n\r\n{"phone":"13800138188","acno":"1109662303541283","sid":"1429830612","username":"宙斯普罗米修斯","gender":1,"birthday":"1998-01-01","birthflay":0,"password":"000000","code2":708537}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="appid"\r\n\r\ndp1svA1gkNt8cQMkoIv7HmD1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="ts"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="sig"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="v"\r\n\r\n2.0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        'postman-token': "6eb8950f-4839-3857-15e9-91a14c7e1663"
    }

    def __init__(self):
        self.baseUrl  = BaseConfig().base_url
        self.url = self.baseUrl + self.url


    #
    @property
    @retry(reNum=getYamlfield(gl.configFile)['RETRY']['ReNum'])
    def userOpencard(self):
        res = requests.request("POST",self.url,data=self.payload,headers=self.headers)
        if res.status_code ==200:
            return res.json()
        else:
            return {"errcode": 9001, "errmsg": str(res)}

if __name__=="__main__":
    print json.dumps(DealClass().userOpencard).decode('unicode-escape')