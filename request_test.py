#coding=utf-8
import requests
import json
from requests import exceptions
from contextlib import closing
#请求百度网页  
URL = 'https://api.github.com'
URL = 'http://192.168.2.110:8888'

def build_uri(endpoint):
    return '/'.join([URL, endpoint])  # 主要作用是拼接接口请求地址


def better_output(json_str):
    return json.dumps(json.loads(json_str), indent=4) #采用json里面提供方法打印出来，格式更好看


def request_method():
    response = requests.get(build_uri('user?relation_type=phone&relation_ids=16267893305')) #调用get方法，注意用户名这个地方写法，没有图片中冒号
    print(response.text) #调用json更好格式输出

def params_method():
    response = requests.get(build_uri('users'), params = {'since': 11} )
    print(better_output(response.text))
    print(response.headers)
    print(response.url)

def json_method():
    response = requests.patch(build_uri('user'), auth=('WeberXu1', 'jayyanhua1'), json={'name':'Weber.Xu'})
    print(better_output(response.text))
    print(response.headers)
    print(response.url)

def post_method():
    response = requests.post(build_uri('user/emails'), auth=('WeberXu1', 'jayyanhua1'), json=['weberxu1@gmail.com'])
    print(better_output(response.text))
    print(response.headers)
    print(response.url)

def delete_method():
    response = requests.delete(build_uri('user/emails'), auth=('WeberXu1', 'jayyanhua1'), json=['weberxu1@gmail.com'])
    print(response.headers)
    print(response.url)


def timeout_request():
    try:
        response = requests.get(build_uri('user/emails'), auth=('WeberXu1', 'jayyanhua1'), timeout=0.01)
    except exceptions.Timeout as e:
        print(str(e))
    else:
        print(response.text)


def custom_request():
    from requests import Request, Session
    s = Session()  # 初始化一个session
    headers = {'User-Agent': 'fake1.3.4'}  # fake是伪装的意思，就是设置一个假的
    request = Request('GET', build_uri('user/emails'), auth=('WeberXu1', 'jayyanhua1'), headers=headers)
    prepped = request.prepare()  # 初始化一个prepare对象，用来包装请求的headers和body
    print(prepped.body)  # 打印出来应该是空，毕竟目前还没有发送请求
    print(prepped.headers)

    response = s.send(prepped, timeout=5)  # 通过session对象调用发送请求，内容是prepped包装好的请求
    print(response.status_code)
    print(response.headers)
    print(response.text)


def download_image():
    url = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1504068152047&di=8b53bf6b8e5deb64c8ac726e260091aa&imgtype=0&src=http%3A%2F%2Fpic.baike.soso.com%2Fp%2F20140415%2Fbki-20140415104220-671149140.jpg'

    response = requests.get(url)
    with closing(requests.get(url, stream=True)) as response:
        # 这里打开一个空的png文件，相当于创建一个空的txt文件,wb表示写文件
        with open('selenium2.png', 'wb') as file:
            # 每128个流遍历一次
            for data in response.iter_content(128):
                # 把流写入到文件，这个文件最后写入完成就是，selenium.png
                file.write(data)

    print(response.status_code)


def oauth_auth():
    headers = {'Authorization': 'token 0f99445c3239715e82c96076f82413bd8557b1c7'}
    # 获取user/email信息
    response = requests.get(build_uri('user/emails'), headers=headers)
    print(response.status_code)
    print(response.text)
    print(response.request.headers)

if __name__ == '__main__':
    request_method()