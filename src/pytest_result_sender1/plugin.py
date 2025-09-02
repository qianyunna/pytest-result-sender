# 开发人员   :   hp
# 开发时间   :   2025/9/2  18:13
# 文件名称   :   plugin.py
# 开发工具   :   PyCharm
from datetime import datetime

import pytest
import requests

data = {
    "passed": 0,
    "failed": 0
}


# 添加配置
def pytest_addoption(parser):
    parser.addini("send_time", help="发送时机")
    parser.addini("send_api", help="发送地址")


# 测试用例结果是否准确
def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == "call":
        data[report.outcome] += 1


# 测试用例数量是否
def pytest_collection_finish(session: pytest.Session):
    # 所有用例执行完之后运行，包含所有用例
    data["total"] = len(session.items)
    print("用例总量:", data["total"])


# 测试开始时间、结束时间是否准确
def pytest_configure(config: pytest.Config):
    data["startTime"] = datetime.now()
    # 配置加载完毕之后执行，所有测试用例执行之前执行
    print(f"{datetime.now()} pytest 开始执行！")
    data["send_time"] = config.getini("send_time")
    data["send_api"] = config.getini("send_api")


def pytest_unconfigure():
    try:
        # 配置卸载完毕之后执行，所有测试用例执行之后执行
        data["endTime"] = datetime.now()
        print(f"{datetime.now()} pytest 结束执行！")
        data["duration"] = data["endTime"] - data["startTime"]
        data["passRatio"] = data["passed"] / data["total"] * 100
        data["passRatio"] = f"{data['passRatio']:.2f}%"

        # assert timedelta(seconds=2.5) < data["duration"] < timedelta(seconds=3)
        # assert data['total'] == 3
        # assert data['passed'] == 2
        # assert data['failed'] == 1
        # assert  data['passRatio'] == "66.67%"
        send_result()
    except KeyError:
        pass



def send_result():
    if not data["send_api"]:
        return
    if data["send_time"] == "on_fail" and data["failed"] == 0:
        return

    url = data["send_api"]
    content = f"""
    pytest自动化测试结果

    测试时间：{data['startTime']}
    用例数量：{data['total']}
    执行时长: {data['duration']}
    测试通过用例数：<font color = "green"> {data['passed']} </font>
    测试失败用例数：<font color = "red"> {data['failed']} </font>
    测试通过率：<font color = "blue"> {data['passRatio']} </font>

    测试报告地址：www.baidu.com
    """
    try:
        requests.post(
            url, json={"msgtype": "markdown", "markdown": {"content": content}}
        )
    except Exception:
        pass

    data["send_done"] = 1


