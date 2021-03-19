import requests
import unittest
#查询发布会接口
'''
url = "http://127.0.0.1:8000/get_event_list/"
r = requests.get(url, params={'eid':'1'})
result = r.json()
print(result)
assert result['status'] == 200
assert result['message'] == "success"
assert result['data']['name'] == "小米手机发布会"
assert result['data']['address'] == "北京林匹克公园水立方"
assert result['data']['start_time'] == "2016-10-15T18:00:00"
'''
class GetEventListTest(unittest.TestCase):
    """查询发布会接口测试"""
    def setUp(self):
        self.url = "http://127.0.0.1:8000/get_event_list/"
    def test_get_event_null(self):
        '''发布会 id 为空'''
        r = requests.get(self.url, params={'eid': ''})
        result = r.json()
        print(result)
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], "parameter error")
    def test_get_event_success(self):
        '''发布会 id 为 1，查询成功'''
        r = requests.get(self.url, params={'eid': '1'})
        result = r.json()
        print(result)
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], "success")
        self.assertEqual(result['data']['name'], "xx 产品发布会")
        self.assertEqual(result['data']['address'], "北京林匹克公园水立方")
        self.assertEqual(result['data']['start_time'], "2016-10-15T18:00:00")
if __name__ == '__main__':
    unittest.main()
