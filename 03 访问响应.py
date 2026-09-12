
import requests


class WebRequester(object):
    """ 网页请求器 """
    @classmethod
    def get_response(cls, url: str) -> requests.Response:
        """ 获取网页响应 """
        response = requests.request(method="GET", url=url)
        print(f"网页请求返回结果：{response}")
        print(f"网页请求返回代码：{response.status_code}")
        print(f"网页请求返回说明：{WebRequester.response_status(response.status_code)}")
        return response

    @staticmethod
    def response_status(code: int) -> str:
        status_code = {
            200: "OK / 客户端请求成功",
            301: "Moved Permanently / 资源被永久移动到新地址",
            400: "Bad Request / 客户端不能被服务器所理解",
            401: "Unauthorized / 请求未经授权",
            403: "Forbidden / 服务器拒绝提供服务",
            404: "Not Found / 请求资源不存在",
            500: "Internal Server / 服务器发生不可预期的错误",
            503: "Service Unavailable / 服务器当前不能处理客户端的请求",
        }
        result = status_code.get(code, "其他未知问题")
        return result


def main():
    # 目标网址
    url = "http://books.toscrape.com"
    # 发送请求
    WebRequester.get_response(url)


if __name__ == "__main__":
    main()
