from cachetools import TTLCache  # 缓存库
from fake_useragent import UserAgent  # 伪装请求头
from pandas import DataFrame

import chardet
import random
import requests
import time

from utils import red, green, yellow, lines, countdown

# 将缓存初始化放在全局作用域
cache = TTLCache(maxsize=1_000, ttl=3_600)  # 缓存有效期 1 小时


class WebRequester(object):
    """ 网页请求器 """

    @classmethod
    def cache_storager(cls, url: str, method: str, ua: UserAgent, current_time: str) -> str:
        """ 缓存存储器 """
        if url in cache:
            print(f"{green('已在缓存中！')}")
            # print(f"缓存内容：{cache}")
            return cache[url]
        else:
            print(f"{red('未在缓存中！')}")
            lines()
            # 发送请求
            response = cls.get_response(url, method, ua, current_time)
            # 缓存存储
            cache[url] = response
            # print(f"缓存已更新：{cache}")
            print(f"{yellow('缓存已更新！')}")
            lines()
            return response

    @classmethod
    def get_response(cls, url: str, method: str, ua: UserAgent, current_time: str) -> str:
        """ 获取网页响应 """
        # 设置请求头伪装
        __user_agent = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/127.0.0.0 Safari/537.36"
        )
        headers = {
            "User-Agent": ua.random,
        }
        # 添加请求头，发送请求
        response = requests.request(url=url, method=method, headers=headers, stream=True)
        print(f"网页请求返回说明：{red(WebRequester.response_status(response.status_code))}")
        lines()
        result = response.content

        # 自动检测编码
        encoding = cls.code_detector(result)
        # 使用检测到的编码
        result = result.decode(encoding)

        # 记录 html 信息
        cls.response_writer(result, current_time)
        return result

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

    @staticmethod
    def scrape_sleeper():
        """ 休眠函数 """
        sleep_time = random.randint(1, 5)
        # print(f"随机休眠 {sleep_time} 秒")
        time.sleep(sleep_time)

    @staticmethod
    def code_detector(text: bytes | bytearray) -> str:
        """ 编码检测器 """
        detector = chardet.detect(text)
        encoding = detector["encoding"]
        return encoding

    @staticmethod
    def response_writer(result: str, current_time: str) -> None:
        """ html 信息记录器 """
        # 构建存储路径
        file_path = f"{current_time} response.html"
        # 保存至 HTML 文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result)

    @staticmethod
    def excel_writer(df: DataFrame, file_name: str, current_time: str) -> None:
        """ Excel 信息记录器 """
        # 构建存储路径
        file_path = f"{current_time} {file_name}.xlsx"
        # 保存至 Excel 文件
        df.to_excel(file_path, sheet_name="data", index=False)
        print(f"{green(f'信息已保存至 {file_path}！')}")


@countdown
def main():
    # 获取当前时间戳
    time_stamp = time.localtime()
    # 格式化今日日期
    current_time = time.strftime("%Y%m%d", time_stamp)

    # 目标网址
    url = "https://books.toscrape.com/"
    # 确定请求方式
    method = "GET"
    # 实例化UA
    ua = UserAgent()

    # 设置缓存
    WebRequester.cache_storager(url, method, ua, current_time)

    # 再次调用，检查缓存存储
    WebRequester.cache_storager(url, method, ua, current_time)


if __name__ == "__main__":
    main()
