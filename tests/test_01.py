import pytest
from pytest_result_sender import plugin
from pathlib import Path

#告诉框架，这是插件的测试
pytest_plugins='pytester'

@pytest.fixture(autouse=True)
def mock():
    bak_data=plugin.data
    plugin.data={
        "passed": 0,
        "failed": 0,
    }
    yield
    #恢复测试环境
    plugin.data=bak_data


@pytest.mark.parametrize(
    'send_when',
    ['every','on_fail']
)
def test_send_when(send_when, pytester : pytest.Pytester, tmp_path: Path):
    config_path=tmp_path.joinpath("pytest.ini")
    config_path.write_text(f"""
[pytest]
send_when = {send_when}
send_api=https://open.feishu.cn/open-apis/bot/v2/hook/ed80416c-ce34-41e0-8c92-173850c7aada
    """)
    # 断言配置加载成功
    config=pytester.parseconfig(config_path)
    assert config.getini('send_when') == send_when

    pytester.makepyfile( #构造全部用例通过的场景
        """
        def test_pass():
            ...
        """
    )
    pytester.runpytest("-c",str(config_path))

    if send_when == 'every':
        assert plugin.data['send_done'] ==1
    else:
        assert plugin.data.get('send_done') is None

@pytest.mark.parametrize(
    'send_api',
    ['','https://open.feishu.cn/open-apis/bot/v2/hook/ed80416c-ce34-41e0-8c92-173850c7aada']
)
def test_send_api(send_api, pytester : pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(f"""
[pytest]
send_when = every
send_api={send_api}
        """)
    # 断言配置加载成功
    config = pytester.parseconfig(config_path)
    assert config.getini('send_api') == send_api

    pytester.makepyfile(  # 构造全部用例通过的场景
        """
        def test_pass():
            ...
        """
    )
    pytester.runpytest("-c", str(config_path))
    if send_api :
        assert plugin.data['send_done'] ==1
    else:
        assert plugin.data.get('send_done') is None
