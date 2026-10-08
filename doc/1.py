from concurrent.futures import ThreadPoolExecutor
import time


def download_url(url):
    time.sleep(1)
    return f"{url}:下载完成，大小是1024个字节"


urls = ["http://www.example1.org", "http://www.example2.org", "http://www.example3.org"]

# 使用线程 池执行器
# max_workers 指的是指定最大工作线程数
with ThreadPoolExecutor(max_workers=3) as executor:
    # 可以使用map方法批量提交任务
    # map函数会自动为每个url创建一个任务，并提交到线程池
    results = executor.map(download_url, urls)
    for result in results:
        print(result)
