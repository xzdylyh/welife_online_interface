#_*_coding:utf-8_*_
import unittest
import shutil
from testScenario import testScenarioCase
from testInterface import testActivity,testCharge,\
    testCoupon,testCredit,testDeal,testGrade,testManage,testProduct,\
    testSearch,testTag,testUser
import os,time,json
from globalVar import gl
from library import HTMLTESTRunnerCN
from library import scripts
from library.emailstmp import EmailClass


class run_test_case(object):

    @classmethod
    def load_tests_list(cls):
        """
        指定加载测试用例顺序
        :return:
        """
        list = [testUser, testTag, testSearch, testProduct, testManage, testGrade, testDeal, testCredit,
                testCoupon, testCharge, testActivity]

        tests = [unittest.TestLoader().loadTestsFromModule(testScenarioCase)]
        for module in list:
            tests.append(unittest.TestLoader().loadTestsFromModule(module))
        return tests

    @classmethod
    def create_report_file(cls):
        #测试报告文件名
        time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        report_dir = time_str.split('_')[0]
        cls.file_name = 'Report_{}.html'.format(time_str)
        portdir = os.path.join(gl.reportPath, report_dir)

        #按日期创建测试报告文件夹
        if not os.path.exists(portdir):
            os.mkdir(os.path.join(gl.reportPath,report_dir))
        rpath = os.path.join(gl.reportPath, report_dir)
        cls.filePath = os.path.join(rpath, cls.file_name)  # 确定生成报告的路径

        return cls.filePath

    @staticmethod
    def copy_report(filePath, file_name):
        # 复制report下子文件夹到 templates/report/下
        split_path = os.path.dirname(filePath).split("\\")
        low_path = split_path[split_path.__len__() - 1]
        web_path = os.path.join(gl.templatesReportPath, low_path)
        if not os.path.exists(web_path):
            shutil.copytree(os.path.dirname(filePath), web_path)
        else:
            shutil.copy(filePath, os.path.join(web_path, file_name))
        return low_path

    @staticmethod
    def tmpl_msg(low_path, file_name):
        # 发送钉钉模版测试结果
        result_str = """共{}个用例, 通过{}, 失败{}, 错误{}, 通过率{}""".format(
            gl.get_value('sum_case'),
            gl.get_value('success_count'),
            gl.get_value('failure_count'),
            gl.get_value('error_count'),
            gl.get_value('passrate')
        )

        # 测试结论
        if '100' in str(gl.get_value('passrate')):
            msg_1 = '本次测试★通过★'
        else:
            msg_1 = '本次测试★不通过★'

        # 发送钉钉消息
        msg = """线上接口自动化测试已完成:{},{}\n测试报告地址:http://60.205.217.8:5001/report/{}/{}"""
        msg = msg.format(result_str,msg_1 , low_path, file_name)

        return msg

    @staticmethod
    def run(filePath):
        """
        去行unittest并生成报告
        :param filePath: report.html绝对路径
        :return: 无
        """
        # unittest测试套件
        suite = unittest.TestSuite()
        suite.addTests(run_test_case.load_tests_list())

        # 执行测试并生成测试报告文件
        with file(filePath, 'wb') as fp:
            runner = HTMLTESTRunnerCN.HTMLTestRunner(
                stream=fp,
                title=u'线上-接口自动化测试报告',
                description=u'详细测试用例结果',  # 不传默认为空
                tester=u"yhleng"  # 测试人员名字，不传默认为小强
            )
            # 运行测试用例
            runner.run(suite)

    @staticmethod
    def invoke():
        """
        开始执行测试生成测试报告
        :return:
        """
        # 测试报告文件名
        time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        filePath = run_test_case.create_report_file()
        print(filePath)

        # 开始测试发送钉钉消息
        scripts.send_msg_dding('{}:★开始API接口自动化测试★......'.format(time_str))

        # 执行测试并生成测试报告文件
        run_test_case.run(filePath)

        # 复制report下子文件夹到 templates/report/下
        low_path = run_test_case.copy_report(filePath, run_test_case.file_name)

        # 模版消息
        msg = run_test_case.tmpl_msg(low_path, run_test_case.file_name)
        print(msg)
        scripts.send_msg_dding(msg)

        # 发送测试报告To Email
        email = EmailClass()
        email.send(filePath)


if __name__=="__main__":
    run_test_case.invoke()