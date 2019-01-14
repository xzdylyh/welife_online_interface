#_*_coding:utf-8_*_
import unittest
from testScenario import testScenarioCase
from testInterface import testActivity,testCharge,\
    testCoupon,testCredit,testDeal,testGrade,testManage,testProduct,\
    testSearch,testTag,testUser
import os,time,json
from globalVar import gl
from library import HTMLTESTRunnerCN
from library import scripts
from library.emailstmp import EmailClass


def loadTestsList():
    list = [testUser, testTag, testSearch, testProduct, testManage, testGrade, testDeal, testCredit,
            testCoupon, testCharge, testActivity]

    tests = [unittest.TestLoader().loadTestsFromModule(testScenarioCase)]
    for module in list:
        tests.append(unittest.TestLoader().loadTestsFromModule(module))
    return tests


if __name__=="__main__":
    suite = unittest.TestSuite()
    suite.addTests(loadTestsList())

    filePath = os.path.join(gl.reportPath, 'Report.html')  # 确定生成报告的路径
    print filePath

    with file(filePath, 'wb') as fp:
        runner = HTMLTESTRunnerCN.HTMLTestRunner(
            stream=fp,
            title=u'线上-接口自动化测试报告',
            description=u'详细测试用例结果',  # 不传默认为空
            tester=u"yhleng"  # 测试人员名字，不传默认为小强
        )
        # 运行测试用例
        runner.run(suite)
        fp.close()

    #发送测试报告To Email
    EmailClass().send
