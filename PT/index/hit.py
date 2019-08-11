import unittest
import requests
import json


class Client(unittest.TestCase):

    def __init__(self, url, method, type='none'):
        self.url = url
        self.method = method
        self.body_type = type
        self.res = None
        self.headers = {}
        self.body = {}
        self._type_equality_funcs = {}

    def send(self):
        if self.method == 'GET':
            self.res = requests.get(url=self.url, headers=self.headers)
        elif self.method == 'POST':
            if self.body_type == 'FORM':
                self.res = requests.post(url=self.url, headers=self.headers, data=self.body)
            elif self.body_type == 'URL-ENCODE':
                self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
                self.res = requests.post(url=self.url, headers=self.headers, data=self.body)
            elif self.body_type == 'JSON':
                self.headers['Content-Type'] = 'application/json'
                self.res = requests.post(url=self.url, headers=self.headers, data=json.loads(self.body))
            elif self.body_type == 'XML':
                self.headers['Content-Type'] = 'text/xml'
                self.res = requests.post(url=self.url, headers=self.headers, data=self.body.get('xml'))
            elif self.body_type == 'NONE':
                self.res = requests.post(url=self.url, headers=self.headers)
            else:
                raise Exception('不支持的正文格式')
        else:
            raise Exception('不支持的请求方法类型')

    def set_headers(self, headers):
        self.headers = headers

    def set_body(self, body):
        self.body = body

    @property
    def text(self):
        if self.res:
            return self.res.text
        else:
            return None

    @property
    def status_code(self):
        if self.res:
            return self.res.status_code
        else:
            return None

    @property
    def res_cookies(self):
        if self.res:
            return requests.utils.dict_from_cookiejar(self.res.cookies)
        else:
            return None

    @property
    def res_headers(self):
        if self.res:
            return self.res.headers
        else:
            return None

    @property
    def res_time(self):
        if self.res:
            return round(self.res.elapsed.total_seconds() * 1000)
        else:
            return None

    def res_to_json(self):
        if self.res:
            try:
                return self.res.json()
            except:
                return None
        else:
            return None

    def check_res_times_less_than(self, exp):
        self.assertLess(self.res_time, exp,
        '响应时间异常：实际结果[{act}], 预期结果[{exp}]'.
                        format(act=self.res_time, exp=exp))
        print('响应时间正确')

    def check_status_code(self, exp):
        self.assertEqual(self.status_code, exp,
         '响应状态码异常：实际结果[{act}], 预期结果[{exp}]'.
                         format(act=self.status_code, exp=exp))
        print('响应状态码正确')

    def check_res_text_contains(self, exp):
        self.assertEqual(exp in self.text, True,
        '响应内容包含异常：实际结果[{act}], 预期结果[{exp}]'.format(act=self.text, exp=exp))
        print('响应内容已包含预期值')
