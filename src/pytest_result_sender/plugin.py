from datetime import datetime,timedelta
import pytest
import requests
import json


data={
    "passed":0,
    "failed":0,
}

def pytest_runtest_logreport(report:pytest.TestReport):
    if report.when == 'call':
        print('本次用例的执行结果',report.outcome)
        data[report.outcome] += 1

def pytest_collection_finish(session: pytest.Session):
    #用例加载完成之后执行，包含了全部用例
    data['total']=len(session.items)
    print("用例的总数：", data['total'])


def pytest_configure():
    """
    在所有测试用例执行前调用。
    """
    data['start_time']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{datetime.now()} pytest执行开始")

    print(1233456)


def pytest_unconfigure():
    """
    在所有测试用例执行完之后调用。
    """
    data['end_time']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{datetime.now()} pytest执行结束")

    data['duration'] = datetime.strptime(data['end_time'], "%Y-%m-%d %H:%M:%S") - datetime.strptime(data['start_time'], "%Y-%m-%d %H:%M:%S")
    data['pass_ratio']=data['passed']/data['total']*100
    data['pass_ratio']=f"{data['pass_ratio']:.2f}"
    #assert data['duration'] > timedelta(seconds=2.5)
    #assert data['total'] == 3
    #assert data['passed'] == 2
    #assert data['failed'] == 1

    # 替换下面的URL为您的实际Webhook URL
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/ed80416c-ce34-41e0-8c92-173850c7aada"

    # 构建消息内容
    data01 = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "Pytest测试结果：",
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": f"测试开始时间: {data['start_time']} \n"
                            },
                            {
                                "tag": "text",
                                "text": f"测试用时: {data['duration']} \n"
                            }

                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"用例总数：{data['total']}\n"
                            },
                            {
                                "tag": "text",
                                "text": f"测试通过：{data['passed']}\n"
                            },
                            {
                                "tag": "text",
                                "text": f"测试失败：{data['failed']}\n"
                            },
                            {
                                "tag": "text",
                                "text": f"测试通过率：{data['pass_ratio']}%\n"
                            }
                        ],
                        [
                            {
                                "tag": "a",
                                "text": "测试报告链接",
                                "href": "https://www.feishu.cn/"
                            }
                        ]
                    ]
                }
            }
        }
    }

    # 发送POST请求
    response = requests.post(
        webhook_url,
        data=json.dumps(data01),
        headers={'Content-Type': 'application/json'}
    )

    # 检查响应状态码
    if response.status_code == 200:
        print("消息发送成功")
    else:
        print("消息发送失败，状态码:", response.status_code)