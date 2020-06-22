import os
import time
from typing import List
from celery import task

from celery import Celery

# 第一引数→カレントモジュールの名前
# broker引数→ブローカーのURL


app = Celery('crawler', broker='amqp://guest@queue:5672//')
# app.conf.result_backend = 'redis://localhost:6379/0'  # 実行結果を保存するために追加
#app.conf.task_routes = {"app.worker.test_celery": "main-queue"}

__DRIVER = None

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
            connector = "http://selenium-debug:4444/wd/hub"
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
    # argv =[
    #     "worker",
    #     f"--app={app.Worker.app.main}",
    #     "--loglevel=DEBUG",
    #     "--queues=queue_crawler",
    #     "-l=info",
    #     "-c=1",
    #     "-E"
    # ]
    # app.worker_main(argv=argv)

    from entrypoint.start_crawler import main
    main()
