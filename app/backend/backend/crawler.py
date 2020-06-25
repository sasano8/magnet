import signal
import os
import time
from typing import List
from celery import task

from celery import Celery

# 第一引数→カレントモジュールの名前
# broker引数→ブローカーのURL


app = Celery('crawler', broker='amqp://guest@rabbitmq:5672//')
# app.conf.result_backend = 'redis://localhost:6379/0'  # 実行結果を保存するために追加
#app.conf.task_routes = {"app.worker.test_celery": "main-queue"}

__DRIVER = None

def receive_signal(signum, stack):
    global __DRIVER
    if __DRIVER:
        __DRIVER.quit()
        print("test")


signal.signal(signal.SIGTERM, receive_signal)
# signal.signal(signal.SIGKILL, receive_signal)

def get_driver():
    # TODO: 起動時間がもったいないため、アイドル中のdriverを再利用したい。（難易度はかなり高い）
    # https://tarunlalwani.com/post/reusing-existing-browser-session-selenium/

    global __DRIVER

    if __DRIVER:
        pass

    else:
        from selenium import webdriver
        from selenium.webdriver import DesiredCapabilities

        print("create driver.")
        connector = ""
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_argument('--blink-settings=imagesEnabled=false')

        is_debug = bool(os.environ.get('IS_SELENIUM_DEBUG', False))
        is_debug = True

        if is_debug:
            connector = "http://localhost:4444/wd/hub"
        else:
            connector = "http://selenium:4444/wd/hub"

        __DRIVER = webdriver.Remote(command_executor=connector,
                                  desired_capabilities=DesiredCapabilities.CHROME.copy(), options=chrome_option, keep_alive=True)


    return __DRIVER


@app.task(queue="queue_crawler")
def task_wait(x, y):
    time.sleep(10)
    result =  x + y
    dic = {"result": x + y}
    print(dic)
    return dic


@app.task(queue="queue_crawler")
def exec_crawler(keyword: str, option_keywords: List[str], deps: int = 0):

    driver = get_driver()

    try:
        driver.get('https://www.google.com/search?q={}'.format(keyword))
        import time
        # time.sleep(10)
        print(driver.title)
        # title = driver.title
        # text = driver.find_element_by_css_selector('article').text
    finally:
        # driverを再利用するため、１つだけタブを残して、それ以外のタブを全て閉じ、空白ページを表示させる
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if len(driver.window_handles) != 1:
                driver.close()

        driver.get('about:blank')

    return {"message": "Hello World"}


if __name__ == "__main__":


    # app.conf.update(argv)
    # app.conf.task_always_eager = True

    kwargs = None

    import threading

    argv = [
        "worker",
        f"--app={app.Worker.app.main}",
        "--loglevel=DEBUG",
        "--queues=queue_crawler",
        "-l=info",
        "-c=1",
        "-E"
    ]

    # main_func = lambda: app.worker_main(argv=argv)


    from entrypoint.start_crawler import run
    celery_cmdline = 'celery worker --app crawler -l info -c 1 -E --queues queue_crawler'
    # p = os.getcwd()

    run(os.getcwd(), celery_cmdline, os.getcwd())
    # run(os.getcwd(), thread, os.getcwd())

    # やりたいこと
    # breakpointで捕捉させる
    # auto reloadを有効にする

    # 進捗
    # 片方ずつのソリューションは実現することができた

    # サブプロセスを作成しブレークポイントを捕捉できるか　→　捕捉できない
    # スレッドを作成しブレークポイントを捕捉できるか
    # loop機構でブレークポイントを捕捉できるか　→　ループ機構に当てはめる処理がどこか分からない　→ハックするのは困難


