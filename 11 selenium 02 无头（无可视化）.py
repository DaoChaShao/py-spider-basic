
from bs4 import BeautifulSoup  # 格式化 HTML 代码
from selenium import webdriver  # 驱动浏览器
from selenium.webdriver.common.by import By  # 用来定位元素
from selenium.webdriver.remote.webelement import WebElement  # 元素对象
from selenium.webdriver.support import expected_conditions as EC  # 等待条件
from selenium.webdriver.support.ui import WebDriverWait  # 等待页面加载完成
from selenium.webdriver.chrome.options import Options  # 无头模式

import time


class SeleniumScraper(object):
    """ selenium 爬虫器 """
    def __init__(self) -> None:
        # 实例化无头模式的浏览器
        options = Options()
        options.add_argument("--headless")  # 无头模式
        options.add_argument("--disable-gpu")  # 禁用 GPU 加速
        options.add_argument("--disable-blink-features=AutomationControlled")  # 规避检测
        options.add_experimental_option(name="excludeSwitches", value=["enable-automation"])  # 规避检测
        options.add_experimental_option(name="useAutomationExtension", value=False)  # 规避检测

        self.browser = webdriver.Chrome(options=options)

        self.browser.execute_cdp_cmd(
            cmd="Page.addScriptToEvaluateOnNewDocument",
            cmd_args={"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
        )

    def __del__(self) -> None:
        """ 析构函数 """
        self.browser.quit()

    def load_waiter(self, locator: tuple[str, str]) -> WebElement:
        """ 等待页面加载完成，返回可点击的元素 """
        return WebDriverWait(driver=self.browser, timeout=5).until(
            EC.element_to_be_clickable(locator)
        )

    @staticmethod
    def html_formatter(html_info: str) -> str:
        """ 格式化 HTML 代码 """
        soup = BeautifulSoup(html_info, "html.parser")
        return soup.prettify()

    @staticmethod
    def html_writer(html_info: str, get=True) -> None:
        """ html 信息记录器 """
        # 获取当前时间戳
        time_stamp = time.localtime()
        # 格式化今日日期、时间
        c_date = time.strftime("%Y%m%d", time_stamp)
        # 构建存储路径
        file_path = f"{c_date} response_get.html" if get else f"{c_date} response_post.html"
        # 保存至文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_info)

    def scraper_get(self, url: str) -> None:
        """ 信息爬取 """
        # 访问网页
        self.browser.get(url)

        # 获取 html 代码
        html_format = SeleniumScraper.html_formatter(self.browser.page_source)
        # print(f"{url} 的 HTML 代码:\n{html_format}")
        # 记录 html 代码
        SeleniumScraper.html_writer(html_format, get=True)


def main():
    """ 主函数 """
    # 目标网址
    url = "https://www.google.co.nz/"
    # 实例化
    scraper = SeleniumScraper()

    # 网页信息爬取
    scraper.scraper_get(url)


if __name__ == "__main__":
    main()
