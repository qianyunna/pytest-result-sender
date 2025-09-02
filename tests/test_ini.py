# 开发人员   :   hp
# 开发时间   :   2025/9/3  19:00
# 文件名称   :   test_ini.py
# 开发工具   :   PyCharm
from pathlib import Path

import pytest

from pytest_result_sender import plugin

# pytester是内部模块，一般不会被使用，所以需要声明。
pytest_plugins = "pytester"  # 声明：”我是测试开发“


@pytest.fixture(autouse=True)
def mock():
    bak_data = plugin.data
    bak_data = {
        "passed": 0,
        "failed": 0,
    }
    # 创建一个干净的测试环境
    yield
    # 恢复测试环境
    plugin.data = bak_data

@pytest.mark.parametrize("send_time", ["every", "on_fail"])
def test_send_time(send_time, pytester: pytest.Pytester, tmp_path: Path):
    # 创建pytest临时配置文件，并写入相关参数
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(f"""
[pytest]
send_time = {send_time}
send_api = https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0b071223-c81a-44eb-ace4-0467522e8970
""")
    # 使用pytester对象加载上一步创建的临时配置文件，测试是否一致
    # 断言，配置加载成功
    config = pytester.parseconfig(config_path)
    assert config.getini("send_time") == send_time

    # 构造场景：所有测试用例全部通过
    # 运行测试用例
    pytester.makepyfile(
        """
    def testfile():
        pass
    """
    )
    pytester.runpytest("-c", str(config_path))
    # 判断插件是否发送报告
    print(plugin.data)
    if send_time == "every":
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None


@pytest.mark.parametrize(
    "send_api",
    [
        "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0b071223-c81a-44eb-ace4-0467522e8970",
        "",
    ],
)
def test_send_api(send_api, pytester: pytest.Pytester, tmp_path: Path):
    # 创建pytest临时配置文件，并写入相关参数
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"""
[pytest]
send_time = "every"
send_api = {send_api}
            """
    )
    # 使用pytester对象加载上一步创建的临时配置文件，测试是否一致
    # 断言，配置加载成功
    config = pytester.parseconfig(config_path)
    assert config.getini("send_api") == send_api

    # 构造场景：所有测试用例全部通过
    # 运行测试用例
    pytester.makepyfile(
        """
        def testfile():
            pass
        """
    )
    pytester.runpytest("-c", str(config_path))
    # 判断插件是否发送报告
    print(plugin.data)
    if send_api:
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None
