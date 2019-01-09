#coding=utf-8
import time, random, string
import requests
import json
from locust import HttpLocust, task, TaskSet, events
from library import scripts
# from gevent._semaphore import Semaphore
#
# all_locusts_spawned = Semaphore()
# all_locusts_spawned.acquire()
#
# def on_hatch_complete(**kwargs):
#     all_locusts_spawned.release()
#
# events.hatch_complete += on_hatch_complete

class HttpTaskSet(TaskSet):
    c_data = {"cno": "1586313249694323", "shop_id": 1905736354, "cashier_id": "1180940478", "money": "100",
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
        return payload,headers

    def genrandomstr(self, lenstr):
        """
        随机产生数据
        :param lenstr: 需要字符串的长度,
        :return: 指定长度的字符和数字组合的字符串，例如：lenstr=5，"Qamo8"
        """
        strs = "".join(random.choice(string.ascii_letters + string.digits)
                       for _ in range(lenstr)
                       )
        return strs



    @task
    def charge(self):
        biz_id_01 = '{}{}'.format(int(time.time()),self.genrandomstr(5))
        #储值数据和头信息
        self.c_data['biz_id'] = biz_id_01
        self.charge_data, self.charge_header = self.gen_data(self.c_data)

        #储值提交数据和头信息
        self.commit_data['biz_id'] = biz_id_01
        self.commit, self.commit_header = self.gen_data(self.commit_data)

        #储值撤销数据和头信息
        self.cancel_data['biz_id'] = biz_id_01
        self.cancel, self.cancel_header = self.gen_data(self.cancel_data)

        # all_locusts_spawned.wait()
        """储值"""
        self.client.headers = self.charge_header
        res = self.client.post(
            url='https://api.acewill.net/charge/preview',
            data=self.charge_data,
            catch_response=True
        )
        if res.status_code ==200:
            if res.json()['errcode'] == 0:
                res.success()
            else:
                res.failure(res.json()['errmsg'])
        else:
            res.failure(str(res))



        """储值提交"""
        self.client.headers = self.commit_header
        res_commit = self.client.post(
            url='https://api.acewill.net/charge/commit',
            data=self.commit,
            catch_response=True
        )

        if res_commit.status_code ==200:
            if res_commit.json()['errcode'] == 0:
                res_commit.success()
            else:
                res_commit.failure(res_commit.json()['errmsg'])
        else:
            res_commit.failure(str(res_commit))


        """储值撤销"""
        self.client.headers = self.cancel_header
        res_cancel = self.client.post(url='https://api.acewill.net/charge/cancel', data=self.cancel, catch_response=True)

        if res_cancel.status_code ==200:
            if res_cancel.json()['errcode'] == 0:
                res_cancel.success()
            else:
                res_cancel.failure(res_cancel.json()['errmsg'])
        else:
            res_cancel.failure(str(res_cancel))



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