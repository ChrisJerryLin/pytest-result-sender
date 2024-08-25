from datetime import datetime


def pytest_configure():
    """
    在所有测试用例执行前调用。
    """
    print(f"{datetime.now()} pytest执行开始")

    print(1233456)


def pytest_unconfigure():
    """
    在所有测试用例执行完之后调用。
    """
    print(f"{datetime.now()} pytest执行结束")
