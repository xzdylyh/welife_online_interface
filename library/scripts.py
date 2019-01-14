#_*_coding:utf-8_*_
from library.log import LogDebug
import time,os,random
import yaml,json,hashlib
from requests_toolbelt.multipart.encoder import MultipartEncoder
from collections import OrderedDict
from urllib import urlencode,quote
import urllib
from globalVar import gl
from requests.exceptions import (
    ConnectTimeout,
    ConnectionError,
    Timeout,
    HTTPError
)


'''
#日期时间串
'''
def rndTimeStr():
    """
    随机字符串
    :return: 日期时间
    """
    time.sleep(1)
    curTimeStr = str(time.strftime('%Y%m%d%H%M%S', time.localtime()).encode('utf-8'))
    #LogDebug().info('生成日期时间串%s'%curTimeStr)
    return curTimeStr.decode('utf-8')

@property
def timeStamp():
    """
    秒级时间戳
    :return: 时间戳
    """
    return int(time.time())

'''
写yaml内容
'''
def writeYmal(yamlPath,data):
    """
    写yaml文件
    :param yamlPath: yaml文件路径
    :param data: 数据内容
    :return: 无
    """
    with open(yamlPath,'wb') as fp:
        yaml.dump(data,fp)
        fp.close()



'''
读yaml文件
'''
def getYamlfield(yamlpath):
    """
    获取yaml配置内容
    :param yamlpath: yaml文件路径
    :return: 返回字典所有内容
    """
    with open(yamlpath,'rb') as fp:
        cont = fp.read()
        fp.close()
    ret = yaml.load(cont)
    return ret



#raw multipart form-data #格式不可动
def MultipartFormData(data,appid ='dp1svA1gkNt8cQMkoIv7HmD1',sig=1,ts=1,v=2.0):
    """
    按特定格式生成接口测试数据
    :param data: 主体数据
    :param appid: 特殊数据
    :param sig: 特殊数据
    :param ts: 特殊数据
    :return: 生成的完整数据
    """
    ts = int(time.time()) #请求时间戳
    data = json.dumps(data).decode('unicode-escape')
    LogDebug().info('------------------START----------------')
    LogDebug().info('请求数据:{0}'.format(data))
    LogDebug().info('请求Appid:{0}'.format(appid))
    payload = '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"req\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"appid\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ts\"\r\n\r\n%d\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"sig\"\r\n\r\n%d\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"v\"\r\n\r\n2.0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--' % (data,appid,ts,sig)

    return payload


#获取配置文件中,运行标记
def getRunFlag(scenarioKey):
    """
    获取配置文件中执行标记
    :param scenarioKey: 场景字段
    :return: 标记值;Y or N
    """
    yamldict = getYamlfield(gl.configFile)
    flagRet = yamldict['RUNING'][scenarioKey]['Flag']
    LogDebug().info('{0}执行标记:{1}'.format(scenarioKey,flagRet))
    return flagRet


def loadDdtData(Itype='t', filename='Charge.yaml', caseflag='CHARGE_CASE1'):
    """
    从yaml加载ddt数据
    :param Itype: t:tcode; s:scenario
    :param filename: 'Charge.yaml'
    :param caseflag:  yaml中接口case的起始节点
    :return: ddt数据list
    """
    ddtData = []
    if Itype == 't':
        configDir = gl.tcodePath
    else:
        configDir = gl.dataScenarioPath

    #拼接yam数据路径，并读取数据内容
    yamfpath = os.path.join(configDir, filename)
    readYam = getYamlfield(yamfpath)

    dictCase = readYam[caseflag]

    #循环遍历，配置数据中节点下，所以case开头用例
    for key in dictCase:
        #配置数据中以case开头的，被认为是一条用例
        if str(key).lower().startswith('case'):

            if Itype =='t':
                # 为每个case添加一个Url
                dictCase[key]['Url'] = dictCase['Url']

            #组织ddt[]数据，每一条case为一个dict对象
            ddtData.append(dictCase[key])

    return ddtData



def loadtestInterface(**kwargs):
    """
    整合，接口数据，并调用
    :param kwargs: 接口相关数据
    instance=类实例
    instance_pro=接口方法属性
    url=接口相对url
    data=接口数据字典
    appid=程序id
    desc=接口描述
    :return: 接口返回结果
    """
    OUT_TMPL = """用例描述-->{}\r\n请求:{}\r\n{}\r\nAppid:{}\r\n响应:\r\n{}"""

    #实例
    view = kwargs['instance']
    view.url =kwargs['url']

    data = kwargs['data']
    appid = kwargs['appid']

    ts = int(time.time())

    """设置一些参数默认值，如果不传参数，值默认"""
    if kwargs.has_key('v'):
        v = kwargs['v']
    else:
        v = '2.0'

    #设置一个appkey默认值
    if kwargs.has_key('Appkey'):
        appkey = kwargs['Appkey']
    else:
        appkey = '3ea8bfbf0574b89ae6b9e4717a34f53f'

    #生成sig签名,md5串
    sig = sign(data=data, appid=appid, appkey=appkey, v=v, ts=ts)

    #给http接口，数据和头信赋值
    view.payload,view.headers = MultipartPartData(
        req=data,
        sig=sig,
        appid=appid,
        v=v,
        ts=ts,
        boundary='----WebKitFormBoundary7MA4YWxkTrZu0gW'
    )

    #调用接口,需注意的是，aetatt，接口函数，必须@property装饰成属性
    viewResult = getattr(view, kwargs['instance_pro'])

    """报告输出，格式模版"""
    print OUT_TMPL.format(
        kwargs['desc'],
        kwargs['url'],
        json.dumps(kwargs['data']).decode('unicode-escape'),
        kwargs['appid'],
        json.dumps(viewResult).decode('unicode-escape')
    )

    return viewResult




def retry(**kw):
    """
    装饰器：http请求，出错重试功能
    :param arg: ()元组，异常类
    :param kw: reNum = n；n为重试次数
    :return: 函数本身
    """
    def wrapper(func):
        def _wrapper(*args,**kwargs):
            raise_ex = None
            for n in range(kw['reNum']):
                try:
                    ret = func(*args,**kwargs)
                    time.sleep(random.randint(1,3))
                    return ret
                except (ConnectTimeout,ConnectionError,Timeout,HTTPError) as ex:
                    raise_ex = ex
                    LogDebug().info(raise_ex)
                LogDebug().warning('重新发送请求:第{0}次'.format(n))
            #raise raise_ex
        return _wrapper
    return wrapper



def rmDirsAndFiles(dirpath):
    """
    删除目标,目录下文件及文件夹
    :param dirpath: 目标目录
    :return: 无
    """
    listdir = os.listdir(dirpath)
    if listdir:
        for f in listdir:
            filepath = os.path.join(dirpath,f)
            if os.path.isfile(filepath):
                os.remove(filepath)
            if os.path.isdir(filepath):
                os.rmdir(filepath)

def sortDict(pyload):
    """
    字典数据递归排序，包含列表排序
    :param pyload: 字典数据
    :return: 排序后的OrderedDict字典
    """
    item = 'p.items()'
    if type(pyload).__name__=='list':
        p = sorted(pyload)
        item = 'enumerate(p)'
    elif type(pyload).__name__ == 'dict':
        p=OrderedDict(sorted(pyload.items(),key=lambda a:a[0]))
    else:
        p = quote(pyload)

    for k,v in eval(item):

        if type(v).__name__=='list':
            if not v or (v is None) or v=="":
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
    """
    MD5加密
    :param str: 目标字符串
    :return: md5串
    """
    h1 = hashlib.md5()
    h1.update(str.encode(encoding='utf-8'))
    return h1.hexdigest()

def urlencodeFunc(payload):
    """
    生成url键值对
    :param payload: post数据
    :return: url键值对
    """
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

def sign(**kwargs):
    """
    根据微生活sig签名算法，生成sig签名md5
    :param kwargs: 参与签名的参数
    :return: sig签名md5字符串
    """

    #处理发送数据为空{}
    if kwargs['data']:
        URL_TMP='{}&appid={}&appkey={}&v={}&ts={}'
    else:
        URL_TMP = '{}appid={}&appkey={}&v={}&ts={}'

    urlcode =URL_TMP.format(
        urlencodeFunc(kwargs['data']),
        kwargs['appid'],
        kwargs['appkey'],
        kwargs['v'],
        kwargs['ts']
    )

    sig= str(md5(urlcode)).lower()
    return sig


def MultipartPartData(**kwargs):
    """
    返回form-data对象，及头信息
    :param kwargs:
    :return: Me为form-data对象；He为头对象
    """

    #取到form-data中的boundary特征字符串，之后删除该key
    by = str(kwargs['boundary'])
    kwargs.pop('boundary' )

    #字典内，所有值转成str
    for k,v in kwargs.items():
        #如果是字典，通过json.dumps转成str类型，否则报错
        if type(v).__name__=='dict':
            kwargs[k] = json.dumps(v)
        else:
            kwargs[k] = str(v)

    Me = MultipartEncoder(
        fields=kwargs,
        boundary=by
    )

    #头信息
    headers = {'cache-control': "no-cache"}
    headers['Content-Type'] = Me.content_type

    return Me,headers


if __name__=="__main__":
    print json.dumps(getRunFlag('testCouponSendAndCancel')).decode('unicode-escape')

