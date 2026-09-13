from fake_useragent import UserAgent  # 伪装请求头
from pandas import DataFrame

import chardet
import random
import requests
import time

from utils import red, green, lines, countdown


class WebRequester(object):
    """ 网页请求器 """

    @classmethod
    def get_response(cls, ua: UserAgent, url: str, method: str, date: str, bytes_out=False) -> str | bytes:
        """ 获取网页响应 """
        # 设置请求头
        headers = {
            "User-Agent": ua.random,
        }
        # 添加请求头，发送请求
        response = requests.request(url=url, method=method, headers=headers, stream=True)
        # 设置编码
        response.encoding = "utf-8"
        # 获取响应内容和类型
        result = response.text if bytes_out else response.content

        # 记录 html 信息
        cls.response_status(response.status_code)
        cls.html_writer(result, date)
        return result

    @staticmethod
    def response_status(code: int) -> None:
        status_dict = {
            200: "OK / 客户端请求成功",
            301: "Moved Permanently / 资源被永久移动到新地址",
            400: "Bad Request / 客户端不能被服务器所理解",
            401: "Unauthorized / 请求未经授权",
            403: "Forbidden / 服务器拒绝提供服务",
            404: "Not Found / 请求资源不存在",
            500: "Internal Server / 服务器发生不可预期的错误",
            503: "Service Unavailable / 服务器当前不能处理客户端的请求",
        }
        result = status_dict.get(code, "其他未知问题")
        print(green(result) if code == 200 else red(result))

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
    def html_writer(response_result: str, date: str) -> None:
        """ html 信息记录器 """
        # 构建存储路径
        file_path = f"{date} response.html"
        # 保存至 HTML 文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response_result)

    @staticmethod
    def excel_writer(df: DataFrame, file_name: str, current_time: str) -> None:
        """ Excel 信息记录器 """
        # 构建存储路径
        file_path = f"{current_time} {file_name}.xlsx"
        # 保存至 Excel 文件
        df.to_excel(file_path, sheet_name="data", index=False)
        print(f"{green(f'信息已保存至 {file_path}！')}")

    @staticmethod
    def file_writer(data: bytes | bytearray, time: str, file_suffix=None) -> str:
        """ 文件信息记录器 """
        # 构建存储路径
        file_suffix = file_suffix if file_suffix is not None else ".png"
        file_path = f"{time} code{file_suffix}"
        # 保存至文件
        with open(file_path, "wb") as f:
            f.write(data)
            print(f"{green(f'{file_path} 已保存！')}")
            lines()
        return file_path


class HTMLScraper(object):
    """ HTML 页面解析器 """

    @classmethod
    def info_scraper(cls):
        """ 信息解析器 """
        pass


@countdown
def main():
    # 获取当前时间戳
    time_stamp = time.localtime()
    # 格式化今日日期、时间
    current_date = time.strftime("%Y%m%d", time_stamp)
    current_time = time.strftime("%Y%m%d %H%M", time_stamp)

    # 实例化UA
    ua = UserAgent()

    # 目标网址
    url = "https://books.toscrape.com/"
    # 确定请求方式
    method = "GET"

    # 发起请求
    WebRequester.get_response(ua, url, method, current_date, bytes_out=True)


if __name__ == "__main__":
    main()
