
from selenium import webdriver  # pip3 install selenium
from selenium.webdriver.common.by import By  # 用来定位元素
from selenium.webdriver.remote.webelement import WebElement  # 元素对象
from selenium.webdriver.support.ui import WebDriverWait  # 等待页面加载完成
from selenium.webdriver.support import expected_conditions as EC  # 等待条件

import random
import time


class SeleniumScraper(object):
    """ selenium 爬虫器 """
    def __init__(self) -> None:
        self.browser = webdriver.Chrome()

    def __del__(self) -> None:
        """ 析构函数 """
        self.browser.quit()

    def avoid_detection(self) -> None:
        """ 防止被检测 """
        return self.browser.execute_cdp_cmd(
            cmd="Page.addScriptToEvaluateOnNewDocument",
            cmd_args={"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
        )

    def load_waiter(self, locator: tuple[str, str]) -> WebElement:
        """ 等待页面加载完成，返回可点击的元素 """
        return WebDriverWait(driver=self.browser, timeout=5).until(
            EC.element_to_be_clickable(locator)
        )

    def scraper_get(self, url: str) -> None:
        """ 信息爬取 """
        # 绕开检测
        self.avoid_detection()
        # 访问网页
        self.browser.get(url)

        # 等待页面加载完成
        search_locator = (By.CLASS_NAME, "gLFyf")
        self.load_waiter(search_locator)
        # 定位元素：搜索框
        search = self.browser.find_element(by=search_locator[0], value=search_locator[1])

        # 输入搜索内容
        search.send_keys("iPhone")

        # 定位元素：搜索按钮
        button_locator = (By.NAME, "btnK")
        button = self.browser.find_element(by=button_locator[0], value=button_locator[1])

        # 等待按钮可点击
        self.load_waiter(button_locator)
        # 点击搜索按钮
        button.click()

        # 执行 js 向下滚动
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 页面保持 5 秒，然后关闭
        SeleniumScraper.scrape_sleeper(fixed=True)

    @staticmethod
    def scrape_sleeper(fixed=True) -> None:
        """ 休眠函数 """
        sleep_time = 5 if fixed else random.randint(1, 3)
        # print(f"休眠 {sleep_time} 秒")
        time.sleep(sleep_time)


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
