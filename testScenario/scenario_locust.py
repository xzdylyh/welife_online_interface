#coding=utf-8
import time
from locust import HttpLocust, task, TaskSet
from library import scripts
from library.http import HttpWebRequest


class HttpTaskSet(TaskSet):
    c_data = {"cno": "1802326514043775", "shop_id": 1905736354, "cashier_id": "1180940478", "money": "100",
              "award_money2": 10, "reward_money": "100", "is_diy": 'true', "charge_type": 1, "remark": "beizhu",
              "biz_id": "37", "recommenderecode2": 9002}

    commit_data = {'biz_id': '37', 'is_diy': 'true'}

    cancel_data = {'biz_id':'37','cashier_id':'1180940478'}


    def gen_data(self, data):
        ts = int(time.time())
        sig = scripts.sign(
            data=data,
            appid='dp3Go73mm5jUiuQaWDe4W',
            appkey='3ea8bfbf0574b89ae6b9e4717a34f53f',
            v=2.0,
            ts=ts
        )
        payload,headers = scripts.MultipartPartData(
            req=data,
            sig=sig,
            appid='dp3Go73mm5jUiuQaWDe4W',
            v=2.0,
            ts=ts,
            boundary='----WebKitFormBoundary7MA4YWxkTrZu0gW'
        )
        return payload, headers

    def on_start(self):
        biz_id_01 = int(time.time()) + '007'
        #储值数据和头信息
        self.charge_data, self.charge_header = self.gen_data(self.c_data)
        self.charge_data['biz_id'] = biz_id_01
        #储值提交数据和头信息
        self.commit_data, self.commit_header = self.gen_data(self.commit_data)
        self.commit_data['biz_id'] = biz_id_01
        #储值撤销数据和头信息
        self.cancel_data, self.cancel_header = self.gen_data(self.cancel_data)
        self.cancel_data['biz_id'] = biz_id_01


    @task
    def charge(self):
        """储值"""
        self.client.headers = self.charge_header
        res = self.client.post(url='/charge/preview', data=self.charge_data)
        assert res['errcode'] == 0, res['errmsg']

    @task
    def charge_commit(self):
        """储值提交"""
        self.client.headers = self.commit_header
        res = self.client.post(url='/charge/commit', data=self.commit_data)
        assert res['errcode'] == 0, res['errmsg']

    @task
    def charge_cancel(self):
        """储值撤销"""
        self.client.headers = self.cancel_header
        res = self.client.post(url='/charge/cancel', data=self.cancel_data)
        assert res['errcode'] == 0, res['errmsg']



class WebsiteUser(HttpLocust):
    task_set = HttpTaskSet
    min_wait = 5000
    max_wait = 15000




#
# '''储值撤销场景:储值预览->储值提交->储值撤销'''
# '''--------------------------交易预览接口----------------------'''
# biz_id_01 = scripts.rndTimeStr() + '007'
#
# data = {"cno":"1802326514043775","shop_id":1905736354,"cashier_id":"1180940478","money":"100","award_money2":10,"reward_money":"100","is_diy":'true',"charge_type":1,"remark":"beizhu","biz_id":"37","recommenderecode2":9002}
# data['biz_id'] = biz_id_01
# # 整合数据，调用接口，获取返回结果
# res = scripts.loadtestInterface(
#     instance=HttpWebRequest(), instance_pro='post', data=data, appid='dp3Go73mm5jUiuQaWDe4W',
#     desc='aaa', url='/charge/preview', v='2.0'
# )
# print('储值:{}'.format(res))
# # 交易预览断言
# assert res['errcode'] == 0,res['errmsg']
#
#
# '''--------------------------交易提交接口----------------------'''
# data = {'biz_id':'37','is_diy':'true'}
# data['biz_id'] = biz_id_01
#
# # 整合数据，调用接口，获取返回结果
# commitResult = scripts.loadtestInterface(
#     instance=HttpWebRequest(), instance_pro='post', data=data, appid='dp3Go73mm5jUiuQaWDe4W',
#     desc='aaa', url='/charge/commit', v='2.0'
# )
# print('储值提交:{}'.format(commitResult))
# assert commitResult['errcode'] == 0,commitResult['errmsg'] # 交易提交断言
#
# '''--------------------------交易撤销接口----------------------'''
# data =  {'biz_id':'37','cashier_id':'1180940478'}
# data['biz_id'] = biz_id_01
#
# # 整合数据，调用接口，获取返回结果
# cancelResult = scripts.loadtestInterface(
#     instance=HttpWebRequest(), instance_pro='post', data=data, appid='dp3Go73mm5jUiuQaWDe4W',
#     desc='aaaa', url='/charge/cancel', v='2.0'
# )
# print('储值撤销:{}'.format(cancelResult))
# assert cancelResult['errcode'] == 0,cancelResult['errmsg']  # 交易撤销断言