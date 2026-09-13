from multiprocessing.dummy import Pool

import time

from utils import countdown


def single_request(url):
    """ 模拟下载循环 """
    print(f"正在爬取 {url} 中信息")
    time.sleep(2)
    print(f"{url} 中信息爬取完毕")


@countdown
def main_traditional():
    """ 传统爬虫 """
    urls = ["url_1", "url_2", "url_3", "url_4"]

    for page_num in range(len(urls)):
        single_request(urls[page_num])


@countdown
def main_pool():
    """ 异步爬虫线程池 """
    urls = ["url_1", "url_2", "url_3", "url_4"]

    # 实例化线程池
    pool = Pool(4)
    # 异步执行爬取任务
    pool.map(single_request, urls)
    # 关闭线程池
    pool.close()
    # 等待所有任务完成
    pool.join()
    print("所有任务完成")


if __name__ == "__main__":
    main_traditional()
    main_pool()
