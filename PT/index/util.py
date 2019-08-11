import unittest
from index.hit import *
import time
import json
import HTMLTestReportCN

def start_run(case_list):
    #拼接测试用例
    try:
        FUNC_TEMPLATE = []
        FUNC_TEMPLATE.append('suite = unittest.TestSuite()\n')
        for case in case_list:
            headers = {}
            if case["headers"]:
                headers = json.loads(case["headers"])
            text = """class Test{id}(unittest.TestCase):
        '''{desc}'''
        def test_case{id}(self):
            url = '{url}'
            method = '{method}'
            type = '{type}'
            headers = {headers}
            data = '''{data}'''
            client = Client(url=url, method=method, type=type)
            client.set_headers(headers)
            client.set_body(data)
            client.send() \n""".format(
                                id=case["id"], desc=case["desc"], url=case["url"],
                                method=case["method"], type=case["body_type"], headers=headers, data=case["body_value"],
                            )
            FUNC_TEMPLATE.append(text)
            if case["checks"]:
                for c in case["checks"].split('&'):
                    if c.split('=')[0] == 'status_code':
                        FUNC_TEMPLATE.append("            client.check_status_code(%s) \n" % c.split('=')[1])
                    elif c.split('=')[0] == 'res_times_less_than':
                        FUNC_TEMPLATE.append("            client.check_res_times_less_than(%s) \n" % c.split('=')[1])
                    elif c.split('=')[0] == 'res_text_contains':
                        FUNC_TEMPLATE.append("            client.check_res_text_contains(%s) \n" % c.split('=')[1])

            run_text = 'suite.addTest(Test{id}("test_case{id}"))\n'.format(id=case["id"])
            FUNC_TEMPLATE.append(run_text)

        title = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        run_result = """HTMLTestReportCN.HTMLTestRunner(title='接口测试报告', stream=open('./index/static/reports/{title}.html', 'wb')).run(suite)""".format(
            title=title
        )
        FUNC_TEMPLATE.append(run_result)
        # print(''.join(FUNC_TEMPLATE))
        exec(''.join(FUNC_TEMPLATE))
        url = "/static/reports/{title}.html".format(title=title)
    except Exception as e:
        print(e)
        url = ''
    return url



