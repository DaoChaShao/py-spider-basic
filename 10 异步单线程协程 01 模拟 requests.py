import asyncio

from utils import countdown


async def info_scaper(url):
    """ 模拟下载循环 """
    print(f"正在爬取 {url} 中信息")
    # 模拟request下载过程（由于异步协程中不能出现同步阻塞的操作（time.sleep(2)），因此只能使用异步挂起操作）
    await asyncio.sleep(2)
    print(f"{url} 中信息爬取完毕")


@countdown
def main():
    """ 主函数 """
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
        coro = info_scaper(url)
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
