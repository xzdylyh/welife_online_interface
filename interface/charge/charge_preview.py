#_*_coding:utf-8_*_
import requests,json
from interface_project.base.base_config import BaseConfig

from interface_project.library.scripts import getYamlfield
from interface_project.library.scripts import retry
from interface_project.globalVar import gl

class ChargeClass(object):

    url = '/charge/preview'
    payload = '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="req"\r\n\r\n{"cno":"1802326514043775","shop_id":1905736354,"cashier_id":"1131294517","money":"100","award_money2":10,"reward_money":"100","is_diy":true,"charge_type":1,"remark":"beizhu","biz_id":"1337","recommenderecode2":9002}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"appid\"\r\n\r\ndp3Go73mm5jUiuQaWDe4W\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="ts"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"sig\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="v"\r\n\r\n2.0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'

    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        'postman-token': "6eb8950f-4839-3857-15e9-91a14c7e1663"
    }

    def __init__(self):
        self.baseUrl = BaseConfig().base_url
        self.url = self.baseUrl + self.url


    #储值预览
    @property
    @retry(reNum=getYamlfield(gl.configFile)['RETRY']['ReNum'])
    def chargePreview(self):
        res = requests.request("POST",self.url,data=self.payload,headers=self.headers)
        if res.status_code ==200:
            return res.json()
        else:
            return {"errcode": 9001, "errmsg": str(res)}


if __name__=="__main__":
    print ChargeClass().chargePreview