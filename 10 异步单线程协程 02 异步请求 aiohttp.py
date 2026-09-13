from fake_useragent import UserAgent  # 作用：随机生成User-Agent

import aiohttp  # 作用：异步HTTP请求库（pip3 install aiohttp）
import asyncio

from utils import red, countdown


class AsyncScraper:
    """ 异步爬虫类 """

    def __init__(self, ua: UserAgent) -> None:
        self.headers = {
            "User-Agent": ua,
        }
        self.get_params = {}
        self.post_data = {}
        self.proxy = ""

    async def get_response(self, url: str) -> str | bytes or None:
        """ 异步下载器 """
        async with aiohttp.ClientSession() as session:
            async with await session.get(
                    url=url, headers=self.headers,
                    params=self.get_params, proxy=self.proxy
            ) as response:
                if response.status == 200:
                    """
                    .text()：获取响应内容，以字符串形式返回
                    .content：获取响应内容，以字节形式返回
                    .json()：获取响应内容，以json格式返回
                    """
                    html_out = await response.text()
                    print(f"{url} 的响应内容为：\n{html_out}")
                    return html_out
                else:
                    print(f"{url} 响应状态码为 {red(response.status)}")
                    return None

    async def post_response(self, url: str) -> str | bytes or None:
        """ 异步上传器 """
        async with aiohttp.ClientSession() as session:
            async with await session.post(
                    url=url, headers=self.headers,
                    data=self.post_data, proxy=self.proxy
            ) as response:
                if response.status == 200:
                    """
                    .text()：获取响应内容，以字符串形式返回
                    .content：获取响应内容，以字节形式返回
                    .json()：获取响应内容，以json格式返回
                    """
                    html_out = await response.text()
                    print(f"{url} 的响应内容为：\n{html_out}")
                    return html_out
                else:
                    print(f"{url} 响应状态码为 {red(response.status)}")
                    return None


@countdown
def main():
    """ 主函数 """
    # 实例化 UserAgent
    ua = UserAgent()
    # 实例化异步爬虫类
    async_scraper = AsyncScraper(ua)

    # 构建 url 列表
    urls = [
        "https://www.baidu.com",
        "https://www.sina.com.cn",
        "https://www.sohu.com",
    ]

    # 构建任务列表
    tasks = []

    for url in urls:
        # 创建协程
        coro = async_scraper.get_response(url)
        # 将协程封装为任务
        task = asyncio.ensure_future(coro)
        # 将任务加入任务列表
        tasks.append(task)

    # 创建事件循环
    loop = asyncio.get_event_loop()
    # 运行事件循环
    loop.run_until_complete(asyncio.wait(tasks))
    # 关闭事件循环
    loop.close()
    print("爬取完毕")


if __name__ == "__main__":
    main()
