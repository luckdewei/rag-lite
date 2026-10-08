# 导入必要的模块
from concurrent.futures import ThreadPoolExecutor
import time


def calculate_square(num1, num2):
    time.sleep(1)
    return num1 + num2


numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# We use process_cpu_count + 4 for both types of tasks.
# But we limit it to 32 to avoid consuming surprisingly large resource
with ThreadPoolExecutor(max_workers=3) as executor:
    # 向线程池提交一个任务
    futures = [executor.submit(calculate_square, num, num) for num in numbers]
    for future in futures:
        result = future.result()
        print(result)
