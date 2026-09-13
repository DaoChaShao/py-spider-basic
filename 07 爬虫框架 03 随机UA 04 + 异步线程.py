from fake_useragent import UserAgent  # 伪装请求头
from pandas import DataFrame

import base64
import os
import random
import requests
import time

from utils import red, green, lines, yellow, countdown


class WebsiteRequester(object):
    """ 网页请求器 """

    @classmethod
    def response_get(cls, ua: UserAgent, url: str, c_date: str, bytes_out=True) -> str | bytes:
        """ 发送 GET 请求 """
        # 设置请求头
        headers = {
            "User-Agent": ua.random,
        }
        # 添加请求头，发送请求
        response = requests.get(url=url, headers=headers, stream=True, timeout=10)
        # 设置编码
        response.encoding = "utf-8"
        # 获取响应内容和类型
        result = response.content if bytes_out else response.text

        # 记录 html 信息
        if isinstance(result, bytes):
            return result
        else:
            cls.response_status(response.status_code)
            cls.html_writer(result, c_date, get=True)
            return result

    @classmethod
    def response_post(cls, ua: UserAgent, url: str, c_date: str) -> str | bytes:
        """ 发送 POST 请求 """
        # 设置请求头
        headers = {
            "User-Agent": ua.random,
        }
        # 设置请求参数
        payload = {
            "username": "admin",
            "password": "123456",
        }
        # 添加请求头，发送请求
        response = requests.post(url=url, headers=headers, stream=True, timeout=30, data=payload)
        # 设置编码
        response.encoding = "utf-8"
        # 获取响应内容和类型
        result = response.text

        # 记录 html 信息
        cls.response_status(response.status_code)
        cls.html_writer(result, c_date, get=False)
        return result

    @staticmethod
    def response_status(code: int) -> None:
        status_dict = {
            200: "OK / 客户端请求成功",
            301: "Moved Permanently / 资源被永久移动到新地址",
            302: "Found / 资源被临时移动到新地址",
            400: "Bad Request / 客户端不能被服务器所理解",
            401: "Unauthorized / 请求未经授权",
            403: "Forbidden / 服务器拒绝提供服务",
            404: "Not Found / 请求资源不存在",
            500: "Internal Server / 服务器发生不可预期的错误",
            503: "Service Unavailable / 服务器当前不能处理客户端的请求",
        }
        result = status_dict.get(code, "其他未知问题")
        print(green(result) if code == 200 else red(result))
        lines()

    @staticmethod
    def html_writer(response_result: str, c_date: str, get=True) -> None:
        """ html 信息记录器 """
        # 构建存储路径
        file_path = f"{c_date} response_get.html" if get else f"{c_date} response_post.html"
        # 保存至文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response_result)

    @staticmethod
    def scrape_sleeper():
        """ 休眠函数 """
        sleep_time = random.randint(1, 3)
        # print(f"随机休眠 {sleep_time} 秒")
        time.sleep(sleep_time)

    @staticmethod
    def excel_writer(df: DataFrame, file_name: str, ctime: str) -> str:
        """ Excel 信息记录器 """
        # 构建存储路径
        file_path = f"{ctime} {file_name}.xlsx"
        # 保存至 Excel 文件
        df.to_excel(file_path, sheet_name="data", index=False)
        print(f"{green(f'信息已保存至 {file_path}！')}")
        return file_path

    @staticmethod
    def file_writer(data: bytes | bytearray, ctime: str, file_name=None, file_suffix=None) -> str:
        """ 文件信息记录器 """
        # 构建存储路径
        file_suffix = file_suffix if file_suffix is not None else ".png"
        file_path = f"{ctime} {file_name}{file_suffix}"
        # 保存至文件
        with open(file_path, "wb") as f:
            f.write(data)
            print(f"{green(f'{file_path} 已保存！')}")
            lines()
        return file_path

    @classmethod
    def video_downloader(cls, ua: UserAgent, video_dict: dict, ctime: str) -> None:
        """ 视频下载器 """
        # 获取视频信息
        video_name = video_dict["name"]
        video_url = video_dict["url"]
        print(f"正在下载 {yellow(video_name)} 视频...")
        # 发送请求
        video_data = requests.get(
            url=video_url,
            headers={"User-Agent": UserAgent().random},
            stream=True,
            timeout=10
        ).content
        # 保存至文件
        folder_name = "videos"
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        video_path = f"{folder_name}/{video_name}.mp4"
        with open(video_path, "wb") as f:
            f.write(video_data)
            print(f"{yellow(video_name)} 视频已保存为：{green(video_path)} ！")


class BaiduOCR(object):
    """ 百度 OCR 识别器 """

    def __init__(self):
        self.__app_id = "108492970"
        self.__api_key = "0ZxkXG4ovNghyzcgQ21a2TmN"
        self.__secret_key = "fcJog4Xd83dcWrDSz1KNhsiaLqgd8n15"

    def fetch_access_token(self) -> str | None:
        """ 获取百度 OCR 访问 token """
        host = (
            f"https://aip.baidubce.com/oauth/2.0/token"
            f"?grant_type=client_credentials"
            f"&client_id={self.__api_key}"
            f"&client_secret={self.__secret_key}"
        )
        response = requests.get(host)
        if response:
            __access_token = response.json()["access_token"]
            # print(f"获取成功！access_token：{cpc.PrintColour.green(__access_token)}")
            return __access_token
        else:
            print(red("获取 access_token 失败！"))
            return None

    @classmethod
    def ocr_recognizer(cls, img_path: str, access_token: str) -> str | None:
        """ 百度 OCR 识别器 """
        # 二进制方式打开图片文件
        f = open(img_path, "rb")
        img = base64.b64encode(f.read())
        # 定义请求参数
        ocr_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
        request_url = ocr_url + "?access_token=" + access_token
        params = {"image": img}
        headers = {
            "content-type": "application/x-www-form-urlencoded",
        }
        # 发送请求
        response = requests.post(request_url, headers=headers, data=params, stream=True, timeout=10)
        if response:
            img_text = response.json()["words_result"][0]["words"]
            print(f"OCR 识别成功！识别结果：{green(img_text)}")
            return img_text
        else:
            print(red("OCR 识别失败！"))
            return None


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

    # 初始化 UA
    fake_ua = UserAgent()

    # 目标网址
    url = "https://books.toscrape.com/"

    # 发起请求
    WebsiteRequester.response_get(fake_ua, url, current_date, bytes_out=False)


if __name__ == "__main__":
    main()
