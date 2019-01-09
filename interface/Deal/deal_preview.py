#_*_coding:utf-8_*_
import requests,json
from interface_project.base.base_config import BaseConfig
from interface_project.library.scripts import getYamlfield
from interface_project.library.scripts import retry
from interface_project.globalVar import gl

class DealClass(object):
    url = "/deal/preview"
    payload = '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="req"\r\n\r\n{"cno":"1262797","shop_id":1112645845,"cashier_id":"1218054703","consume_amount":100,"sub_balance":100, "deno_coupon_ids":[""],"gift_coupons_ids":[""],"sub_credit":0,"activity_ids2":["0"],"payment_amount":0,"credit_amount":0,"payment_mode":1,"count_num":2,"biz_id":8036,"table_id":"A023","tags2":["舌尖上的中国"],"diy_gift_coupon_pay2":[{"user_coupon_id":"","deno":100}],"products2":[{"name":"388","no":388,"num": "1","price":"100","is_activity":1,"coupons_ids2":["1597533836855947312"],"tags2":["来自中国的美味"]}]}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="appid"\r\n\r\ndp1svA1gkNt8cQMkoIv7HmD1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="ts"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="sig"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="v"\r\n\r\n2.0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        'postman-token': "6eb8950f-4839-3857-15e9-91a14c7e1663"
    }

    def __init__(self):
        self.baseUrl  = BaseConfig().base_url
        self.url = self.baseUrl + self.url


    #消费预览
    @property
    @retry(reNum=getYamlfield(gl.configFile)['RETRY']['ReNum'])
    def dealPreview(self):
        res = requests.request("POST",self.url,data=self.payload,headers=self.headers)
        if res.status_code ==200:
            return res.json()
        else:
            return {"errcode": 9001, "errmsg": str(res)}


if __name__=="__main__":
    print json.dumps(DealClass().dealPreview).decode('unicode-escape')