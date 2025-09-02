# 开发人员   :   hp
# 开发时间   :   2025/9/2  19:37
# 文件名称   :   aa.py
# 开发工具   :   PyCharm
import requests

url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0b071223-c81a-44eb-ace4-0467522e8970"

content = """
pytest自动化测试结果

测试时间：xxx <br/>
用例数量：3 <br/>
执行时长:xxx <br/>
测试通过用例数：<font color = "green"> 2 </font><br/>
测试失败用例数：<font color = "red"> 1 </font> <br/>
测试通过率：<font color = "blue"> 66.67% </font> <br/>

测试报告地址：www.baidu.com <br/>
"""
requests.post(url, json={"msgtype": "markdown", "markdown": {"content": content}})
